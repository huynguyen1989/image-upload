import os
from flask import Flask, render_template, request, redirect, url_for, session
from config import settings
app = Flask(__name__)

# Static folders
app.config['ROOT_DIRECTORY'] = os.getcwd()
app.config['UPLOAD_FOLDER']  = "./static/uploads/"

app.secret_key = settings["APP_SECRET_KEY"]

# Import Routes 
from routes.category import init_category_routes
init_category_routes(app)
from routes.upload import init_upload_routes
init_upload_routes(app)
from routes.image import init_image_routes
init_image_routes(app)

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if 'username' in session:
            return redirect(url_for('category'))
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == '123456':
            session['username'] = username
            return redirect(url_for('category'))
        else:
            return render_template('login.html', error='Username or password do not match')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

# Run the application
if __name__ == '__main__':
    app.run(host=settings['APPLICATION_HOST'], port=int(settings['APPLICATION_PORT']), debug=bool(settings['APPLICATION_DEBUG']))