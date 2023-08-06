import config
from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory

app = Blueprint('telegram', __name__, template_folder='templates')


@app.route('/telegram/add/', methods=['POST'])
@auth_required
def telegram_add(userid):
	data = request.get_json()
	if not data:
		return '', 401
	if 'hash' not in data or 'id' not in data:
		return '', 402
	if not tg_check_hash(data):
		return '', 403
	db = Db("database.db")
	db.enable_notification(userid['userid'], data['id'])
	db.close()
	return '', 200


@app.route('/telegram/set_status/<status>/<msg>')
@auth_required
def telegram_status(status, msg, userid):
	status = int(status)
	db = Db("database.db")
	ret = db.status_notification(userid['userid'], status)
	if ret:
		ret = db.message_notification(userid['userid'], msg.strip())
	db.close()
	if not ret:
		return '', 400
	return '', 200


"""
@app.route('/telegram/admin/add/<login>')
@auth_required
def telegram_add_admin(login, userid):
	db = Db("database.db")
	db.enable_notification(userid['userid'], login)
	db.close()
	return '', 200
"""


@app.route('/telegram/remove')
@auth_required
def telegram_remove(userid):
	db = Db("database.db")
	db.unlink_notification(userid['userid'])
	db.close()
	return '', 200
