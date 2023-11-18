import config
from globals import *
from routes.helpers import *
from flask import Blueprint, render_template, send_from_directory

app = Blueprint('xp', __name__, template_folder='templates')


@app.route('/xp/')
@auth_required
def xp_front(userid):
	data = get_cached_user_data(userid['userid'])
	cursus = get_cursus(data, "42cursus")
	refresh = date_relative(data['refreshed']) if data is not None and 'refreshed' in data else ''
	projects = get_cached_projects_with_xp()
	# Move it to config one day
	hardcode_whitelist = ['Libft', 'get_next_line', 'ft_printf', 'Born2beroot', 'push_swap', 'minitalk', 'pipex',
	                      'so_long', 'FdF', 'fract-ol', 'minishell', 'Philosophers', 'NetPractice', 'cub3d', 'miniRT',
	                      'CPP Module 04', 'Inception', 'CPP Module 09', 'webserv', 'ft_irc', 'ft_transcendence']
	projects = sorted(projects, key=lambda d: d['experience'])
	return render_template("xp.html", data=cursus, refreshed=refresh, projectsList=projects, whitelist=hardcode_whitelist)
