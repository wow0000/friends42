from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory, make_response, redirect
import maps.maps as maps

app = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


@app.route('/admin')
@auth_required
def admin(userid):
	if not userid['admin'] or userid['admin']['level'] < 1:
		return 'Not authorized', 401
	shadow_bans = []
	with Db() as db:
		if userid['admin']['level'] >= 3:
			shadow_bans = db.get_all_shadow_bans()
		piscines = db.get_all_piscines()
		silents = db.get_all_silents()
	return render_template('admin.html', user=userid, shadow_bans=shadow_bans, piscines=piscines, silents=silents)


@app.route('/admin/piscine_add', methods=['POST'])
@auth_required
def insert_piscine(userid):
	if not userid['admin'] or userid['admin']['level'] < 1:
		return 'Not authorized', 401
	if not verify_csrf(request.form['csrf']):
		return 'Please refresh and try again', 401
	with Db() as db:
		db.insert_piscine(int(request.form['campus']), request.form['cluster'])
	return ''


@app.route('/admin/piscine_remove/<int:ban_id>/<csrf>')
@auth_required
def piscine_remove(ban_id, csrf, userid):
	if not userid['admin'] or userid['admin']['level'] < 1:
		return 'Not authorized', 401
	if not verify_csrf(csrf):
		return 'Please refresh and try again', 401
	with Db() as db:
		db.remove_piscine(int(ban_id))
	return ''

@app.route('/admin/silent_add', methods=['POST'])
@auth_required
def insert_silent(userid):
	if not userid['admin'] or userid['admin']['level'] < 1:
		return 'Not authorized', 401
	if not verify_csrf(request.form['csrf']):
		return 'Please refresh and try again', 401
	with Db() as db:
		db.insert_silent(int(request.form['campus']), request.form['cluster'])
	return ''


@app.route('/admin/silent_remove/<int:ban_id>/<csrf>')
@auth_required
def silent_remove(ban_id, csrf, userid):
	if not userid['admin'] or userid['admin']['level'] < 1:
		return 'Not authorized', 401
	if not verify_csrf(csrf):
		return 'Please refresh and try again', 401
	with Db() as db:
		db.remove_silent(int(ban_id))
	return ''

@app.route('/admin/change_tag', methods=['POST'])
@auth_required
def change_tag(userid):
	if not userid['admin'] or userid['admin']['level'] < 1:
		return 'Not authorized', 401
	if not verify_csrf(request.form['csrf']):
		return 'Please refresh and try again', 401
	with Db() as db:
		db.admin_change_tag(userid['userid'], request.form['tag'])
	return ''


@app.route('/admin/shadow_ban', methods=['POST'])
@auth_required
def shadow_ban(userid):
	if not userid['admin'] or userid['admin']['level'] < 3:
		return 'Not authorized', 401
	if not verify_csrf(request.form['csrf']):
		return 'Please refresh and try again', 401
	with Db() as db:
		db.shadow_ban(int(request.form['victim']), int(request.form['offender']), request.form['reason'])
	return ''


@app.route('/admin/shadow_remove/<int:ban_id>/<csrf>')
@auth_required
def del_shadow_ban(ban_id, csrf, userid):
	if not userid['admin'] or userid['admin']['level'] < 3:
		return 'Not authorized', 401
	if not verify_csrf(csrf):
		return 'Please refresh and try again', 401
	with Db() as db:
		db.remove_shadow_ban(int(ban_id))
	return ''
