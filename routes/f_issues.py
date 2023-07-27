from globals import *
from routes.helpers import *
from flask import Blueprint

app = Blueprint('issues', __name__, template_folder='templates')


@app.route('/addissue/<pc>/<issue_type>')
@auth_required
def create_issue(pc, issue_type, userid):
	db = Db("database.db")
	if db.is_banned(userid['userid']):
		return 'banned', 403
	success = db.create_issue(userid['userid'], pc, int(issue_type))
	db.close()
	if not success:
		return '', 400
	return '', 200
