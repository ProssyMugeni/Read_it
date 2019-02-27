import os

from flask import Flask, session,jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


app = Flask(__name__)

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


@app.route("/")
def index():
    return "Project 1: TODO"

@app.route('/book/show')
@app.route('/book/show/')
def showBooks():
    cmd= "SELECT * FROM books"
    
    result=db.execute(cmd)
    # return result
    if result:
        return jsonify({"message":[dict(row) for row in result]})
    return jsonify({"message":"Resource not found"})

@app.route('/book/show/<int:isbn>')
@app.route('/book/show/<int:isbn>/')
def show_specific_book(isbn):
    cmd = "SELECT * FROM books WHERE books.isbn ='{}';".format(isbn)
    result=db.execute(cmd)
    if result:
        return jsonify({"Book":[dict(book) for book in result]})
    return jsonify({"message":"Resource not found"})