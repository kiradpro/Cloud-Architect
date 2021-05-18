from flask import Flask
from flask import request
from flask import render_template
from flask import abort, redirect, url_for, make_response, flash
from azuredatabase import AzureDB



app = Flask(__name__)



@app.route('/')
def index(): 
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    if request.method == "POST":
        if len(request.form['nickname']) > 2 and len(request.form['text']) > 5:
            
            res = AzureDB().azureAddData(request.form['nickname'], request.form['text'])

            flash('Form has been successfully added', category='success')
        
        else:
            flash('We found some errors in your form', category='error')

    return render_template('contact.html')


@app.route("/gallery")
def gallery():
    return render_template('gallery.html')


@app.route("/result")
def result():
    with AzureDB() as a:
        data = a.azureGetData()
    return render_template("result.html", data = data)


@app.route("/result/<int:id>/update", methods=['POST', 'GET'])
def update_user(id):
    article = AzureDB().azureGetDataid(id)
    if request.method == "POST":
        if len(request.form['nickname']) > 2 and len(request.form['text']) > 5:
            
            res = AzureDB().azureUpdateData(request.form['nickname'], request.form['text'], id)

            return redirect('/result')
        
        else:
            flash('We found some errors in your form', category='error')
    else:
        
        return render_template('result_update.html', article = article)


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

