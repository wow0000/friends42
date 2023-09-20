import json
import wip_project_scraper as scraper
from time import sleep
from db import Db


def get_projects():
	with open('./projects.json') as json_file:
		projects = json.load(json_file)
	res = []
	for project in projects:
		if project['exam']:
			continue
		if len(project['project_sessions']) == 0:
			res.append({"name": project['name'], "slug": project['slug']})
		solo = True
		description = None
		for session in project['project_sessions']:
			if 'description' in session and session['description'] is not None and len(session['description']) > 5:
				description = session['description']
			if not session['solo']:
				solo = False
				break
		difficulty = 0
		if 'difficulty' in project and project['difficulty'] is not None:
			difficulty = project['difficulty']
		res.append({"id": project['id'], "name": project['name'], "slug": project['slug'], "solo": solo,
		            "description": description,
		            "xp": difficulty})
	res = sorted(res, key=lambda d: d['name'])
	return res


def find_subject_in_attachments(attachments):
	for attachment in attachments:
		if 'subject' in attachment['name'].lower():
			return attachment['link']
	return None


def get_subjects(projects):
	intra = scraper.Intra()
	intra.do_login()
	for project in projects:
		sleep(1)
		attachments = intra.get_attachments(project['slug'])
		print(f"[+] Found {len(attachments)} attachments in project {project['name']}")
		project['attachments'] = attachments
		project['subject'] = find_subject_in_attachments(attachments)
	return projects


def get_detailed_subjects():
	projects = get_projects()
	projects = get_subjects(projects)
	print(f"[+] Found {len(projects)} projects")
	with open('./projects_backup.json', 'w') as outfile:
		json.dump(projects, outfile)
	return projects


def insert_to_db(projects):
	db = Db("database.db")
	for project in projects:
		db.raw_query(
			"INSERT OR REPLACE INTO PROJECTS(id, name, slug, solo, subject, description, experience, attachements) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
			(project['id'], project['name'], project['slug'], project['solo'], project['subject'],
			 project['description'], project['xp'], json.dumps(project['attachments'])))
	db.commit()
	db.close()


def main(new_subjects=False):
	subjects = []
	if new_subjects:
		subjects = get_detailed_subjects()
	else:
		with open('./projects_backup.json') as json_file:
			subjects = json.load(json_file)
	print(f"[+] Loaded {len(subjects)} projects")
	insert_to_db(subjects)


if __name__ == "__main__":
	main()
