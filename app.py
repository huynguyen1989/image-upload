import os
from hashlib import md5
from flask import Flask, render_template, request, redirect, url_for, session
from models.db import connection
import json



app = Flask(__name__)
app.config.from_object("config.Config")

app.config['UPLOAD_FOLDER']  = "./uploads/"

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username == 'admin' and password == '123456':
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Username or password do not match')
    return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('login'))

@app.route('/category', methods=['GET', 'POST'])
def category():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        category_name = request.form['category_name']
        category_description = request.form['category_description']
        
        if len(category_name) <= 0:
            return render_template('category.html', error='Name is required!')
        
        sql = """ INSERT INTO `Categories` (`CategoryName`, `Description`) VALUES (%s, %s) """
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql, (category_name, category_description))
                connection.commit()
            except Exception as e:
                print(f"Categories Errors: {str(e)}")
                
    return render_template('category.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'username' not in session:
        return redirect(url_for('login'))
    sql ="""SELECT `CategoryID`, `CategoryName`, `Description` FROM `Categories`"""
    categories = None
    with connection.cursor() as cursor:
            try:
                cursor.execute(sql)
                categories = cursor.fetchall()
                if not len(categories):
                    return "Category table is empty" 
            except Exception as e:
                print(f"Get All Categories Errors: {str(e)}")
    
    if request.method == 'POST':
        # check if the post request has the files part
        if not request.files['file']:
            return render_template('upload.html', error='Files is required!', categories=categories)    

        # Iterate for each file in the files List, and Save them 
        sql_insert_upload_images ="""INSERT INTO `Images` (`CategoryID`, `ImageURL`) VALUES (%s, %s);"""
        with connection.cursor() as cursor:
            try:
                files = request.files.getlist("file")        
                for file in files:
                    # Use MD5 hash for filename
                    md5_filename_hash = md5(str(file.filename).encode(), usedforsecurity=True).hexdigest()
                    filename_hash_with_extension =  f'{md5_filename_hash}.{str(file.filename).split(".")[1]}'
                    
                    saving_directory = os.path.join(app.config['UPLOAD_FOLDER'], filename_hash_with_extension) # type: ignore
                    
                    file.save(saving_directory)
                    
                    cursor.execute(sql_insert_upload_images, (request.form['category'], saving_directory))                
                    
                connection.commit()
            except Exception as e:
                print(f"Upload Images Errors: {str(e)}")
        
        return render_template('upload.html', categories=categories)
        
    return render_template('upload.html', categories=categories)

@app.route('/categories', methods=['GET'])
def categories():
    sql ="""SELECT `CategoryID`, `CategoryName`, `Description` FROM `Categories`"""
    categories = None
    with connection.cursor() as cursor:
            try:
                cursor.execute(sql)
                categories = cursor.fetchall()
                if not len(categories):
                    return "Category table is empty" 
                return categories
            except Exception as e:
                print(f"Get All Categories Errors: {str(e)}")

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
