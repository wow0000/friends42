from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory, make_response, redirect
import maps.maps as maps

app = Blueprint('api', __name__, template_folder='templates', static_folder='static')


@app.route('/public/clusters_info/<int:campus>/<token>')
def clusters(campus, token):
	if campus not in maps.available:
		return f'Campus not supported', 404
	db = Db("database.db")
	user = db.get_user_by_bookie(token)
	issues = db.get_issues()
	db.close()
	if user == 0:
		return 'Not authorized', 401
	cache_tab = get_cached_locations(campus)
	campus_map = maps.available[campus].map
	if 'buildings' not in campus_map:
		return "This campus is not supported yet.", 404
	last_update = get_last_update(1)
	last_update = [last_update[0].format('YYYY-MM-DD HH:mm:ss ZZ'), last_update[1]]
	# Buildings
	ret_builds = {}
	for build in campus_map['buildings'].keys():
		users = 0
		all_place = 0
		for user in cache_tab:
			if build in user['host']:
				users += 1
		for cluster in campus_map['buildings'][build]:
			all_place += maps.places(campus_map['exrypz'], campus_map[cluster])
		ret_builds[build] = {'taken': users, 'max_place': all_place}
	# Issue
	issues_map = {}
	for issue in issues:
		if issue['station'] not in issues_map:
			issues_map[issue['station']] = 1
	# Clusters
	ret_clusters = {}
	location_map = {}
	for user in cache_tab:
		location_map[user['host']] = user
	for cluster in campus_map['allowed']:
		ret_clusters[cluster] = {"taken": maps.count_in_cluster(cluster, location_map),
		                         "max_place": maps.places(campus_map['exrypz'], campus_map[cluster]),
		                         "dead_pc": maps.count_in_cluster(cluster, issues_map)}
	return {"update": last_update, "buildings": ret_builds, "clusters": ret_clusters}


@app.route('/public/get_dead_pc/<token>')
def print_dead_pc(token):
	db = Db("database.db")
	user = db.get_user_by_bookie(token)
	issues = db.get_issues()
	db.close()
	if user == 0:
		return 'Not authorized', 401
	return issues


@app.route('/public/last_pos/<login>')
@auth_required
def last_pos(login, userid):
	return get_last_pos(login)


@app.route('/public/whats_my_token/')
@auth_required
def print_token(userid):
	return request.cookies['token']


@app.route('/bocal/delete_issue/<token>/<station>')
def delete_issue(token, station):
	if token != config.bocal_token:
		return 'Bad token', 401
	with Db() as db:
		db.delete_issues(station)
		issues = db.get_issues()
	return issues, 200
