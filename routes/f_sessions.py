import config
from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory

app = Blueprint('session', __name__, template_folder='templates')


@app.route('/sessions/reset/')
@auth_required
def session_reset(userid):
	db = Db("database.db")
	db.reset_user_cookies(userid['userid'])
	db.close()
	return '', 200
