# Friends42

## Developer quick-start

You'll need the followings:

* Python 3
* Redis
* 42 API key
* Telegram key [optional]

```bash
git clone git@github.com:wow0000/friends42.git && cd friends42
pip install -r requirements.txt
vim config.py
python3 app.py
```

Then head to http://localhost:8080/
(You will need to add this URL to the authorized list of redirect URI on 42)

## How to add a feature

* Create your feature
*
	- You'll need to use basic features (no flask.g, middleware, etc) and adapt to the existing code style if possible.
*
	- If you are doing SQL, you must place it in the db.py file, it is forbidden to concat/str template anything to a
	  SQL request
* Create a push request with in it a list of features added, config changed and sql changes.
* Post it ! :)
* Note: I keep the right to accept or reject features, you can contact me through Discord if you'd like to be sure
  before doing the work

## How to add a campus

* Copy maps/_template.py to maps/campus_name.py
* Create a map of your own campus (Feel free to look at paris.py)
* Add your campus to maps/maps.py as an import and to the list (the number is the campus-id) (located end of file)
* Add your campus to the update list in config.py
* Create a push request with your changes and I'll come back to you quickly ! :)