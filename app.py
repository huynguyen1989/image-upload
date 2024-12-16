import os
from hashlib import md5
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from models.db import connection
import json

app = Flask(__name__)
app.config.from_object("config.Config")

app.config['UPLOAD_FOLDER']  = "./static/uploads/"

# @app.route('/static/<path:filename>')
# def serve_static_assets_folder(filename):
#     return send_from_directory('./static/assets', filename)

from routes.category import init_category_routes
init_category_routes(app)
from routes.upload import init_upload_routes
init_upload_routes(app)
from routes.dashboard import init_dashboard_routes
init_dashboard_routes(app)

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
    app.run(host='0.0.0.0', port=5000, debug=False)
