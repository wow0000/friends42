import os


def get_all_routes():
	ret = []
	for folder in os.listdir('./routes/'):
		if '.py' in folder and '__' not in folder and 'f_' in folder:
			ret.append(folder.replace('.py', ''))
	return ret
