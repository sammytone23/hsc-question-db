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
	pages={'home':'/home','logout':'/logout', 'random question':'/random', 'make a test':'/make_test'}
	if user['privileges'] in ['teacher','admin']:
		pages['question list']='/question'
		pages['check test history']='/check_test_history'
	return pages

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

@app.before_request
def before_request():
	try:
		session['pages']
	except:
		reset_session()

@app.after_request
def after_request(response):
	"""Ensure responses aren't cached"""
	response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
	response.headers["Expires"] = 0
	response.headers["Pragma"] = "no-cache"
	return response

@app.route('/session')
def display_session():
	return str(session)
	
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
		session['pages']=update_pages_list(user)

		return render_template('registered.html', heading="Registered", session=session)

	return render_template('register.html', heading='Register', session=session)

@app.route('/random')
def random_question():
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)
	return redirect('/question/'+str(random.randint(0,len(fake_db['questions'])-1)))

@app.route('/question')
def find_question():
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)

	return render_template('question_list.html', questions=fake_db['questions'], heading="Question list", session=session)

@app.route('/question/<question_id>', methods=['GET','POST'])
def question(question_id):
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)

	if len(fake_db['questions'])-1>int(question_id):
		question=fake_db['questions'][int(question_id)]
	else:
		return apology('invalid question id', 403)
	
	if question['multiple_choice']:
		question['answers']={chr(ord('a')+p):answer for p,answer in enumerate(question['answers'])}
	return render_template('question.html',heading='Question',session=session,question=question)

@app.route('/submit_question/<question_id>', methods=['POST'])
def submit_question(question_id):
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)

	if len(fake_db['questions'])-1>int(question_id):
		question=fake_db['questions'][int(question_id)]
	else:
		return apology('invalid question id', 403)
	
	if question['multiple_choice']:
		correct='incorrect'
		if question['correct_answer']==request.form.get('answer'):
			correct='correct'
		
		session['submitted'].append({'question_id':int(question_id), 'correct_answer':question['correct_answer'], 'submitted_answer':request.form.get('answer'), 'marks':1 if correct=='correct' else 0})

		return render_template('multiple_choice_mark.html', heading='Marks', session=session, correct=correct, correct_answer=question['correct_answer'], question_id=question_id)
	
	else:
		session['submitted'].append({'question_id':int(question_id), 'marking_guide':question['marking_guide'], 'submitted_answer':request.form.get('answer')})
		return render_template('short_answer_mark.html', heading='Marks', session=session, warning=False, answer=request.form.get('answer'), marking_guide=question['marking_guide'], marks=question['marks'], question_id=question_id)

@app.route('/next_question', methods=['GET', 'POST'])
def next_question():
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)
	if 'in_test' in session.keys() and session['in_test']:
		if request.method=='POST':
			test_marks=int(request.form.get('marks'))
			session['test_marks']+=test_marks
			if not fake_db['questions'][int(request.form.get('from'))]['multiple_choice']:
				session['submitted'][-1]['marks']=test_marks
		if session['test_questions']:
			next_q=session['test_questions'].pop(0)
			print(next_q)
			return redirect('/question/'+str(next_q['question_id']))
		else:
			return redirect('/test_marks')
	return redirect('/home')

@app.route('/test_marks')
def test_marks():
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)
	if 'in_test' in session.keys():
		marks=sum([int(question['marks']) for question in session['submitted']])
		test={'user':session['user'], 'marks':marks,'test':session['submitted']}
		fake_db['completed_tests'].append(test)
		with open('static/fake_db.json','w') as f:
			f.write(json.dumps(fake_db))
		session.pop('in_test', '')
		session.pop('test_questions', '')
		session.pop('test_marks', '')
		session.pop('submitted', '')
		return render_template('test_marks.html', heading="Test results", session=session, test=test, questions=fake_db['questions'])
	return redirect('/home')

def make_test(length, tags):
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)
	possible_questions=[]

	if tags:
		for question in fake_db['questions']:
			if list(set(tags) & set(question['tags'])):
				possible_questions.append(question)
	else:
		for question in fake_db['questions']:
			possible_questions.append(question)
	
	if len(possible_questions)<int(length):
		return apology('Error: not enough questions with the chosen tag'+'s' if len(tags)>1 else '')
	else:
		choices=random.choices(possible_questions,k=int(length))
		session['in_test']=True
		session['test_questions']=choices
		session['test_marks']=0
		session['submitted']=[]
		return redirect('/next_question')


@app.route('/make_test', methods=['GET','POST'])
def set_test(questions=[]):
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)
	if request.method=='POST':
		if not request.form.get('test_length'):
			return render_template('make_test.html', heading="Test yourself", session=session, tags=tags, num_questions=len(fake_db['questions']), warning="please input a test length")
		tags=request.form.getlist('tags')
		return make_test(request.form.get('test_length'),tags)
	
	tags=[]
	for question in fake_db['questions']:
		tags=list(set(tags)|set(question['tags']))

	return render_template('make_test.html', heading="Test yourself", session=session, tags=tags, num_questions=len(fake_db['questions']), warning=False)

def get_user_stats(user_id):
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)
	tests_done=0
	marks_got=0
	possible_marks=0
	for test in fake_db['completed_tests']:
		if test['user']==user_id:
			tests_done+=1
			for question in test['test']:
				marks_got+=question['marks']
				possible_marks+=fake_db['questions'][question['question_id']]['marks']
	if tests_done:
		return{'user':user_id,'test_num':tests_done,'avg_marks':round((marks_got/possible_marks)*100)}
	else:
		return{'user':user_id,'test_num':0,'avg_marks':0}


@app.route('/check_test_history', methods=['GET','POST'])
def check_test_history():
	with open('static/fake_db.json') as f:
		fake_db=json.load(f)
	if request.method=='POST':
		if request.form.get('student_id'):
			student_id=int(request.form.get('student_id'))
			if student_id>len(fake_db['logins']) or fake_db['logins'][session['user']]['privileges']=='teacher' and fake_db['logins'][int(request.form.get('student_id'))]['class']!=fake_db['logins'][session['user']]['class']:
				return render_template('student_search.html', heading="View test results", session=session, results=False, student=False, warning='That is not a student in your class')
			tests_by_student=[test for test in fake_db['completed_tests'] if test['user']==student_id]
			return render_template('student_search.html', heading="View test results", session=session, results={'user_id':student_id, 'tests':tests_by_student}, student=True, warning=False, questions=fake_db['questions'])
		user_class=fake_db['logins'][session['user']]['class']
		user_stats=[]
		for user in fake_db['logins']:
			if user['class']==user_class or user_class==0:
				user_stats.append(get_user_stats(user['user_id']))

		return render_template('student_search.html', heading="View test results", session=session, results={'class':user_class, 'users':user_stats}, student=False, warning=False)



	return render_template('student_search.html', heading="View test results", session=session, results=False, student=False, warning=False)



if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000)