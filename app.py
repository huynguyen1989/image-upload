import os
from hashlib import md5
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from models.db import connection
import json

app = Flask(__name__)
app.config.from_object("config.Config")




# Import Routes 
from routes.category import init_category_routes
init_category_routes(app)
from routes.upload import init_upload_routes
init_upload_routes(app)
from routes.dashboard import init_dashboard_routes
init_dashboard_routes(app)

app.config['UPLOAD_FOLDER']  = "./static/uploads/"
# Static folders
@app.route('/vendors/<path:filename>')
def serve_static_vendors_folder(filename):
    return send_from_directory('./static/vendors/', filename)

@app.route('/js/<path:filename>')
def serve_static_js_folder(filename):
    return send_from_directory('./static/js/', filename)

@app.route('/css/<path:filename>')
def serve_static_css_folder(filename):
    return send_from_directory('./static/css/', filename)

@app.route('/assets/<path:filename>')
def serve_static_assets_folder(filename):
    return send_from_directory('./static/assets/', filename)

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
