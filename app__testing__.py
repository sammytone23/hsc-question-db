#main python app

from flask import Flask, render_template, redirect, session, request
import random
from flask_session import Session
from db import SQL
import json

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
	return render_template("apology.html", apology_message=f'{code}, '+escape(message), heading='Error: '+str(code), session=session), code

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

@app.route("/")
def home():
	"""Home page"""
	if not ('pages' in session.keys()):
		session['pages']={'home':'/','reset session':'/reset','add':'/add_page'}

	# pages={'hello':'/','world':'/'}
	# print(session)
	return render_template('home.html', heading="This is a home page", session=session)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=="POST":

        if not request.form.get('username'):
            return apology('must provide username', 403)
        username=request.form.get('username')
        if not request.form.get('password'):
            return apology('must provide password', 403)
        password=request.form.get('password')

        with open('static/fake_db.json') as f:
            fake_db=json.load(f)
            for user in fake_db['logins']:
                if user['username']==username:
                    if user['password']==password:
                        session['user']=user['user_id']
                        return render_template('logged_in.html', heading='Logged in', session=session)
                    return apology('password incorrect', 403)
            return apology('user does not exist', 403)

    return render_template('login.html', heading='login', session=session)




"""
!!! Testing pages, leave commented out !!!

def make_page(route, title="Title", methods=['GET'], file=None, **kwargs):
    if request.method not in methods:
        return apology("method not allowed", 403)
    if not file:
        return render_template()

@app.route('/apology')
def apologise():
	return apology('get apologised')

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

		\""" < add person to db here >\"""

	else:
		pass

@app.route('/is_correct', methods=['POST'])
def is_correct():
	if not request.form.get('thing'):
		return apology("must input thing", code=403)
	if request.form.get('thing')=='correct':
		session.pop('reply', None)
		session['pages']['win']='/win'
		session['win']=True
	else:
		session['reply']='that input is not correct'
	return redirect('/')

@app.route('/win')
def win():
	if 'win' not in session.keys() or not session['win']:
		return redirect('/')
	return render_template('win.html', heading='You Won!', session=session)

@app.route('/add_page', methods=['GET', 'POST'])
def add_page():
	print(request)
	if request.method=='POST':
		if not request.form.get('page'):
			return apology("must input page", code=403)
		session['pages'][request.form.get('page')]='/'
	
	return render_template('add.html', heading="add a fake page", session=session)
"""

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)