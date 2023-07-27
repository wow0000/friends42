import config
from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory

app = Blueprint('theme', __name__, template_folder='templates')


@app.route('/theme/set/', methods=['POST'])
@auth_required
def theme_set(userid):
	data = request.get_json()
	if not data:
		return '', 401
	if 'javascript' not in data or 'css' not in data or 'enabled' not in data:
		return '', 402
	db = Db("database.db")
	ret = db.update_theme(userid['userid'], data['css'], data['javascript'], int(data['enabled']))
	db.close()
	if ret:
		return '', 200
	else:
		return '', 400


@app.route('/reset')
@auth_required
def theme_disable(userid):
	db = Db("database.db")
	data = db.get_theme(userid['userid'])
	ret = db.update_theme(userid['userid'], data['css'], data['javascript'], 0)
	db.close()
	if ret:
		return 'OK', 200
	return 'Erreur!!!', 400
