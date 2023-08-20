from flask import Flask, redirect, url_for, request, render_template, make_response, escape, session, flash
from werkzeug.utils import secure_filename

#Initialize the Flask Application
app = Flask(__name__)
app.secret_key = 'any random string'

#Simple hello World
@app.route('/hello')
def hello_world():
    return "Hello World, Hii From Manoj"

#Example for passing variable names
@app.route('/hello/user_name/<name>')
def hello_Manoj(name):
    return "Hello %s !, How are you "  % name

@app.route('/hello/<int:post_number>')
def int_variable(post_number):
    return 'Postbox Number is %d' % post_number

#Example for building URL
@app.route('/admin/<name>')
def hello_admin(name):
    return' Hello $s !' % name

@app.route('/guest/<guest_name>')
def hello_guest(guest_name):
    return 'Hello, our guest name is %s !' % guest_name

@app.route('/hello/<name2>')
def url_build(name2):
    if name2 == 'Admin':
        return redirect(url_for('hello_admin'))
    else:
        return redirect(url_for('hello_guest',guest_name = name2))
    
#HTTP Methods Example
@app.route('/login',methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        user=request.form['nm']
        return redirect(url_for('hello_guest',guest_name = user))
    else:
        user=request.args.get('nm')
        return redirect(url_for('hello_Manoj', name=user))
    
#Example for How to use Flask Templates in Flask application
#1.Manual way of Rendering
@app.route('/template')
def index():
    str ="""
<html>
<body>
<h1>Hello World</h1>
</body>
</html>
"""
    return str
#2.render using render_template()
@app.route('/render_template')
def index2():
    return render_template('hello.html')

#Flask Frame work Static Files
@app.route('/static_file')
def index3():
    return render_template("index.html")

#Example for Sending Form Data to Templates
@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        result = request.form
        return render_template('result.html', result = result)

#Flask Framework cookies
@app.route('/cookie')
def index4():
    return render_template('setcookie.html')

@app.route('/setcookie',methods= ['POST','GET'])
def setcookie():
    if request.method == 'POST':
        user = request.form['nm']
        resp = make_response(render_template('readcookie.html'))
        resp.set_cookie('userID',user)
        return resp

@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('userID')
    return '<h1>welcome '+name+'</h1>'

#Session Object in Flask Framework
@app.route('/session')
def index5():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username +'<br>' + \
        "<b><a href = '/logout'>click here to logout</a></b>" 
    return "You are not logged in <br><a href = '/login2'></b>" + \
            "click here to log in</b></a>"

@app.route('/login2', methods = ['POST','GET'])
def login2():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index5'))
    return render_template('session.html')

@app.route('/logout')
def logout():
    #remove the username from session if it is there
    session.pop('username',None)
    return redirect(url_for('index5'))

#Flask Framework- Redirects and Errors
@app.route('/redirect')
def index6():
    return render_template('login.html')

@app.route('/login3', methods = ['POST','GET'])
def login3():
    print(request.method)
    if request.method == 'POST' and request.form['username'] =='admin':
        return redirect(url_for('success'))
    else:
        return redirect(url_for('index6'))

@app.route('/success')
def success():
    return 'logged in successfully'

#Flask Framework Message Flashing
@app.route('/flash')
def index7():
    return render_template('index7.html')

@app.route('/login4', methods = ['GET','POST'])
def login4():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
            request.form['password'] !=  'admin':
            error = 'Invalid username or password. Please try again'
        else:
            flash('you were succesfully logged in')
            flash('log out before login again')
            return redirect(url_for('index7'))
    return render_template('log_in.html', error = error)


#Flask Frame work file uploading
@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods = ['POST','GET'])
def uploader():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'


if __name__  == '__main__':
    app.run()