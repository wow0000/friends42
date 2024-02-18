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
	with Db("database.db") as db:
		campus_id = db.get_user_by_id(userid['userid'])['campus']
	if campus_id not in maps.available:
		return render_template('campus_refresh.html', campus_id=campus_id)
	data = maps.available[campus_id].exrypz(pos)
	if data and 'etage' in data and 'made' not in data['etage'].lower():
		data['etage'] = data['etage'].rstrip('A')
		data['etage'] = data['etage'].rstrip('B')
	if not data or 'etage' not in data or data['etage'] not in maps.available[campus_id].map['allowed']:
		return f"{pos} not found !!!", 404
	return make_response(redirect(f"/?cluster={data['etage']}&p={pos}", 307))


@app.route('/update_campus_id/')
@auth_required
def update_campus_id(userid):
	if r.get("campus_refreshed/" + str(userid['userid'])):
		return "Already refreshed, please wait 60s", 400
	ret_status, ret_data = api.get_unknown_user(userid['login'])
	if ret_status != 200:
		return "L'intra n'est pas disponible pour le moment, réessayez plus tard", 500
	r.set("campus_refreshed/" + str(userid['userid']), '1', ex=60)
	campus = find_correct_campus(ret_data)
	with Db("database.db") as db:
		db.create_user(ret_data, campus)
	return redirect('/', 307)
