import config
from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory

app = Blueprint('messages', __name__, template_folder='templates')


def anonymize_messages(messages, userid=-1):
	for message in messages:
		if message['anonymous'] == 1 and message['author'] != int(userid):
			message['author'] = 0
			message['author_login'] = 'Anonyme'
	return messages


def send_msg(author, dest, msg, db, ano=False):
	db.insert_message(author['userid'], dest['id'], msg, 1 if 'anonymous' in request.form else 0)
	notifs = db.has_notifications(dest['id'])
	if notifs and notifs['enabled'] == 1:
		sender = "de " + author['login']
		if 'anonymous' in request.form:
			sender = 'Anonyme'
		send_raw_tg_dm(notifs['telegram_id'], f"📬 Nouveau message {sender} : {msg}")


@app.route('/messages/')
@auth_required
def msg_default_route(userid):
	with Db() as db:
		messages = db.get_messages(userid['userid'])
		db.mark_messages_as_read(userid['userid'])
	return render_template('messages.html', me=userid['userid'],
	                       messages=anonymize_messages(messages, userid['userid']), hide_msg=True)


@app.route("/messages/org/<token>")
@auth_required
def org_messages(token, userid):
	with Db() as db:
		user = db.get_special_user_by_key(token)
		if not user:
			return "Invalid token", 400
	return render_template('mass_messages.html', user=user)


@app.route('/messages/send/', methods=['POST'])
@auth_required
def msg_send(userid):
	if not verify_csrf(request.form['csrf']):
		return 'Please refresh and try again', 401
	if 'message' not in request.form or not request.form['message']:
		return 'Message is empty or malformed', 400
	# Remove this check for special occasions
	if 'anonymous' in request.form:
		return "C'est fini déso !", 401
	msg = request.form['message'].strip()
	if len(msg) > 2000 or len(msg) <= 1:
		return 'Message is too long (or too short!)', 400
	with Db() as db:
		user = db.get_user_by_login(request.form['dest'])
		if not user:
			return 'User not found', 404
		send_msg(userid, user, msg, db, 'anonymous' in request.form)
	return 'OK'


@app.route('/messages/unread_count/')
@auth_required
def msg_unread_count(userid):
	with Db() as db:
		return str(db.number_of_unread_msg(userid['userid']))


@app.route('/messages/send_as_org/', methods=['POST'])
@auth_required
def msg_send_as_org(userid):
	form = request.form
	if 'token' not in form:
		return 'Missing token', 400
	msg = request.form['message'].strip()
	if len(msg) > 2000 or len(msg) <= 1:
		return 'Message is too long (or too short!)', 400
	msg_sent = 0
	with Db() as db:
		sp_user = db.get_special_user_by_key(form['token'])
		if not sp_user:
			return 'Invalid token', 400
		users_list = set([user.strip() for user in form['dest'].split(',')])
		for user in users_list:
			user = db.get_user_by_login(user)
			if user:
				msg_sent += 1
				send_msg({"login": sp_user['sp_author'], "userid": -sp_user['sp_id']}, user, msg, db,
				         'anonymous' in request.form)
	return f"OK, {msg_sent} messages sent"


@app.route('/messages/org_update/<token>', methods=['POST'])
@auth_required
def org_msg_update(token, userid):
	with Db() as db:
		user = db.get_special_user_by_key(token)
		if not user:
			return "Invalid token", 400
		form = request.form
		db.update_special_user(token, form['sp_tag'], form['sp_tag_style'], form['sp_author'])
	return redirect('/messages/org/' + user['sp_send_key'], 303)
