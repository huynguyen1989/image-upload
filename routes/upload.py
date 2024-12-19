from flask import Flask, render_template, request, redirect, url_for, session
from models.db import connection
import os
import uuid

def init_upload_routes(app):
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
                        
                        # Use uuid4 hash for filename
                        filename_hash_with_extension =  f'{uuid.uuid4()}.{str(file.filename).split(".")[1]}'
                        
                        saving_directory = os.path.join(app.config['UPLOAD_FOLDER'], str(filename_hash_with_extension)) # type: ignore
                        file.save(saving_directory)
                        
                        removed_prefix_dot = saving_directory[1:len(saving_directory)]
                        
                        cursor.execute(sql_insert_upload_images, (request.form['category'], removed_prefix_dot))                
                        
                    connection.commit()
                except Exception as e:
                    print(f"Upload Images Errors: {str(e)}")
            
            sql_select_images = """SELECT `ImageID`, `ImageURL` FROM SecondTask.Images i WHERE i.CategoryID IN (%s)"""
            categories = []
            with connection.cursor() as cursor:
                    try:
                        cursor.execute(sql_select_categories)
                        categories = cursor.fetchall()
                        
                        for category in categories:
                            cursor.execute(sql_select_images, (category["CategoryID"]))
                            category["uploaded_images"] = cursor.fetchall()
                    except Exception as e:
                        print(f"Get All Categories Errors: {str(e)}")
        
            return redirect(url_for('category'))
        
        return render_template('upload.html', categories=categories)

