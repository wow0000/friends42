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


@app.route('/messages/')
@auth_required
def msg_default_route(userid):
	with Db() as db:
		messages = db.get_messages(userid['userid'])
		db.mark_messages_as_read(userid['userid'])
	return render_template('messages.html', me=userid['userid'],
	                       messages=anonymize_messages(messages, userid['userid']), hide_msg=True)


@app.route('/messages/send/', methods=['POST'])
@auth_required
def msg_send(userid):
	if not verify_csrf(request.form['csrf']):
		return 'Please refresh and try again', 401
	if 'message' not in request.form or not request.form['message']:
		return 'Message is empty or malformed', 400
	msg = request.form['message'].strip()
	if len(msg) > 2000 or len(msg) <= 1:
		return 'Message is too long (or too short!)', 400
	with Db() as db:
		user = db.get_user_by_login(request.form['dest'])
		if not user:
			return 'User not found', 404
		db.insert_message(userid['userid'], user['id'], msg, 1 if 'anonymous' in request.form else 0)
	return 'OK'


@app.route('/messages/unread_count/')
@auth_required
def msg_unread_count(userid):
	with Db() as db:
		return str(db.number_of_unread_msg(userid['userid']))
