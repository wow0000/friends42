from globals import *
from routes.helpers import *
from flask import Blueprint, make_response

app = Blueprint('users', __name__, template_folder='templates')


@app.route('/search/<start>')
@auth_required
def search(start, userid):
	if len(start) < 3 or '%' in start:
		return '', 400
	if ',' in start:
		start = start.split(',')[-1].strip()
		if len(start) < 3:
			return '', 400
	start = start.lower()
	db = Db("database.db")
	req = db.search(start)
	db.close()
	resp = [e['name'] for e in req]
	return resp, 200


@app.route('/getuser/<login>')
@auth_required
def getuser(login, userid):
	db = Db("database.db")
	user = db.get_user_profile(login)
	if user is None:
		return '', 404
	is_friend = db.is_friend(userid['userid'], user['id'])
	user['is_friend'] = is_friend
	user["position"] = get_position(user['name'])
	user["image"] = proxy_images(user["image"])
	return dict(user)


@app.route('/settings/profile', methods=['POST'])
@auth_required
def settings_profile(userid):
	info = request.json
	if info is None:
		return 400
	db = Db("database.db")
	if db.is_banned(userid['userid']):
		return 'banned', 403
	success = db.set_profile(userid['userid'], dict(info))
	db.close()
	if not success:
		return '', 400
	return redirect('/settings/', 307)
