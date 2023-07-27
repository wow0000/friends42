from globals import *
from routes.helpers import *
from flask import Blueprint, make_response
import secrets
import time

app = Blueprint('auth', __name__, template_folder='templates')


@app.route('/redirect_42')
def redirect_42():
	link = config.auth_link.replace('{current_domain}', request.headers['host'])
	resp = make_response(redirect(link, 307))
	resp.set_cookie('state', secrets.token_hex(32), httponly=True)
	return resp


@app.route('/logout')
def logout():
	token = request.cookies.get('token')
	if not token:
		return 'Not logged in', 400
	db = Db("database.db")
	db.delete_cookie(token)
	db.close()
	resp = make_response('Successfully logged out')
	resp.delete_cookie('token')
	return resp


@app.route('/auth')
def auth():
	code = request.args.get('code')
	state = request.cookies.get('state')
	if code is None or state is None:
		return redirect('/', 307)
	if len(state) == 32:
		final_token = api.get_access_token(code, state, request.headers['host'])
		resp = make_response(redirect('/my_correction/' + final_token, 307))
		return resp
	user_id = api.get_user_id_by_token(code, state, request.headers['host'])
	if user_id == 0:
		return "Error while logging in. Please try again", 500
	db = Db("database.db")
	add_id = db.get_user(user_id)
	if add_id is None:
		status, resp = api.get_unknown_user(user_id)
		if status == 200:
			create_users(db, [{'user': resp}])
		else:
			return '', 500
	cookie = db.create_cookie(user_id, request.headers.get('User-Agent'))
	db.close()
	resp = make_response(redirect('/', 307))
	resp.set_cookie('token', cookie, expires=time.time() + 30 * 86400, httponly=True)  # 30 days
	return resp
