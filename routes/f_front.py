from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory, make_response, redirect
import maps.maps as maps
import arrow

app = Blueprint('front', __name__, template_folder='templates', static_folder='static')


@app.route('/profile/<login>')
@auth_required
def profile(login, userid):
	db = Db("database.db")
	user = db.get_user_profile(login, api)
	if user is None:
		return '', 404
	is_friend = db.is_friend(userid['userid'], user['id']) is not False
	is_banned = db.is_banned(user['id'])
	theme = db.get_theme(userid['userid'])
	hide = is_shadow_banned(user['id'], userid['userid'], db)
	db.close()
	if user is None:
		return "", 404
	if hide:
		user['position'] = None
	else:
		user["position"] = get_position(user['name'])
	if user['active'] and user['position'] is None and hide == False:
		user["last_active"] = "depuis " + (
			arrow.get(user['active'], "YYYY-MM-DD HH:mm:ss", tzinfo='UTC')).humanize(locale='FR', only_distance=True)
	else:
		user["last_active"] = ""
	return render_template('profile.html', user=user, is_friend=is_friend, userid=userid, is_banned=is_banned,
	                       theme=theme)


@app.route('/settings/', methods=['GET', 'POST'])
@auth_required
def settings(userid):
	db = Db("database.db")
	login = db.get_user_by_id(userid['userid'])['name']
	user = db.get_user_profile(login)
	notif = db.has_notifications(userid['userid'])
	theme = db.get_theme(userid['userid'])
	cookies = db.get_user_cookies(userid['userid'])
	campus_id = db.get_user_by_id(userid['userid'])['campus']
	db.close()
	kiosk_buildings = {}
	if campus_id in maps.available:
		kiosk_buildings = maps.available[campus_id].map['buildings']
	return render_template('settings.html', user=user, notif=notif, theme=theme, cookies=cookies,
	                       kiosk_buildings=kiosk_buildings)


@app.route('/')
@auth_required
def index(userid):
	pos = standard_cluster(get_position(userid['userid']))
	db = Db("database.db")
	campus_id = db.get_user_by_id(userid['userid'])['campus']
	if campus_id not in maps.available:
		db.close()
		return f'Your campus layout is not yet supported, send a DM to @wow000 or @neoblacks on Discord to get started (Your campus id: {campus_id})', 200
	friends = db.get_friends(userid['userid'])
	issues = db.get_issues()
	me = db.get_user_profile_id(userid['userid'])
	theme = db.get_theme(userid['userid'])
	shadow_bans = db.get_shadow_bans(userid['userid'])
	db.close()
	campus_map = maps.available[campus_id].map
	if pos and type(campus_map['exrypz'](pos)) == bool:
		pos = campus_map['default']
	else:
		pos = campus_map['default'] if not pos else campus_map['exrypz'](pos)['etage']
	cache_tab = get_cached_locations(campus_id)
	cluster_name = pos if request.args.get('cluster') is None else request.args.get('cluster')
	if cluster_name not in campus_map['allowed']:
		cluster_name = campus_map['default']
	location_map = {}
	issues_map = {}
	for user in cache_tab:
		user_id = user['user']['id']
		if user_id in shadow_bans:
			continue
		location_map[user['host']] = user
		location_map[user['host']]['me'] = user_id == userid['userid']
		location_map[user['host']]['friend'] = user_id in [e['has'] for e in friends]
		location_map[user['host']]['close_friend'] = user_id in [e['has'] for e in friends if e['relation'] == 1]
		if me and 'pool' in me:
			location_map[user['host']]['pool'] = f"{user['user']['pool_month']} {user['user']['pool_year']}" == me[
				'pool']
		else:
			location_map[user['host']]['pool'] = False
	for issue in issues:
		if issue['station'] not in issues_map:
			issues_map[issue['station']] = {"count": 0}
		issues_map[issue['station']]['issue'] = issue['issue']
		issues_map[issue['station']]['count'] += 1
	clusters_list = [
		{"name": cluster, "exrypz": campus_map['exrypz'], "map": campus_map[cluster],
		 "maximum_places": maps.places(campus_map['exrypz'], campus_map[cluster]),
		 "users": maps.count_in_cluster(cluster, location_map),
		 "dead_pc": maps.count_in_cluster(cluster, issues_map),
		 "places": maps.available_seats(cluster, campus_map[cluster], campus_map['exrypz'], location_map, issues_map)}
		for cluster in campus_map['allowed']]
	return render_template('index.html', map=campus_map[cluster_name], locations=location_map,
	                       clusters=clusters_list, actual_cluster=cluster_name, issues_map=issues_map,
	                       exrypz=campus_map['exrypz'], piscine=campus_map['piscine'], theme=theme,
	                       focus=request.args.get('p'))


@app.route('/friends/')
@auth_required
def friends_route(userid):
	db = Db("database.db")
	theme = db.get_theme(userid['userid'])
	friend_list = db.get_friends(userid['userid'])
	shadow_bans = db.get_shadow_bans(userid['userid'])
	db.close()
	for friend in friend_list:
		if friend['has'] in shadow_bans:
			friend['position'] = None
			friend["last_active"] = ""
		else:
			friend["position"] = get_position(friend["name"])
			if friend['active'] and friend['position'] is None:
				date = arrow.get(friend['active'], "YYYY-MM-DD HH:mm:ss", tzinfo='UTC')
				friend["last_active"] = "depuis " + date.humanize(locale='FR', only_distance=True)
			else:
				friend["last_active"] = ""
	friend_list = sorted(friend_list, key=lambda d: d['name'])
	friend_list = sorted(friend_list, key=lambda d: 0 if d['relation'] == 1 else 1)
	friend_list = sorted(friend_list, key=lambda d: 0 if d['position'] else 1)
	return render_template('friends.html', friends=friend_list, theme=theme)


@app.route('/search/<keyword>/<int:friends_only>')
@auth_required
def search_route(keyword, friends_only, userid):
	if len(keyword) < 2 or '%' in keyword:
		return '', 400
	if ',' in keyword:
		keyword = keyword.split(',')[-1].strip()
		if len(keyword) < 3:
			return '', 400
	keyword = keyword.lower()
	db = Db("database.db")
	req_friends = db.search(keyword)
	projects = []
	if friends_only == 0:
		projects = find_keyword_project(keyword, False)
	db.close()
	resp = [{"type": "user", "v": e['name'], "s": e['name']} for e in req_friends]
	if friends_only == 0:
		resp += [{"type": "project", "v": e['name'], "s": e['slug']} for e in projects]
	return resp, 200


@app.route('/goto/<pos>')
@auth_required
def goto_route(pos, userid):
	db = Db("database.db")
	campus_id = db.get_user_by_id(userid['userid'])['campus']
	db.close()
	if campus_id not in maps.available:
		return f'Your campus layout is not yet supported, send a DM to @wow000 or @neoblacks on Discord to get started (Your campus id: {campus_id})', 200
	data = maps.available[campus_id].exrypz(pos)
	if not data or 'etage' not in data or data['etage'] not in maps.available[campus_id].map['allowed']:
		return f"{pos} not found !!!", 404
	return make_response(redirect(f"/?cluster={data['etage']}&p={pos}", 307))


# Manual things that need to be routed on /

@app.route('/static/<path:path>')
def send_static(path):
	return send_from_directory('static', path)


@app.route('/favicon.ico')
def favicon():
	return send_from_directory('static', 'img/favicon.ico')


@app.route('/manifest.json')
def manifest():
	return send_from_directory('static', 'manifest.json')


@app.route('/service_worker.json')
def service_worker():
	return send_from_directory('static', 'js/service_worker.js')


@app.route('/apple-touch-icon.png')
def apple_touch_icon():
	return send_from_directory('static', 'img/apple-touch-icon.png')
