from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory, make_response
import maps.maps as maps
import time

app = Blueprint('idle', __name__, template_folder='templates', static_folder='static')


# one day it'll be clean, but that day is not today
@app.route('/idle/<building>')
@auth_required
def idle(building, userid):
	db = Db("database.db")
	campus_id = db.get_user_by_id(userid['userid'])['campus']
	if campus_id not in maps.available:
		db.close()
		return f'Your campus layout is not yet supported, send a DM to @wow000 or @neoblacks on Discord to get started (Your campus id: {campus_id})', 200
	issues = db.get_issues()
	theme = db.get_theme(userid['userid'])
	piscines = [x['cluster'] for x in db.get_piscines(userid['campus'])]
	db.close()
	cache_tab = get_cached_locations(campus_id)
	campus_map = maps.available[campus_id].map
	if 'buildings' not in campus_map or building not in campus_map['buildings']:
		return "This campus is not supported yet."
	clusters_to_load = campus_map['buildings'][building]
	location_map = {}
	issues_map = {}
	for user in cache_tab:
		location_map[user['host']] = user
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
		for cluster in clusters_to_load]
	places = [0, 0]
	last_update = get_last_update(campus_id)
	last_update = [last_update[0].humanize(locale='fr', granularity='minute'), last_update[1]]
	for cluster in clusters_list:
		places[0] += cluster['users']
		places[1] += cluster['maximum_places'] - cluster['dead_pc']
	ret_builds = []
	for build in campus_map['buildings'].keys():
		users = 0
		all_place = 0
		classes = []
		for user in cache_tab:
			if build in user['host']:
				users += 1
		for cluster in campus_map['buildings'][build]:
			all_place += maps.places(campus_map['exrypz'], campus_map[cluster])
		for class_name in campus_map['kiosk_classes'].keys():
			for cluster in campus_map['kiosk_classes'][class_name]:
				if build in cluster and class_name not in classes:
					classes.append(class_name)
		for piscine in piscines:
			if build in piscine and 'Piscine' not in classes:
				classes.append('<i class="fa-solid fa-person-swimming text-info"></i>')
		ret_builds.append(
			{'name': build, 'taken': users, 'all_place': all_place, 'free': all_place - users, 'classes': classes})
	resp = make_response(
		render_template('idle.html', locations=location_map, clusters=clusters_list,
		                issues_map=issues_map, exrypz=campus_map['exrypz'], piscine=piscines,
		                theme=theme, kiosk=True, places=places, scroll=clusters_to_load, last_update=last_update,
		                kiosk_class=campus_map['kiosk_classes'], buildings=ret_builds, building=building))
	resp.set_cookie('token', request.cookies.get('token'), expires=time.time() + 30 * 86400, httponly=True)
	return resp


@app.route('/new/<building>')
@auth_required
def idle_new(building, userid):
	db = Db("database.db")
	campus_id = db.get_user_by_id(userid['userid'])['campus']
	if campus_id not in maps.available:
		db.close()
		return f'Your campus layout is not yet supported, send a DM to @wow000 or @neoblacks on Discord to get started (Your campus id: {campus_id})', 200
	issues = db.get_issues()
	theme = db.get_theme(userid['userid'])
	friends = db.get_friends(userid['userid'])
	me = db.get_user_profile_id(userid['userid'])
	db.close()
	cache_tab = get_cached_locations(campus_id)
	campus_map = maps.available[campus_id].map
	if 'buildings' not in campus_map or building not in campus_map['buildings']:
		return "This campus is not supported yet."
	clusters_to_load = campus_map['buildings'][building]
	location_map = {}
	issues_map = {}
	for user in cache_tab:
		location_map[user['host']] = user
		location_map[user['host']]['classes'] = ""
		if user['user']['id'] == userid['userid']:
			location_map[user['host']]['classes'] += "me "
		if user['user']['id'] in [e['has'] for e in friends if e['relation'] == 1]:
			location_map[user['host']]['classes'] += "close_friend "
		elif user['user']['id'] in [e['has'] for e in friends]:
			location_map[user['host']]['classes'] += "friend "
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
		for cluster in clusters_to_load]
	places = [0, 0]
	last_update = get_last_update(campus_id)
	last_update = [last_update[0].humanize(locale='fr', granularity='minute'), last_update[1]]
	for cluster in clusters_list:
		places[0] += cluster['users']
		places[1] += cluster['maximum_places'] - cluster['dead_pc']
	ret_builds = []
	for build in campus_map['buildings'].keys():
		users = 0
		all_place = 0
		classes = []
		for user in cache_tab:
			if build in user['host']:
				users += 1
		for cluster in campus_map['buildings'][build]:
			all_place += maps.places(campus_map['exrypz'], campus_map[cluster])
		for class_name in campus_map['kiosk_classes'].keys():
			for cluster in campus_map['kiosk_classes'][class_name]:
				if build in cluster and class_name not in classes:
					classes.append(class_name)
		for piscine in campus_map['piscine']:
			if build in piscine and 'Piscine' not in classes:
				classes.append('<i class="fa-solid fa-person-swimming text-info"></i>')
		ret_builds.append(
			{'name': build, 'taken': users, 'all_place': all_place, 'free': all_place - users, 'classes': classes})
	resp = make_response(
		render_template('idle.html', locations=location_map, clusters=clusters_list,
		                issues_map=issues_map, exrypz=campus_map['exrypz'], piscine=campus_map['piscine'],
		                theme=theme, kiosk=False, places=places, scroll=clusters_to_load, last_update=last_update,
		                kiosk_class=campus_map['kiosk_classes'], buildings=ret_builds, building=building))
	return resp
