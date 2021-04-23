from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for, make_response


app = Flask(__name__)

@app.route('/')
def home(): 
    return render_template("index.html")

@app.route("/about")
def about():
    return app.send_static_file("about.html")

@app.route("/contact")
def contact():
    return app.send_static_file("contact.html")

@app.route("/gallery")
def gallery():
    return app.send_static_file("gallery.html")

@app.route('/error_denied')
def error_denied():
    abort(401)

@app.route('/error_internal')
def error_internal():
    abort(505)

@app.route('/error_not_found')
def error_not_found():
    abort(404)
