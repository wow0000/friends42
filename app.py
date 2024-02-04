from flask import Flask, g
from maps.maps import place_to_btn, percent_to_btn
from db import Db
import sentry_sdk
import config
import routes.finder
import importlib
import routes.helpers

if config.sentry and config.sentry != '':
	sentry_sdk.init(
		dsn=config.sentry,
		traces_sample_rate=config.sentry_traces_sample_rate,
		profiles_sample_rate=config.sentry_profiles_sample_rate
	)

db = Db("database.db")
db.initialize()

app = Flask(__name__)

for route in routes.finder.get_all_routes():
	app.register_blueprint(importlib.import_module('routes.' + route, package=None).app)

app.jinja_env.globals.update(len=len)
app.jinja_env.globals.update(enumerate=enumerate)
app.jinja_env.globals.update(place_to_btn=place_to_btn)
app.jinja_env.globals.update(percent_to_btn=percent_to_btn)
app.jinja_env.globals.update(proxy_images=routes.helpers.proxy_images)
app.jinja_env.globals.update(date_relative=routes.helpers.date_relative)
app.jinja_env.globals.update(date_fmt_locale=routes.helpers.date_fmt_locale)
app.jinja_env.globals.update(create_csrf=routes.helpers.create_csrf)
app.jinja_env.globals.update(verify_csrf=routes.helpers.verify_csrf)
app.jinja_env.globals.update(g=g)

routes.helpers.create_hooks(app)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8080)
