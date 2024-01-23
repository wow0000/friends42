from globals import *
from functools import wraps
from db import Db
import config
from flask import request, redirect, make_response, g
import json
import requests
import urllib.parse
import hashlib
import hmac
import collections
import time
import secrets
import datetime
import arrow
import zlib


def proxy_images(url: str, light=False):
	if not url:
		return "/static/img/unknown.jpg"
	if light:
		return url.replace('https://cdn.intra.42.fr/users/', 'https://friends42.fr/proxy/resize/70/')
	if 'small' in url or 'medium' in url:
		return url.replace('https://cdn.intra.42.fr/users/', 'https://friends42.fr/proxy/')
	return url.replace('https://cdn.intra.42.fr/users/', 'https://friends42.fr/proxy/resize/512/')


def auth_required(function):
	@wraps(function)
	def wrapper(*args, **kwargs):
		token = request.cookies.get('token')
		db = Db("database.db")
		userid = db.get_user_by_bookie(token)
		if userid == 0:
			db.close()
			resp = make_response(redirect("/redirect_42", 307))
			resp.set_cookie("previous", str(request.url_rule), secure=True, max_age=None, httponly=True)
			return resp
		details = db.get_user_by_id(userid['userid'])
		is_admin = db.is_admin(userid['userid'])
		db.close()
		userid['admin'] = is_admin
		userid['campus'] = details['campus']
		userid['login'] = details['name']
		userid['image_medium'] = proxy_images(details['image_medium'])
		kwargs["userid"] = userid
		return function(*args, **kwargs)

	return wrapper


def gen_session():
	return secrets.token_urlsafe(30)


def create_hooks(app):
	@app.before_request
	def hook_session():
		if 'session' not in request.cookies:
			g.session = gen_session()
			g.set_session_cookie = True
		else:
			g.session = request.cookies['session']

	@app.after_request
	def after_request(response):
		if 'set_session_cookie' in g:
			response.set_cookie('session', g.session, None)
		return response


def create_csrf():
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
	random = secrets.token_urlsafe(20)
	msg = timestamp + "," + random + ""
	signature = hmac.new(
		(config.secret + g.session).encode('ascii'),
		msg=msg.encode('ascii'),
		digestmod=hashlib.sha256)
	return msg + ":" + signature.hexdigest()


def verify_csrf(csrf: str):
	if ':' not in csrf and ',' not in csrf:
		return False
	msg = csrf.split(':')[0]
	signature = csrf.split(':')[1]
	try:
		date = time.strptime(csrf.split(',')[0], '%Y-%m-%d-%H-%M-%S')
	except ValueError:
		return False
	if (time.time() - time.mktime(date)) > 1500:
		return False
	digest = hmac.new((config.secret + g.session).encode('ascii'), msg=msg.encode('ascii'),
	                  digestmod=hashlib.sha256).hexdigest()
	return hmac.compare_digest(digest, signature)


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
	if (time.time() - int(data['auth_date'])) > 86400:
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
		req = requests.get(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={tg_id}&text={msg}')
		if req.status_code != 200:
			print('[Telegram] Request failed: ', req.status_code, req.text)
	except requests.exceptions.RequestException as e:
		print("[Telegram] Request failed ", e)


def find_correct_campus(elem):
	if 'campus_users' in elem['user']:
		for campus_data in elem['user']['campus_users']:
			campus_id = campus_data['campus_id']
			if campus_data['is_primary']:
				return campus_id
	if 'campus_id' in elem:
		return elem['campus_id']
	if 'campus' in elem['user']:
		return elem['user']['campus'][0]['id']
	return 1


def create_users(db, profiles):
	for elem in profiles:
		campus = find_correct_campus(elem)
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
			r.set('PERM>' + str(elem["user"]["login"]), elem['user']["location"])
	db.commit()


def get_last_pos(login):
	x = r.get('PERM>' + login)
	if not x:
		return 'Unknown'
	return x.decode('utf-8')


def get_cached_locations(campus=1):
	locations = r.get("locations/" + str(campus)) or '[]'
	# locations[0] == '[':
	if locations[0] == 91 or locations[0] == '[':
		cache_tab = json.loads(locations)
	else:
		cache_tab = json.loads(zlib.decompress(locations).decode('utf-8'))
	return cache_tab


def get_last_update(campus=1):
	last_update = r.get("location_last_update/" + str(campus))
	success = r.get("location_success/" + str(campus))
	if last_update:
		return arrow.get(last_update.decode("utf-8")), success.decode("utf-8") == '1'
	return None, False


def optimize_locations(data: list[dict]) -> list[dict]:
	if len(data) == 0:
		return data
	compressed = []
	for user in data:
		tmp = user['user']
		compressed.append({
			"id": user['id'],
			"host": user['host'],
			"campus_id": user['campus_id'],
			"user": {
				"id": tmp['id'],
				"login": tmp['login'],
				"pool_month": tmp['pool_month'],
				"pool_year": tmp['pool_year'],
				"location": tmp['location'],
				"image": {
					"link": tmp['image']['link'],
					"versions": {
						"medium": tmp['image']["versions"]["medium"],
						"small": tmp['image']["versions"]["small"]
					}
				},
			}
		})
	return compressed


def is_shadow_banned(user: int, offender: int, c_db=None):
	db = c_db
	if c_db is None:
		db = Db("database.db")
	ret = db.is_shadow_banned(user, offender)
	if c_db is None:
		db.close()
	return ret


def locs(campus=1):
	status, data = api.get_paged_locations(campus)
	if status == 200:
		data = optimize_locations(data)
		db = Db("database.db")
		create_users(db, data)
		db.close()
		r.set("locations/" + str(campus), zlib.compress(json.dumps(data).encode('utf-8')))
		r.set("location_last_update/" + str(campus), arrow.now().__str__())
		r.set("location_success/" + str(campus), '1')
		return data, 200
	else:
		r.set("location_success/" + str(campus), '0')
		return data, status


def date_fmt_locale(date: str, fmt="DD/MM/YYYY HH:mm:ss"):
	if date is None:
		return arrow.now().to('local').format(fmt, locale='fr')
	return arrow.get(date).to('local').format(fmt, locale='fr')


def date_relative(date, granularity=None):
	if granularity:
		return arrow.get(date).humanize(locale='fr', granularity=granularity)
	return arrow.get(date).humanize(locale='fr')


def get_projects(group=False):
	db = Db("database.db")
	projects = []
	if group:
		projects = db.get_group_projects_list(r)
	else:
		projects = db.get_project_list(r)
	db.close()
	return projects


def get_cached_projects_with_xp():
	db = Db("database.db")
	projects = db.get_xp_projects_list(r)
	db.close()
	return projects


def find_keyword_project(keyword: str, group: False) -> list:
	db = Db("database.db")
	if group:
		projects = db.search_project_solo(keyword, False)
	else:
		projects = db.search_project(keyword)
	db.close()
	return projects


def does_group_project_exists(slug: str) -> bool:
	db = Db("database.db")
	ret = db.is_project_a_thing(slug)
	db.close()
	return ret


def get_cached_user_data(user):
	data = r.get(f"data>{user}")
	if data == "":
		return None
	if data:
		return json.loads(data)
	status, data = api.get_unknown_user(user)
	if status != 200:
		r.set(f"data>user", "", ex=2)
		return None
	data['refreshed'] = arrow.now().__str__()
	r.set(f"data>{user}", json.dumps(data), ex=43200)
	return data


def get_cursus(data, cursus_name):
	if data is None:
		return None
	for cursus in data['cursus_users']:
		if cursus['cursus']['name'] == cursus_name:
			return cursus
	return None
