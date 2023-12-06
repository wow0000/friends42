import config
from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory
import maps.maps as maps

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


@app.route('/goto/<pos>')
@auth_required
def goto_route(pos, userid):
	db = Db("database.db")
	campus_id = db.get_user_by_id(userid['userid'])['campus']
	db.close()
	if campus_id not in maps.available:
		return f'Your campus layout is not yet supported, send a DM to @wow000 or @neoblacks on Discord to get started (Your campus id: {campus_id})', 200
	data = maps.available[campus_id].exrypz(pos)
	if 'made' not in data['etage'].lower():
		data['etage'] = data['etage'].rstrip('A')
		data['etage'] = data['etage'].rstrip('B')
	if not data or 'etage' not in data or data['etage'] not in maps.available[campus_id].map['allowed']:
		return f"{pos} not found !!!", 404
	return make_response(redirect(f"/?cluster={data['etage']}&p={pos}", 307))
