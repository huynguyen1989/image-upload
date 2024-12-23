from flask import Flask, render_template, request, redirect, url_for, session
from models.db import attemptConnectToDB
from models.queries import queries_templates
import os
import uuid

def init_upload_routes(app):
    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if 'username' not in session:
            return redirect(url_for('login'))
        
        connection = attemptConnectToDB()
        cursor = connection.cursor()
        cursor.execute(queries_templates['sql_select_categories'])
        categories = cursor.fetchall()
        
        if request.method == 'POST':
            if not request.files['file']:
                return render_template('upload.html', error='Files is required!', categories=categories)    

            # Iterate for each file in the files List, and Save them 
            try:
                files = request.files.getlist("file")        
                for file in files:
                    
                    # Use uuid4 hash for filename
                    filename_hash_with_extension =  f'{uuid.uuid4()}.{str(file.filename).split(".")[1]}'
                    
                    saving_directory = os.path.join(app.config['UPLOAD_FOLDER'], str(filename_hash_with_extension)) # type: ignore
                    file.save(saving_directory)
                    
                    removed_prefix_dot = saving_directory[1:len(saving_directory)]
                    
                    cursor.execute(queries_templates['sql_create_images'], (request.form['category'], removed_prefix_dot))                
                    
                connection.commit()
            except Exception as e:
                print(f"Upload Images Errors: {str(e)}")
            
            categories = []
            cursor.execute(queries_templates['sql_select_categories'])
            categories = cursor.fetchall()
            
            for category in categories:
                cursor.execute(queries_templates['sql_select_images_by_category_id'], (category["CategoryID"]))
                category["uploaded_images"] = cursor.fetchall()
        
            return redirect(url_for('category'))
        
        return render_template('upload.html', categories=categories)

