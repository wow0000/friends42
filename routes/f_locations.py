import config
from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory

app = Blueprint('locations', __name__, template_folder='templates')


@app.route('/locations/<token>/<int:campus>')
def update_locs(token, campus):
	if token != config.update_key:
		return 'Bad token', 400
	locs(campus)
	return 'OK', 200


@app.route('/locations/<token>/<int:campus>/dbg')
def update_locs_dbg(token, campus):
	if token != config.update_key:
		return 'Bad token', 400
	return locs(campus)
