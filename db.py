import sqlite3
import secrets
import base64


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

	def __init__(self, filename: str):
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

	def create_table(self, sql_file: str):
		self.cur.executescript(read_file(sql_file))

	# Users
	def create_user(self, user_data: dict, campus=1):
		def god(db, field, userid: int):
			"""get old data"""
			return f"(SELECT {field} FROM {db} WHERE id = '{userid}')"

		uid = int(user_data["id"])
		active = "CURRENT_TIMESTAMP" if user_data["location"] else god('USERS', 'active', uid)
		if type(campus) != int:
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
		query = self.cur.execute("SELECT name, campus, image_medium FROM USERS WHERE name = ?", [login])
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
	def get_user_by_bookie(self, cookie: str) -> dict:
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
		"""
		:param login: Login 42 str
		:return: SELECT * FROM USERS
		"""
		query = self.cur.execute("SELECT * FROM USERS LEFT JOIN PROFILES ON PROFILES.userid = USERS.id WHERE name = ?",
		                         [str(login)])
		ret = query.fetchone()
		if api and ret is None:
			ret_status, ret_data = api.get_unknown_user(login)
			if ret_status != 200:
				return None
			self.create_user(ret_data)
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
	"""
	id             INTEGER PRIMARY KEY AUTOINCREMENT,
	project        TEXT,
	created        DATETIME DEFAULT CURRENT_TIMESTAMP,
	creator_id     INTEGER,
	campus         INTEGER,
	deadline       TEXT     DEFAULT NULL,
	progress       INTEGER  DEFAULT 0,
	quick_contacts TEXT,
	mates          TEXT,
	description    TEXT,
	contact        TEXT,
	UNIQUE (project, creator_id),
	FOREIGN KEY (creator_id) REFERENCES USERS (id)
	"""

	def get_mate_by_id(self, id):
		req = self.cur.execute("SELECT * FROM MATES WHERE id = ?", [id])
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
