from flask import *
import psycopg2
from functools import wraps
from time import asctime

app=Flask(__name__)
app.secret_key="has"
@app.route('/')
def welcome():
	return render_template('welcome.html')
@app.route('/home')
def home():
		conn=psycopg2.connect(database='has')
		c=conn.cursor()
		c.execute('select title,post from blog order by id desc')
		value=[dict(title=i[0],post=i[1]) for i in c.fetchall()]
		return render_template('home.html',value=value)

def login_required(test):
	@wraps(test)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return test(*args,**kwargs)
		else:
			flash('you need to login first')
			return redirect(url_for('login'))
	return wrap

@app.route('/login',methods=['GET','POST'])
def login():
    	if request.method == 'POST':
        	if request.form['username'] != 'haseeb':
                	flash('Invalid username')
        	elif request.form['password'] != '123':
                	flash('Invalid password')
        	else:
			session['logged_in']=True
        	     	flash('You were logged in')
        		return redirect(url_for('post'))
        return render_template('login.html')

@app.route('/logout')
def logout():
	session.pop('logged_in',None)
	return redirect(url_for('welcome'))


@app.route('/post')
@login_required
def post():
	return render_template('post.html')


@app.route('/home',methods=['POST'])
def submit():
	conn=psycopg2.connect(database='has')
	c=conn.cursor()
	c.execute('insert into blog (title,post) values(%s,%s)',[request.form['title'],request.form['post'],])
	conn.commit()
	c.execute('select title,post from blog order by id desc')

	value=[dict(title=i[0],post=i[1]) for i in c.fetchall()]
	return render_template('home.html',value=value)
	
app.run(debug=True)
