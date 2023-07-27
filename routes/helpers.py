from globals import *
from functools import wraps
from db import Db
import config
from flask import request, redirect
import json
import requests
import urllib.parse
import hashlib
import hmac
import collections
from time import time
import arrow


def proxy_images(url: str):
	if not url:
		return "/static/img/unknown.jpg"
	if 'small' in url or 'medium' in url:
		return url.replace('https://cdn.intra.42.fr/users/', 'https://friends42.fr/proxy/')
	return url.replace('https://cdn.intra.42.fr/users/', 'https://friends42.fr/proxy/resize/512/')


def auth_required(function):
	@wraps(function)
	def wrapper(*args, **kwargs):
		token = request.cookies.get('token')
		db = Db("database.db")
		userid = db.get_user_by_bookie(token)
		db.close()
		if userid == 0:
			return redirect("/redirect_42", 307)
		kwargs["userid"] = userid
		return function(*args, **kwargs)

	return wrapper


def get_position(name):
	ret = r.get("USER>" + str(name))
	return ret.decode('utf-8') if ret is not None else None


def tg_check_hash(data: dict):
	data_check_string = ""
	data_ordered = collections.OrderedDict(sorted(data.items()))
	for k, v in data_ordered.items():
		if k != 'hash':
			data_check_string += str(k) + '=' + str(v) + '\n'
	data_check_string = data_check_string.strip('\n')
	secret_key = hashlib.sha256(config.telegram_token.encode()).digest()
	new_hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
	if new_hash == data['hash']:
		return True
	if (time() - int(data['auth_date'])) > 86400:
		return False
	return False


def standard_cluster(pos):
	if pos and 'paul' in pos:
		pos = pos.replace('A', '')
		pos = pos.replace('B', '')
	return pos


def send_tg_dm(tg: dict, who: str, place: str):
	msg = tg['message'] or "🧑‍💻 |id| s'est connecté en |dump|"
	msg = msg.replace('|id|', who)
	msg = msg.replace('|dump|', place)
	msg = urllib.parse.quote(msg, safe='')
	tg_id = tg["telegram_id"]
	try:
		token = config.telegram_token
		if not token:
			print('Missing tg token')
		r = requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={tg_id}&text={msg}')
		if r.status_code != 200:
			print('[Telegram] Request failed: ', r.status_code, r.text)
	except:
		print("[Telegram] Request failed")


def create_users(db, profiles):
	for elem in profiles:
		campus = 1
		if 'campus_id' in elem:
			campus = elem['campus_id']
		if 'campus' in elem['user']:
			campus = elem['user']['campus'][0]['id']
		db.create_user(elem["user"], campus)
		if elem['user']["location"]:
			db.delete_issues(elem['user']['location'])
			old_location = r.get('USER>' + str(elem["user"]["id"]))
			if not old_location or old_location.decode("utf-8") != elem['user']['location']:
				notif_friends = db.get_notifications_friends(elem['user']['id'])
				for friend in notif_friends:
					send_tg_dm(friend['tg'], elem['user']['login'], elem['user']['location'])
			r.set('USER>' + str(elem["user"]["id"]), elem['user']["location"], ex=200)
			r.set('USER>' + str(elem["user"]["login"]), elem['user']["location"], ex=200)
	db.commit()


def get_cached_locations(campus=1):
	locations = r.get("locations/" + str(campus)) or '[]'
	cache_tab = json.loads(locations)
	return cache_tab


def locs(campus=1):
	status, data = api.get_paged_locations(campus)
	if status == 200:
		db = Db("database.db")
		create_users(db, data)
		db.close()
		r.set("locations/" + str(campus), json.dumps(data))
		return data
	else:
		return data, status


def date_relative(date):
	return arrow.get(date).humanize(locale='fr', granularity=["day"])
