from flask import Blueprint, render_template
from globals import *
from routes.helpers import *
import arrow

app = Blueprint('friends', __name__, template_folder='templates')


@app.route('/friends/add/<add>')
@auth_required
def add_friend(add, userid):
	db = Db("database.db")
	friends = add.split(',')
	success = True
	for friend in friends:
		friend = friend.strip().lower()
		if len(friend) < 3:
			success = False
			continue
		add_id = db.get_user(friend)
		if add_id is None:
			status, resp = api.get_unknown_user(friend)
			if status == 200:
				create_users(db, [{'user': resp}])
			else:
				return '', 404
			add_id = {'id': resp['id']}
		if not db.add_friend(userid['userid'], add_id['id']):
			success = False
	db.close()
	return '', 200 if success else 404


@app.route('/friends/remove/<remove>')
@auth_required
def remove_friend(remove, userid):
	db = Db("database.db")
	remove_id = db.get_user(remove)
	if remove_id is None:
		return '', 404
	success = db.remove_friend(userid['userid'], remove_id['id'])
	db.close()
	return '', 200 if success else 404


@app.route('/friends/set_relation/<who>/<int:relation>')
@auth_required
def set_relation(who, relation, userid):
	db = Db("database.db")
	who_id = db.get_user(who)
	if who_id is None:
		db.close()
		return '', 404
	success = db.set_relation(userid['userid'], who_id['id'], int(relation))
	db.close()
	return '', 200 if success else 500
