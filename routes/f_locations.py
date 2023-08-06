import config
from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory

app = Blueprint('locations', __name__, template_folder='templates')


@app.route('/locations/<token>/<int:campus>')
def update_locs2(token, campus):
	if token == config.update_key:
		locs(campus)
		return '', 200
	return '', 400
