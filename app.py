from flask import Flask
from maps.maps import place_to_btn, percent_to_btn
from db import Db
import routes.finder
import importlib
import routes.helpers

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

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=8080)
