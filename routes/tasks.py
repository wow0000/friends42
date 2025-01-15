from db import Db
from globals import api
import queue
import threading
import uuid
import time
import sqlite3

import_queue = queue.Queue()
task_status = {}
task_lock = threading.Lock()
IMPORT_TIMEOUT = 300

def execute_with_retry(cursor, query, params=(), retries=5, delay=0.1):
	for attempt in range(retries):
		try:
			cursor.execute(query, params)
			return
		except sqlite3.OperationalError as e:
			if 'database is locked' in str(e):
				time.sleep(delay)
			else:
				raise
	raise sqlite3.OperationalError("Database is locked after multiple retries.")

def import_worker():
	while True:
		task_id, data, userid = import_queue.get()
		start_time = time.time()
		try:
			with task_lock:
				task_status[task_id] = 'En cours'
			db = Db("database.db")
			user_data = data.get('user')
			friends = data.get('friends')
			theme = data.get('theme')
			with db.transaction():
				profile_info = {
					'website': user_data['website'],
					'github': user_data['github'],
					'discord': user_data['discord'],
					'description': user_data['recit']
				}
				existing_profile = db.cur.execute(
					"SELECT website, github, discord, recit FROM PROFILES WHERE userid = ?", 
					[userid['userid']]
				).fetchone()
				if existing_profile:
					if (existing_profile['website'] != profile_info['website'] or
						existing_profile['github'] != profile_info['github'] or
						existing_profile['discord'] != profile_info['discord'] or
						existing_profile['recit'] != profile_info['description']):
						db.set_profile(userid['userid'], profile_info)
				else:
					db.set_profile(userid['userid'], profile_info)
				existing_friends = db.get_friends(userid['userid'])
				existing_friend_ids = set(friend['has'] for friend in existing_friends)

				new_friends_to_add = []
				for friend in friends:
					if time.time() - start_time > IMPORT_TIMEOUT:
						raise TimeoutError("Importation annulée en raison d'un dépassement du délai.")
					friend_username = friend.get('name')
					if not friend_username:
						continue
					friend_record = db.get_user(friend_username)
					if not friend_record:
						status, resp = api.get_unknown_user(friend_username)
						if status == 200:
							db.create_user(resp, campus=resp.get('campus', 1))
							friend_record = db.get_user(friend_username)
							if not friend_record:
								continue
						else:
							continue
					friend_id = friend_record['id']
					if friend_id not in existing_friend_ids:
						new_friends_to_add.append(friend_id)
						existing_friend_ids.add(friend_id)
				if new_friends_to_add:
					friend_tuples = [(userid['userid'], friend_id) for friend_id in new_friends_to_add]
					try:
						db.cur.executemany("INSERT OR REPLACE INTO FRIENDS(who, has) VALUES (?, ?)", friend_tuples)
					except sqlite3.OperationalError as e:
						for tuple_entry in friend_tuples:
							execute_with_retry(db.cur, "INSERT OR REPLACE INTO FRIENDS(who, has) VALUES (?, ?)", tuple_entry)
				theme_enabled = theme.get('enabled', 0)
				theme_js = theme.get('javascript', '')
				theme_css = theme.get('css', '')
				existing_theme = db.get_theme(userid['userid'])
				if existing_theme:
					if (existing_theme['css'] != theme_css or
						existing_theme['javascript'] != theme_js or
						existing_theme['enabled'] != theme_enabled):
						db.update_theme(userid['userid'], theme_css, theme_js, int(theme_enabled))
				else:
					db.update_theme(userid['userid'], theme_css, theme_js, int(theme_enabled))
			with task_lock:
				task_status[task_id] = 'Terminé'
			db.close()
		except TimeoutError as te:
			print(f"Importation annulée: {te}")
			with task_lock:
				task_status[task_id] = 'Annulée (timeout)'
			db.conn.rollback()
		except Exception as e:
			print(f"Erreur lors de l'importation: {e}")
			with task_lock:
				task_status[task_id] = f'Erreur: {e}'
			db.conn.rollback()
		finally:
			import_queue.task_done()

worker_thread = threading.Thread(target=import_worker, daemon=True)
worker_thread.start()
