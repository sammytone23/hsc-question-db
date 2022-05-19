#main python app

from flask import Flask, render_template, redirect, session
import random
from flask_session import Session
from db import SQL

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# web_db=SQL('web_db.db')

session['pages']={'hello':'/','world':'/'}

def apology(message, code=400):
	"""Render message as an apology to user."""
	def escape(s):
		"""
		Escape special characters.

		https://github.com/jacebrowning/memegen#special-characters
		"""
		for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
						 ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
			s = s.replace(old, new)
		return s
	return render_template("apology.html", apology_message=f'{code}, '+escape(message), heading=code), code

"""
@app.route('/reset_web_db')
def reset_people():
	try open('web_db.db'):
		web_db=SQL('web_db.db')
		web_db.execute('DROP TABLE people;')
		web_db.execute('DROP TABLE questions;')
	except:
		web_db=SQL('web_db.db')
	web_db.execute('CREATE TABLE people(id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR NOT NULL, isTeacher BOOLEAN, classCode VARCHAR NOT NULL, UNIQUE(classCode));')
	web_db.execute('CREATE TABLE classes(id INTEGER PRIMARY KEY AUTOINCREMENT, class )')
	web_db.execute('CREATE TABLE questions(id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR NOT NULL, isMult BOOLEAN, multAns VARCHAR NOT NULL, hasChild BOOLEAN, hasParent BOOLEAN, hasImage BOOLEAN);')
"""

@app.after_request
def after_request(response):
	"""Ensure responses aren't cached"""
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response

@app.route("/", methods=['GET'])
def hello_world():
	"""Home page"""

	# pages={'hello':'/','world':'/'}
	return render_template('home.html', heading="This is a substituted heading", pages=pages)

@app.route('/apology')
def apologise():
	return apology


@app.route("/register", methods=['GET','POST'])
def login():

	# Forget any user_id
	session.clear()

	if request.method=='POST':
		 # Ensure username was submitted
		if not request.form.get("username"):
			return apology("must provide username", 403)

		# Ensure password was submitted
		elif not request.form.get("password"):
			return apology("must provide password", 403)

		# Ensure confirmation was submitted
		elif not request.form.get("confirmation"):
			return apology("must provide confirmation", 403)

		# Ensure password = confirmation
		elif not request.form.get("confirmation")==request.form.get("password"):
			return apology("password and confirmation must match", 403)

		""" < add person to db here >"""

	else:
		pass

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)