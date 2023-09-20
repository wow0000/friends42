import config
from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory

app = Blueprint('mates', __name__, template_folder='templates')


def apply_modifications_mates(db, projects):
	for proj in projects:
		proj['a_mates'] = [db.get_user_by_login(mate.strip()) for mate in proj['mates'].split(',')]
		proj['date'] = date_relative(proj['created'], ['day'])
		for mate in proj['a_mates']:
			mate['image_medium'] = proxy_images(mate['image_medium'])
	return projects


@app.route('/mates/')
@auth_required
def mates_default_route(userid):
	db = Db("database.db")
	latest = db.get_latest_mates(userid['campus'])
	apply_modifications_mates(db, latest)
	theme = db.get_theme(userid['userid'])
	db.close()
	return render_template('mate.html', project=False, projects=latest, projectsList=get_projects(False),
	                       creator_id=userid['userid'], theme=theme)


@app.route('/mates/<project>')
@auth_required
def mates_route(project, userid):
	if does_group_project_exists(project) is False:
		return 'Unknown project', 404
	db = Db("database.db")
	projects = db.get_mates(project, userid['campus'])
	theme = db.get_theme(userid['userid'])
	project_info = db.get_project(project, r)
	apply_modifications_mates(db, projects)
	db.close()
	project_info['attachements'] = json.loads(project_info['attachements'])
	return render_template('mate.html', project=project, projects=projects or {}, projectsList=get_projects(False),
	                       creator_id=userid['userid'], theme=theme, project_info=project_info)


@app.route("/mates/<project_id>/contact")
@auth_required
def contact_mate_route(project_id, userid):
	db = Db("database.db")
	project = db.get_mate_by_id(project_id)
	db.close()

	if project is None:
		return '', 404
	return project['contact']


@app.route("/mates/<project_id>/delete")
@auth_required
def remove_mate_route(project_id, userid):
	db = Db("database.db")
	project = db.get_mate_by_id(project_id)
	if project is None:
		db.close()
		return '', 404
	if project['creator_id'] != userid['userid']:
		db.close()
		return '', 403
	db.delete_mate(project_id)
	db.close()
	return '', 200


@app.route("/mates/<project>/post", methods=['POST'])
@auth_required
def post_mate_route(project, userid):
	if does_group_project_exists(project) is False:
		return 'Unknown project', 404
	data = request.get_json()
	if 'progress' not in data or 'quick_contact' not in data or 'mates' not in data or 'description' not in data or 'contact' not in data or 'people' not in data:
		return 'Missing field', 411
	if 'length' not in data:
		data['length'] = None
	if not str.isnumeric(data['progress']) or not str.isnumeric(data['people']):
		return 'Invalid int', 413
	data['progress'] = int(data['progress'])
	data['people'] = int(data['people'])
	mates: list[str] = [mate.strip() for mate in data['mates'].split(',')]
	db = Db("database.db")
	if db.get_project(project, r)['solo'] == 1:
		db.close()
		return 'This is a solo project!!!', 405
	final_mate = []
	for mate in mates:
		mate = mate.strip()
		if len(mate) == 0:
			continue
		user = db.get_user_profile(mate, api)
		if user is None:
			db.close()
			return 'Unknown mate', 412
		if user['id'] != userid['userid']:
			final_mate.append(mate)
	if len(final_mate) > 8:
		db.close()
		return 'Too many mates', 413
	creator_user = db.get_user_by_id(userid['userid'])
	final_mate.insert(0, creator_user['name'])
	if len(final_mate) > data['people']:
		db.close()
		return 'You have more mates than your limit allows', 417
	ret = db.new_mate(userid['userid'], project, data['length'], data['progress'], data['quick_contact'],
	                  ','.join(final_mate), data['description'], data['contact'], data['people'])
	db.close()
	if ret != 0:
		return 'Unknown error', 500 + ret
	return '', 200


@app.route('/mates/<project>/new/')
@auth_required
def new_mates_route(project, userid):
	if does_group_project_exists(project) is False:
		return 'Unknown project', 404
	return render_template('new_mate.html', project=project, edit={})


@app.route('/mates/<project_id>/edit/')
@auth_required
def edit_mates_route(project_id, userid):
	db = Db("database.db")
	project = db.get_mate_by_id(project_id)
	theme = db.get_theme(userid['userid'])
	db.close()
	if project is None or project['creator_id'] != userid['userid']:
		db.close()
		return '', 403
	return render_template('new_mate.html', project=project['project'], edit=project, theme=theme)
