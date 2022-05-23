#main python app

from flask import Flask, render_template, redirect, session, request, url_for
from flask_session import Session
from db import SQL
import random, json

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

def update_pages_list(user):
	return {'home':'/home','logout':'/logout'}

@app.before_request
def before_request():
	if not session['pages']:
		reset_session()

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
	session['pages']={'home':'/home','login':'/login', 'register':'/register'}
	return redirect('/')

@app.route('/')
def landing():
	reset_session()
	return redirect('/home')

@app.route("/home")
def home():
	"""Home page"""

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
					session['pages']=update_pages_list(user)
					return render_template('logged_in.html', heading='Logged in', session=session)
				return apology('password incorrect', 403)
		return apology('user does not exist', 403)

	return render_template('login.html', heading='login', session=session)

@app.route('/logout')
def logout():
	return redirect('/')

def create_user(fake_db):
	user_id=fake_db['logins'][-1]['user_id']+1
	
	if not request.form.get('class_code'):
		class_code_unique=False
		while not class_code_unique:
			class_code=''.join([random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for i in range(random.randint(4,7))])
			found=False
			for p,class_group in enumerate(fake_db['classes']):
				print(class_group)
				if class_group['class']==class_code:
					found=True
			class_code_unique=(not found)
		fake_db['classes'].append({'class':class_code,'users':[user_id]})

	else:
		class_code=request.form.get('class_code')
		for p,class_group in enumerate(fake_db['classes']):
			if class_group['class']==class_code:
				fake_db['classes'][p]['users'].append(user_id)
	
	user={"user_id":user_id,"username":request.form.get('username'),"password":request.form.get('password'),"privileges":request.form.get('user-type'),"class":class_code}
	fake_db['logins'].append(user)
	
	return fake_db,user_id

@app.route("/register", methods=['GET','POST'])
def register():

	# Forget any user_id
	reset_session()

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

		with open('static/fake_db.json') as f:
			fake_db=json.load(f)

		for user in fake_db['logins']:
			if request.form.get('username')==user['username']:
				return apology('username taken', 403)
		
		fake_db,user_id=create_user(fake_db)
		session['user']=user_id
		with open('static/fake_db.json','w') as f:
			json_object=json.dumps(fake_db)
			f.write(json_object)

		return render_template('registered.html', heading="Registered", session=session)

	return render_template('register.html', heading='Register', session=session)

@app.route('/question')
def find_question():
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)

	return render_template('question_list.html', questions=fake_db['questions'], heading="Question list", session=session)

@app.route('/question/<question_id>', methods=['GET','POST'])
def question(question_id):
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)

	try:
		question=fake_db['questions'][int(question_id)]
	except:
		return apology('invalid question id', 403)
	if question['multiple_choice']:
		question['answers']={chr(ord('a')+p):answer for p,answer in enumerate(question['answers'])}
	return render_template('question.html',heading='Question',session=session,question=question)

@app.route('/submit_question/<question_id>', methods=['POST'])
def submit_question(question_id):
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)
	try:
		question=fake_db['questions'][int(question_id)]
	except:
		return apology('invalid question id', 403)
	if question['multiple_choice']:
		correct='incorrect'
		if question['correct_answer']==request.form.get('answer'):
			correct='correct'
		return render_template('multiple_choice_mark.html', heading='Marks', session=session, correct=correct, correct_answer=question['correct_answer'], question_id=question_id)
	else:
		return render_template('short_answer_mark.html', heading='Marks', session=session, warning=False, answer=request.form.get('answer'), marking_guide=question['marking_guide'], marks=question['marks'], question_id=question_id)
'''
@app.route('/next_question', methods=['GET', 'POST'])
def next_question():
	if request.method=='POST':
		if session['']
	return redirect('/home')
'''
def set_test(questions=[]):
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)
	pass

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