import os

from flask import Flask, session, request, flash, render_template, redirect
from flask_session import Session
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import login_user, current_user, logout_user, login_required 

app = Flask(__name__)

bcyrpt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


# calls the front page of the website
@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# register a new user
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    # Validate the form
    if request.method == 'POST' and form.validate(): 
        user_name = request.form.get(user_name)
        email=request.form.get(email)
        password=bcrypt.generate_password_hash(request.form.get(password)).decode('utf-8')
        #check if user is already in database    
        check_name = db.execute("SELECT * FROM users WHERE user_name = f'{user_name}'")
        # if so:
        if int(check_name)>0:
            flash('Username already exists! Change username.','danger')
            return render_template('register.html', form=form)
        check_email = db.execute("SELECT * FROM users WHERE email = f'{user_name}'"))
        elif int(check_email)>0:
            flash('Email already exists! Log in.','danger')
            return render_template('login.html', form=form)
        else:
            db.execute('INSERT into users (user_name, email, password) VALUES (:f'{user_name}',:f'{email}',:f'{password}')',
            {'user_name':f'{user_name}','email':f'{email}','password':f'{password}' )
            db.commit()
            flash('Account successfully created! Login to get started.','success')
        return redirect('#login', form=form)     
    return render_template('register.html', title='Register', form=form)

# login a user 
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #valid the user
    if request.method == 'POST' and form.validate():
        user_name = request.form.get(user_name)
        password=bcrypt.generate_password_hash(request.form.get(password)).decode('utf-8')
        #check the database for the user with that username
        data = db.execute("SELECT * FROM users WHERE user_name = :f'{user_name}'")
        #if no user
        if int(data)=0:
            flash('Unknown username! Kindly register first.','danger')
            return redirect('register', form=form)
        else:
            #check if harshed password in database is equal to the harshed input password for the user
            if password != f'{password}':
                flash('Incorrect password! Kindly check the password.','danger')
                return redirect('login', form=form) 
            flash('Login successfull!','success')
            return redirect(url_for('home'))
    return render_template('login.html', title='Login', form=form)

#logs out a user
@app.route('/logout')  
def logout():
    logout_user()
    return redirect(url_for('index'))

#search a book
@app.route('/home',method=['GET'])
@login_required
#GET
    #search a book using isbn/title/author
    #check if value in database
        #error no match found if result = 0
    #renders the book list match 

#get a book
@app.route('/home/book/<string:isbn>', method=['GET'])
@login_required
#return book details for that isbn
    #isbn,author,title,year_pub,reviews
    #consume api to return the reviews for the book

#make a review
@app.route('/home/book/<string:isbn>', method=['POST','GET'])
@login_required
#users to make a review with rating and content
#one review per user
#if userId already mathes a review, then flash not allowed

#review data
@app.route('/home/book/<string:isbn>', method=['GET'])
@login_required
#average rating and number of ratings from goodreads

#write an api 
@app.route('/api/<string:isbn>')
#check database if isbn exists
#if no:
    #return jsonify({'error':'None found'}),404
#else:
    #return jsonify({value required})