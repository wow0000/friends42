import config
from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory

app = Blueprint('monitoring', __name__, template_folder='templates')


@app.route('/monitoring/<token>/api42')
def monitoring_api42(token):
	if token != config.update_key:
		return 'Bad token', 400
	return '', 200 if api.get_token() else 500


@app.route('/monitoring/<token>/db')
def monitoring_db(token):
	if token != config.update_key:
		return 'Bad token', 400
	try:
		db = Db("database.db")
		db.search("eee")
		db.close()
	except:
		return 'BAD', 500
	return 'OK', 200


@app.route('/monitoring/<token>/redis')
def monitoring_redis(token):
	if token != config.update_key:
		return 'Bad token', 400
	try:
		r.set('monitoring', time.time())
	except:
		return 'BAD', 500
	return 'OK', 200
