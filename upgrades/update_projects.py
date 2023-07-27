#!/usr/bin/python3
import requests
import json
import time

token = input('token: ')

content = []
i = 1

start = time.time()

print('[+] Starting...')
while 1:
	req = requests.get(
		f"https://api.intra.42.fr/v2/cursus/42cursus/projects?page[size]=100&filter[visible]=true&filter[exam]=false&page[number]={i}",
		headers={"Authorization": "Bearer " + token})
	if req.status_code != 200:
		break;
	if int(req.headers['X-Total']) == i:
		break
	num_proj = len(req.json())
	print(f"[?] {int(req.headers['X-Page']) * 100}/{req.headers['X-Total']}. Got {len(req.json())} projects")
	if num_proj == 0:
		break
	time.sleep(1)
	content += req.json()
	i += 1

with open('projects.json', 'w') as f:
	f.write(json.dumps(content))

time = "%.2f" % (time.time() - start)
print(f'[+] {len(content)} projects written to projects.json in {time}s')
