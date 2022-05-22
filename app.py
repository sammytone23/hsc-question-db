#main python app

from flask import Flask, render_template, redirect, session, request
import random
from flask_session import Session
from db import SQL

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# web_db=SQL('web_db.db')


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
	return render_template("apology.html", apology_message=f'{code}, '+escape(message), heading=code, session=session), code

@app.after_request
def after_request(response):
	"""Ensure responses aren't cached"""
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response

@app.route('/reset')
def reset_session():
	session.clear()
	return redirect('/')

@app.route("/", methods=['GET'])
def home():
	"""Home page"""
	if not ('pages' in session.keys()):
		session['pages']={'home':'/','reset session':'/reset'}

	# pages={'hello':'/','world':'/'}
	# print(session)
	return render_template('home.html', heading="This is a home page", session=session)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)