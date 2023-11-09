import time
from typing import Optional
from typing import Union
import requests
import math
import config


class Api:
	key: str = ""
	secret: str = ""
	rate_limit_sec = 0
	rate_limit_last_time: float = time.time()
	token: str = ""
	expire_at: int = 0
	intra: str = "https://api.intra.42.fr"

	def __init__(self, key: str, secret: str):
		self.key = key
		self.secret = secret
		self.rate_limit_last_time = time.time()
		self.rate_limit_last_time_hours = time.time()
		if not self.get_token():
			print("Failed to get token")

	def get_token(self) -> bool:
		self.add_rate()
		r = requests.post(f"{self.intra}/oauth/token", data={
			"grant_type": "client_credentials",
			"client_id": self.key,
			"client_secret": self.secret
		})
		if r.status_code == 200:
			self.token = r.json()["access_token"]
			print(self.token)
			self.expire_at = r.json()["expires_in"] + r.json()["created_at"]
			return True
		else:
			return False

	def get_access_token(self, token: str, state: str, domain: str) -> str:
		self.add_rate()
		print('->', domain)
		r = requests.post(f"{self.intra}/oauth/token", data={
			"grant_type": "authorization_code",
			"client_id": self.key,
			"client_secret": self.secret,
			"code": token,
			"state": state,
			"redirect_uri": config.redirect_url.replace('{current_domain}', domain)
		})
		if r.status_code != 200:
			return ""
		print('token', "Authorization: Bearer " + r.json()["access_token"])
		return r.json()["access_token"]

	def get_token_info(self, token: str):
		self.add_rate()
		user_info = requests.get(f"{self.intra}/oauth/token/info", headers={
			"Authorization": "Bearer " + token
		})
		if user_info.status_code != 200:
			return None
		return user_info.json()

	def get_user_id_by_token(self, token: str, state: str, domain: str) -> int:
		final_token = self.get_access_token(token, state, domain)
		if final_token == "":
			return 0
		user_info = self.get_token_info(final_token)
		if not user_info:
			return 0
		return int(user_info["resource_owner_id"])

	def add_rate(self):
		if self.rate_limit_last_time == time.time() and self.rate_limit_sec == 2:
			time.sleep(1)
			self.rate_limit_sec = 0
		if self.rate_limit_last_time != time.time():
			self.rate_limit_sec = 0
			self.rate_limit_last_time = time.time()
		self.rate_limit_sec += 1

	def get(self, url: str, params: Optional[list] = None) -> tuple[dict, int, dict]:
		if params is None:
			params = []
		if self.expire_at < time.time():
			if not self.get_token():
				return {"error": "Rate limit"}, 429, {}
		self.add_rate()
		req_url = self.intra
		if "v2/" != url[:3]:
			req_url += '/v2'
		req_url += f"{url}?{'&'.join([item for item in params])}"
		r = None
		try:
			r = requests.get(req_url, headers={
				"Authorization": f"Bearer {self.token}"
			})
		except requests.exceptions.RequestException as e:  # This is the correct syntax
			return {"error": e.__str__()}, 0, {}
		if r and r.status_code == 200:
			return r.json(), r.status_code, dict(r.headers)
		else:
			return {"error": r.text}, r.status_code, dict(r.headers)

	def get_unknown_user(self, user_name: str) -> tuple[int, dict]:
		data, status, header = self.get(f'/users/{user_name}')
		if status == 200:
			return 200, data
		return status, data

	def get_paged_locations(self, campus: int) -> tuple[int, list]:
		ret = []
		i = 1
		page_numbers = 1
		while i <= page_numbers:
			# 1200 students max
			if i > 12:
				break
			if i > 1:
				time.sleep(1.1)
			data, status, headers = self.get(f"/campus/{campus}/locations",
			                                 ["page[size]=100", "sort=begin_at",
			                                  "filter[active]=true", "filter[primary]=true",
			                                  "range[begin_at]=2023-06-10T00:00:00.000Z,2500-01-01T00:00:00.000Z",
			                                  f"page[number]={i}"])
			if status == 200:
				ret += data
				i += 1
				page_numbers = math.ceil(int(headers["X-Total"]) / int(headers["X-Per-Page"]))
			else:
				print("Could not get locations", status, data)
				return status, ret
		return 200, ret
