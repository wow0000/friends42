import sqlite3
import secrets
import base64
import json
from routes.api_helpers import *

def read_file(filename: str):
	with open(filename, 'r') as f:
		return f.read()


def dict_factory(cursor, row) -> dict:
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d


class Db:
	cur: sqlite3.Cursor = None
	con: sqlite3.Connection = None
	is_closed = False

	def __init__(self, filename="database.db"):
		self.con = sqlite3.connect(filename)
		self.con.row_factory = dict_factory
		self.cur = self.con.cursor()

	# Management
	def initialize(self):
		self.create_table('scheme.sql')
		self.close()

	def commit(self):
		self.con.commit()

	def close(self):
		self.commit()
		self.con.close()
		self.is_closed = True

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		if not self.is_closed:
			self.close()

	def __del__(self):
		if not self.is_closed:
			self.close()

	def create_table(self, sql_file: str):
		self.cur.executescript(read_file(sql_file))

	# Users
	def create_user(self, user_data: dict, campus=1):
		def god(db, field, userid: int):
			"""get old data"""
			return f"(SELECT {field} FROM {db} WHERE id = '{userid}')"

		uid = int(user_data["id"])
		active = "CURRENT_TIMESTAMP" if user_data["location"] else god('USERS', 'active', uid)
		if not campus or type(campus) is not int:
			campus = 1
		self.cur.execute(
			'INSERT OR REPLACE INTO USERS(id, name, image, image_medium, pool, active, campus) '
			f"VALUES(?, ?, ?, ?, ?, {active}, {campus})",
			[uid, user_data["login"], user_data["image"]["link"], user_data["image"]["versions"]["medium"],
			 f"{user_data['pool_month']} {user_data['pool_year']}"])

	def get_user(self, user_id):
		query = self.cur.execute("SELECT id FROM USERS WHERE name = ?", [user_id])
		return query.fetchone()

	def get_user_by_id(self, user_id: int):
		query = self.cur.execute("SELECT name, campus, image_medium FROM USERS WHERE id = ?", [user_id])
		return query.fetchone()

	def get_user_by_login(self, login: str):
		query = self.cur.execute("SELECT id, name, campus, image_medium FROM USERS WHERE name = ?", [login])
		return query.fetchone()

	def search(self, start: str):
		req = self.cur.execute("SELECT name FROM USERS WHERE name LIKE ? LIMIT 5", [start + '%'])
		resp = req.fetchall()
		return resp

	# Notifications
	def enable_notification(self, who: int, tg_id: int, message=None):
		if who is None or tg_id is None:
			return False
		self.cur.execute(
			"INSERT OR REPLACE INTO NOTIFICATIONS_TELEGRAM(userid, telegram_id, message, enabled) VALUES (?, ?, ?, ?)",
			[who, tg_id, message, 1])
		self.commit()
		return True

	def status_notification(self, who, status: int):
		if who is None or status > 1 or status < 0:
			return False
		self.cur.execute("UPDATE NOTIFICATIONS_TELEGRAM SET enabled = ? WHERE userid = ?", [status, who])
		self.commit()
		return True

	def message_notification(self, who, msg):
		if len(msg) > 50:
			return False
		if not msg or len(msg) == 0 or msg == 'NONONON':
			msg = None
		self.cur.execute("UPDATE NOTIFICATIONS_TELEGRAM SET message = ? WHERE userid = ?", [msg, who])
		self.commit()
		return True

	def unlink_notification(self, who):
		if who is None:
			return False
		self.cur.execute("DELETE FROM NOTIFICATIONS_TELEGRAM WHERE userid = ?", [who])
		self.commit()
		return True

	def has_notifications(self, who: int):
		if who is None:
			return False
		req = self.cur.execute(
			"SELECT telegram_id, message, enabled FROM NOTIFICATIONS_TELEGRAM WHERE userid = ?", [who])
		res = req.fetchone()
		if res is None:
			return False
		return res

	# Theme
	def update_theme(self, who: int, css: str, js: str, enabled: int):
		if who is None or enabled > 1 or enabled < 0:
			return False
		if len(css) > 5000 or len(js) > 5000:
			return False
		self.cur.execute(
			"INSERT OR REPLACE INTO THEME(userid, javascript, css, enabled) VALUES (?, ?, ?, ?)",
			[who, js, css, enabled])
		self.commit()
		return True

	def get_theme(self, who):
		if who is None:
			return False
		query = self.cur.execute("SELECT * FROM THEME WHERE userid = ?", [who])
		data = query.fetchone()
		if data is None:
			return {"enabled": 0, "javascript": "", "css": ""}
		return data

	# Friends
	def add_friend(self, who: int, add_id: int):
		if who is None or add_id is None or add_id <= 0:
			return False
		self.cur.execute("INSERT OR REPLACE INTO FRIENDS(who, has) VALUES (?, ?)",
		                 [who, add_id])
		self.commit()
		return True

	def get_friends(self, who: int):
		query = self.cur.execute("SELECT * FROM FRIENDS JOIN USERS ON USERS.id = FRIENDS.has WHERE who = ?", [who])
		return query.fetchall()

	def get_notifications_friends(self, who: int):
		query = self.cur.execute(
			"SELECT * FROM FRIENDS JOIN USERS ON USERS.id = FRIENDS.has WHERE who = ? AND relation = 1", [who])
		ret = query.fetchall()
		r_ret = []
		for friend in ret:
			tg = self.has_notifications(friend['has'])
			if tg and tg['enabled'] == 1 and self.is_friend(friend['has'], who) == 1:
				r_ret.append({'id': friend['has'], 'tg': tg})
		return r_ret

	def is_friend(self, who: int, has: int) -> bool:
		req = self.cur.execute("SELECT relation FROM FRIENDS WHERE who = ? AND has = ?", [who, has])
		res = req.fetchone()
		if res is not None:
			return res['relation']
		return False

	def remove_friend(self, who: int, remove: int):
		if who is None or remove is None or remove <= 0:
			return False
		self.cur.execute("DELETE FROM FRIENDS WHERE who = ? AND has = ?", [who, remove])
		self.con.commit()
		return True

	def set_relation(self, who: int, has: int, relation: int):
		if who is None or has is None or relation < 0 or relation > 1:
			return False
		self.cur.execute("UPDATE FRIENDS SET relation = ? WHERE who = ? AND has = ?", [relation, who, has])
		self.commit()
		return True

	# Cookies
	def get_user_by_bookie(self, cookie: str):
		req = self.cur.execute('SELECT userid FROM COOKIES WHERE uuid = ?', [cookie])
		ret = req.fetchone()
		if ret is None:
			return 0
		return ret

	def get_user_cookies(self, who: int) -> list:
		if who is None:
			return []
		req = self.cur.execute('SELECT * FROM COOKIES WHERE userid = ? ORDER BY creation DESC LIMIT 25', [who])
		ret = req.fetchall()
		if ret is None:
			return []
		return ret

	def reset_user_cookies(self, who: int):
		if who is None:
			return False
		self.cur.execute('DELETE FROM COOKIES WHERE userid = ?', [who])
		self.con.commit()
		return True

	def create_cookie(self, who: int, user_agent) -> str:
		while 1:
			token = base64.b64encode(secrets.token_bytes(16)).decode('ascii')
			query = self.cur.execute("SELECT 1 FROM COOKIES WHERE uuid = ?", [token])
			ret = query.fetchone()
			if ret is not None:
				continue
			self.cur.execute("INSERT INTO COOKIES(userid, uuid, name) VALUES(?, ?, ?)", [who, token, user_agent])
			self.commit()
			return token

	def delete_cookie(self, cookie: str):
		self.cur.execute('DELETE FROM COOKIES WHERE uuid = ?', [cookie])

	# Dead PC
	def delete_issues(self, station: str):
		"""
		Needs commit afterwards
		:param station: e1r1p1
		:return:
		"""
		self.cur.execute('DELETE FROM DEAD_PC WHERE station = ?', [station])

	def already_created(self, who: int, station: str) -> bool:
		req = self.cur.execute('SELECT 1 FROM DEAD_PC WHERE issuer = ? AND station = ?', [
			who, station
		])
		res = req.fetchone()
		if res is None:
			return False
		return True

	def create_issue(self, who: int, station: str, issue: int) -> bool:
		if issue < 0 or issue > 5 or len(station) > 15 or len(station) < 6:
			return False
		if self.already_created(who, station):
			return False
		self.cur.execute('INSERT INTO DEAD_PC(issuer, station, issue) VALUES(?, ?, ?)',
		                 [who, station, issue])
		self.commit()
		return True

	def get_issues(self):
		req = self.cur.execute("SELECT station, issue, since FROM DEAD_PC WHERE solved = 0")
		return req.fetchall()

	# Profile
	def set_profile(self, who: int, info: dict) -> bool:
		if 'description' not in info or 'github' not in info or 'discord' not in info or 'website' not in info:
			return False
		if len(info["description"]) > 1500 or len(info["discord"]) > 40 or len(info['github']) > 60 or len(
				info['website']) > 30:
			return False
		if len(info['github']) > 0 and not info['github'].startswith('https://github.com/'):
			return False
		if (len(info['discord']) > 50) or (
				len(info['github']) > 0) and 'https://github.com/' not in info['github']:
			return False
		if (len(info['website']) > 0 and not (
				info['website'].startswith('http://') or info['website'].startswith('https://'))):
			return False
		self.cur.execute(
			"INSERT OR REPLACE INTO PROFILES(userid, website, github, discord, recit) VALUES (?, ?, ?, ?, ?)",
			[who, info["website"], info["github"], info["discord"], info["description"]])
		self.commit()
		return True

	def get_user_profile(self, login, api=None):
		query = self.cur.execute("SELECT * FROM USERS LEFT JOIN PROFILES ON PROFILES.userid = USERS.id WHERE name = ?",
		                         [str(login)])
		ret = query.fetchone()
		if api and ret is None:
			ret_status, ret_data = api.get_unknown_user(login)
			if ret_status != 200:
				return None
			self.create_user(ret_data, find_correct_campus(ret_data))
			return self.get_user_profile(login)
		return ret

	def get_user_profile_id(self, login):
		"""
		:param login: Login 42 id
		:return: SELECT * FROM USERS
		"""
		query = self.cur.execute(
			"SELECT * FROM USERS LEFT JOIN PROFILES ON PROFILES.userid = USERS.id WHERE USERS.id = ?", [login])
		return query.fetchone()

	# Ban list
	def is_banned(self, user_id: int) -> bool:
		query = self.cur.execute('SELECT 1 FROM BAN_lIST WHERE userid = ?', [user_id])
		return query.fetchone() is not None

	# Mates

	def get_mate_by_id(self, mate_id):
		req = self.cur.execute("SELECT * FROM MATES WHERE id = ?", [mate_id])
		return req.fetchone()

	def get_mates(self, project: str, campus: int):
		req = self.cur.execute("SELECT * FROM MATES WHERE project = ? AND campus = ? ORDER BY created DESC",
		                       [project, campus])
		return req.fetchall()

	def get_latest_mates(self, campus: int):
		req = self.cur.execute("SELECT * FROM MATES WHERE campus = ? ORDER BY created DESC LIMIT 5",
		                       [campus])
		return req.fetchall()

	def delete_mate(self, project_id):
		self.cur.execute("DELETE FROM MATES WHERE id = ?", [project_id])
		self.commit()

	def new_mate(self, creator: int, project: str, deadline: str, progress: int, quick_contacts: str, mates: str,
	             description: str, contact: str, people: int) -> int:
		if len(quick_contacts) > 35 or len(mates) > 60 or len(description) > 1000 or len(contact) > 500 or len(
				deadline) > 10:
			return 1
		if creator <= 0 or progress > 100 or progress < 0:
			return 2
		if people > 8 or people < 2:
			return 4

		creator_details = self.get_user_by_id(creator)
		if not creator_details:
			return 3

		self.cur.execute(
			"INSERT OR REPLACE INTO MATES(project, creator_id, campus, deadline, progress, quick_contacts, mates, description, contact, people) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
			[project, creator, creator_details['campus'], deadline, progress, quick_contacts, mates, description,
			 contact, people])
		self.commit()
		return 0

	# Projects

	def get_project_list(self, redis):
		rds_ret = redis.get('db_project_list')
		if rds_ret:
			return json.loads(rds_ret)
		req = self.cur.execute("SELECT * FROM PROJECTS")
		data = req.fetchall()
		redis.set('db_project_list', json.dumps(data), ex=3600)
		return data

	def get_group_projects_list(self, redis):
		rds_ret = redis.get('db_project_list_group')
		if rds_ret:
			return json.loads(rds_ret)
		req = self.cur.execute("SELECT * FROM PROJECTS WHERE solo = 0")
		data = req.fetchall()
		redis.set('db_project_list_group', json.dumps(data), ex=3600)
		return data

	def get_xp_projects_list(self, redis):
		rds_ret = redis.get('db_project_list_xp')
		if rds_ret:
			return json.loads(rds_ret)
		req = self.cur.execute("SELECT * FROM PROJECTS WHERE experience != 0")
		data = req.fetchall()
		redis.set('db_project_list_xp', json.dumps(data), ex=3600)
		return data

	def get_project(self, project_slug, redis):
		rds_ret = redis.get('db_project_name_' + project_slug)
		if rds_ret:
			return json.loads(rds_ret)
		req = self.cur.execute("SELECT * FROM PROJECTS WHERE slug = ?", [project_slug])
		data = req.fetchone()
		redis.set('db_project_name_' + project_slug, json.dumps(data), ex=3600)
		return data

	def is_project_a_thing(self, project_slug) -> bool:
		req = self.cur.execute("SELECT 1 FROM PROJECTS WHERE slug = ?", [project_slug])
		return True if req.fetchone() is not None else False

	def search_project_solo(self, keyword: str, solo: False) -> list:
		keyword = f"%{keyword}%"
		req = self.cur.execute("SELECT * FROM PROJECTS WHERE (name LIKE ? OR slug LIKE ?) AND solo = ?",
		                       [keyword, keyword, solo])
		return req.fetchall()

	def search_project(self, keyword: str) -> list:
		keyword = f"%{keyword}%"
		req = self.cur.execute("SELECT * FROM PROJECTS WHERE name LIKE ? OR slug LIKE ?",
		                       [keyword, keyword])
		return req.fetchall()

	# Update process
	def raw_query(self, query, args):
		return self.cur.execute(query, args)

	# Shadow ban
	def is_shadow_banned(self, user: int, offender: int) -> bool:
		req = self.cur.execute("SELECT 1 FROM SHADOW_BAN WHERE user = ? AND offender = ?", [user, offender])
		return req.fetchone() is not None

	def get_shadow_bans(self, offender: int) -> list:
		req = self.cur.execute("SELECT user FROM SHADOW_BAN WHERE offender = ?", [offender])
		parsed = []
		for user in req.fetchall():
			parsed.append(user['user'])
		return parsed

	def shadow_ban(self, user: int, offender: int, reason: str):
		self.cur.execute("INSERT INTO SHADOW_BAN(user, offender, reason) VALUES(?, ?, ?)", [user, offender, reason])
		self.commit()

	def remove_shadow_ban(self, ban_id: int):
		self.cur.execute("DELETE FROM SHADOW_BAN WHERE id = ?", [ban_id])
		self.commit()

	def get_all_shadow_bans(self):
		req = self.cur.execute(
			"SELECT USERS.name as offender_login, SHADOW_BAN.id as ban_id, reason, SHADOW_BAN.user AS victim FROM SHADOW_BAN LEFT JOIN USERS ON USERS.id = SHADOW_BAN.offender")
		return req.fetchall()

	# Piscines
	def insert_piscine(self, campus: int, cluster: str):
		self.cur.execute("INSERT INTO PISCINES(campus, cluster) VALUES(?, ?)", [campus, cluster])
		self.commit()

	def remove_piscine(self, piscine: int):
		self.cur.execute("DELETE FROM PISCINES WHERE id = ?", [piscine])
		self.commit()

	def get_all_piscines(self):
		req = self.cur.execute("SELECT * FROM PISCINES")
		return req.fetchall()

	def get_piscines(self, campus: int):
		req = self.cur.execute("SELECT * FROM PISCINES WHERE campus = ?", [campus])
		return req.fetchall()

	def is_piscine(self, campus: int, cluster: str):
		req = self.cur.execute("SELECT 1 FROM PISCINES WHERE campus = ? AND cluster LIKE ?", [campus, cluster])
		return True if req.fetchone() else False

	# Admin
	def is_admin(self, user_id: int):
		req = self.cur.execute("SELECT * FROM PERMISSIONS WHERE user_id = ?", [user_id])
		res = req.fetchone()
		if res is None:
			return False
		return res

	def admin_change_tag(self, user_id: int, tag: str):
		self.cur.execute("UPDATE PERMISSIONS SET tag = ? WHERE user_id = ?", [tag, user_id])
		self.commit()

	# Messages

	def insert_message(self, author, dest, content, anon=False):
		anon = 1 if anon else 0
		self.cur.execute("INSERT INTO MESSAGES(author, dest, content, anonymous) VALUES(?, ?, ?, ?)",
		                 [author, dest, content, anon])
		self.commit()

	def get_messages(self, dest):
		req = self.cur.execute(
			"SELECT MESSAGES.id, author, dest, content, anonymous, read, created, USERS_AUTHOR.name as author_login, USERS_DEST.name as dest_login FROM MESSAGES JOIN USERS AS USERS_AUTHOR ON MESSAGES.author = USERS_AUTHOR.id JOIN USERS AS USERS_DEST ON MESSAGES.dest = USERS_DEST.id WHERE dest = ? OR author = ? ORDER BY created DESC",
			[dest, dest])
		return req.fetchall()

	def mark_messages_as_read(self, dest):
		self.cur.execute("UPDATE MESSAGES SET read = 1 WHERE dest = ?", [dest])
		self.commit()

	def number_of_unread_msg(self, dest):
		req = self.cur.execute("SELECT COUNT(1) as c FROM MESSAGES WHERE dest = ? AND read = 0", [dest])
		return req.fetchone()['c']
