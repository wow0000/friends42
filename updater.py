import requests
import time
import config

campuses = config.campuses_to_update

if __name__ == '__main__':
	while True:
		for campus in campuses:
			print(f'updating campus {campus}...')
			try:
				req = requests.get(f'http://127.0.0.1:8000/locations/{config.update_key}/{campus}')
				print(req.status_code)
			except:
				print('failed req')
			time.sleep(5)
		print('waiting 45s')
		time.sleep(45)
