from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for, make_response


app = Flask(__name__)


@app.route('/')
def index(): 
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact")
def contact():
    return render_template('contact.html')


@app.route("/gallery")
def gallery():
    return render_template('gallery.html')


@app.route('/error_denied')
def error_denied():
    abort(401)


@app.route('/error_internal')
def error_internal():
    abort(505)


@app.route('/error_not_found')
def error_not_found():
    abort(404)


if __name__ == "__main__":
    app.run(debug=True)

