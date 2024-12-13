import os
from hashlib import md5
from flask import Flask, render_template, request, redirect, url_for, session
from models.db import connection
import json

app = Flask(__name__)
app.config.from_object("config.Config")

app.config['UPLOAD_FOLDER']  = "./static/uploads/"

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

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if not 'username' in session:
        return redirect(url_for('login'))
    
    sql_select_categories ="""SELECT `CategoryID`, `CategoryName`, `Description` FROM Categories c"""
    sql_select_images = """SELECT `ImageID`, `ImageURL` FROM SecondTask.Images i WHERE i.CategoryID IN (%s)"""
    categories = []
    with connection.cursor() as cursor:
            try:
                cursor.execute(sql_select_categories)
                categories = cursor.fetchall()
                if len(categories):
                    for category in categories:
                        cursor.execute(sql_select_images, (category["CategoryID"]))
                        category["uploaded_images"] = cursor.fetchall()
            except Exception as e:
                print(f"Get All Categories Errors: {str(e)}")
    
    return render_template('dashboard.html', username=session['username'], categories=categories)

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
    sql_select_categories ="""SELECT `CategoryID`, `CategoryName`, `Description` FROM `Categories`"""
    categories = None
    with connection.cursor() as cursor:
            try:
                cursor.execute(sql_select_categories)
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
                    # md5_filename_hash = md5(str(file.filename).encode(), usedforsecurity=True).hexdigest()
                    # filename_hash_with_extension =  f'{md5_filename_hash}.{str(file.filename).split(".")[1]}'
                    
                    saving_directory = os.path.join(app.config['UPLOAD_FOLDER'], str(file.filename)) # type: ignore
                    
                    file.save(saving_directory)
                    
                    cursor.execute(sql_insert_upload_images, (request.form['category'], saving_directory))                
                    
                connection.commit()
            except Exception as e:
                print(f"Upload Images Errors: {str(e)}")
        
        sql_select_images = """SELECT `ImageID`, `ImageURL` FROM SecondTask.Images i WHERE i.CategoryID IN (%s)"""
        categories = []
        with connection.cursor() as cursor:
                try:
                    cursor.execute(sql_select_categories)
                    categories = cursor.fetchall()
                    if not len(categories):
                        return "Category table is empty" 
                    
                    for category in categories:
                        cursor.execute(sql_select_images, (category["CategoryID"]))
                        category["uploaded_images"] = cursor.fetchall()
                except Exception as e:
                    print(f"Get All Categories Errors: {str(e)}")
    
        return render_template('dashboard.html', username=session['username'], categories=categories, notification='Upload Success')
    
    return render_template('upload.html', categories=categories)

@app.route('/categories', methods=['GET'])
def categories():
    sql_select_categories ="""SELECT `CategoryID`, `CategoryName`, `Description` FROM Categories c"""
    sql_select_images = """SELECT `ImageID`, `ImageURL` FROM SecondTask.Images i WHERE i.CategoryID IN (%s)"""
    categories = []
    # uploaded_images = []
    with connection.cursor() as cursor:
            try:
                cursor.execute(sql_select_categories)
                categories = cursor.fetchall()
                # print(type(categories, '--------'))
                # import pdb; pdb.set_trace()
                if not len(categories):
                    return "Category table is empty" 
                
                for category in categories:
                    cursor.execute(sql_select_images, (category["CategoryID"]))
                    category["uploaded_images"] = cursor.fetchall()
                    # uploaded_images.append(cursor.fetchall())
            except Exception as e:
                print(f"Get All Categories Errors: {str(e)}")
    
    return render_template('categories.html', categories=categories)

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
