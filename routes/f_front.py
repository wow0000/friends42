from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory
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
	db.close()
	if user is None:
		return "", 404
	user["position"] = get_position(user['name'])
	if user['active'] and user['position'] is None:
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
	db.close()
	return render_template('settings.html', user=user, notif=notif, theme=theme, cookies=cookies)


@app.route('/')
@auth_required
def index(userid):
	db = Db("database.db")
	pos = standard_cluster(get_position(userid['userid']))
	campus_id = db.get_user_by_id(userid['userid'])['campus']
	if campus_id not in maps.available:
		db.close()
		return f'Your campus layout is not yet supported, send a DM to @wow000 or @neoblacks on Discord to get started (Your campus id: {campus_id})', 200
	campus_map = maps.available[campus_id].map
	if pos and type(campus_map['exrypz'](pos)) == bool:
		pos = campus_map['default']
	else:
		pos = campus_map['default'] if not pos else campus_map['exrypz'](pos)['etage']
	cluster_name = pos if request.args.get('cluster') is None else request.args.get('cluster')
	if cluster_name not in campus_map['allowed']:
		cluster_name = campus_map['default']
	cache_tab = get_cached_locations(campus_id)
	location_map = {}
	friends = db.get_friends(userid['userid'])
	issues = db.get_issues()
	me = db.get_user_profile_id(userid['userid'])
	theme = db.get_theme(userid['userid'])
	db.close()
	issues_map = {}
	for user in cache_tab:
		user_id = user['user']['id']
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
		 "places": maps.available_seats(cluster, campus_map[cluster], campus_map['exrypz'], location_map, issues_map)}
		for cluster in campus_map['allowed']]
	return render_template('index.html', map=campus_map[cluster_name], locations=location_map,
	                       clusters=clusters_list, actual_cluster=cluster_name, issues_map=issues_map,
	                       exrypz=campus_map['exrypz'], piscine=campus_map['piscine'], theme=theme)


@app.route('/friends/')
@auth_required
def friends_route(userid):
	db = Db("database.db")
	theme = db.get_theme(userid['userid'])
	friend_list = db.get_friends(userid['userid'])
	db.close()
	for friend in friend_list:
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
