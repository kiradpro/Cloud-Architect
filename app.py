from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for, make_response, flash
from azuredatabase import AzureDB
from flask_dance.contrib.github import make_github_blueprint, github
import secrets
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = 'sdfdgfhkjhe48wwkdr235v4l6b70inkb6v5c'
app.secret_key = secrets.token_hex(16)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

#localhost client id: 526a3b8734481dd38821
#localhost client secret: f3fc22a19b56c6a940840662be802590429509a7
#azure client id: efd90bd904602c820fd0
#azure client secret: 8df76e152b30f3b197daf10f79f5e6041e14366e
github_blueprint = make_github_blueprint(
    client_id="efd90bd904602c820fd0",
    client_secret="8df76e152b30f3b197daf10f79f5e6041e14366e",
)
app.register_blueprint(github_blueprint, url_prefix='/login')


@app.route('/')
def index():
    if not github.authorized:
        return redirect(url_for('github.login'))
    else:
        account_info = github.get('/user')
        if account_info.ok:
            account_info_json = account_info.json()
            return render_template('index.html', account_info_json = account_info_json)
    return '<h1>Request failed!</h1>'

@app.route("/about")
def about():
    return render_template('about.html', account_info_json = github.get('/user').json())


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        if len(request.form['nickname']) > 2 and len(request.form['text']) > 5:
            
            res = AzureDB().azureAddData(request.form['nickname'], request.form['text'])

            flash('Form has been successfully added', category='success')
        
        else:
            flash('We found some errors in your form', category='error')

    return render_template('contact.html', account_info_json = github.get('/user').json())


@app.route("/gallery")
def gallery():
    return render_template('gallery.html', account_info_json = github.get('/user').json())


@app.route("/result")
def result():
    with AzureDB() as a:
        data = a.azureGetData()
    return render_template("result.html", data = data, account_info_json = github.get('/user').json())


@app.route("/result/<int:id>/update", methods=['POST', 'GET'])
def update_user(id):
    with AzureDB() as a:
        data = a.azureGetDataid(id)
    if request.method == "POST":
        if len(request.form['nickname']) > 2 and len(request.form['text']) > 5:
            
            res = AzureDB().azureUpdateData(request.form['nickname'], request.form['text'], id)

            return redirect('/result')
        
        else:
            flash('We found some errors in your form', category='error')
    else:
        
        return render_template('result_update.html', data = data, account_info_json = github.get('/user').json())


@app.route('/result/<int:id>/delete')
def delete_user(id):
    AzureDB().azureDeleteData(id)
    return redirect('/result')

    



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

