def find_correct_campus(elem):
	def get_campus():
		if 'campus_users' in elem:
			for campus_data in elem['campus_users']:
				if campus_data['is_primary']:
					return campus_data['campus_id']
		if 'user' in elem and 'campus_users' in elem['user']:
			for campus_data in elem['user']['campus_users']:
				if campus_data['is_primary']:
					return campus_data['campus_id']
		if 'campus_id' in elem:
			return elem['campus_id']
		if 'campus' in elem['user'] and len(elem['user']['campus']) > 0:
			return elem['user']['campus'][0]['id']
		return 1
	campus = get_campus()
	# 42 network, 42 centrale
	if campus == 42 or campus == 54:
		return 1
	return campus
