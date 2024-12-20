import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from models.db import connection
import os

def init_image_routes(app):
    @app.route('/image', methods=['GET'])
    def image():
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
        
        return render_template('image.html', categories=categories)
    
    @app.route('/image/<int:categoryID>', methods=['GET'])
    def getImageByCategoryID(categoryID):
        sql_select_images ="""SELECT `CategoryID`, `ImageID`, `ImageURL`, `Ordering` FROM Images i WHERE i.CategoryID = %s"""
        sql_select_categories ="""SELECT `CategoryID`, `CategoryName`, `Description` FROM `Categories`"""
        images = None
        categories = None
        with connection.cursor() as cursor:
                try:
                    cursor.execute(sql_select_images, (categoryID))
                    images = cursor.fetchall()
                    
                    cursor.execute(sql_select_categories)
                    categories = cursor.fetchall()
                except Exception as e:
                    print(f"Get Images By CategoryID Errors: {str(e)}")
        return render_template('image.html', categories=categories, images=images)
    
    @app.route('/image/delete/<int:categoryID>/<int:imageID>', methods=['POST'])
    def deleteImage(categoryID,imageID):
        if not 'username' in session:
            return redirect(url_for('login'))
        
        sql_select_images = """SELECT `CategoryID`, `ImageID`, `ImageURL` FROM Images i WHERE i.CategoryID = %s AND i.ImageID = %s"""
        sql_delete_image = """DELETE FROM Images i WHERE i.CategoryID = %s AND i.ImageID = %s"""
        with connection.cursor() as cursor:
                try:
                    cursor.execute(sql_select_images, (categoryID, imageID))
                    
                    image = cursor.fetchone()
                    
                    os.remove(os.getcwd() + image['ImageURL'])
                    
                    cursor.execute(sql_delete_image, (categoryID, imageID))
                    
                    connection.commit()
                    return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
                except Exception as e:
                    print(f"Delete Image Errors: {str(e)}")
        
        return render_template('dashboard.html', username=session['username'], categories=categories)
    
    @app.route('/image/ordering', methods=['POST'])
    def handleImageOrder():
        if request.is_json: 
            data = request.get_json()
            
            sql_update_image_order = """UPDATE `Images` SET `Ordering`=%s WHERE `ImageID`=%s AND `CategoryID` =%s"""
            with connection.cursor() as cursor:
                try:
                    for image in data:
                        cursor.execute(sql_update_image_order, (image["Ordering"], int(image["ImageID"]), int(image["CategoryID"])))
                        
                    connection.commit()
                    
                    return jsonify({'success':True}), 200, {'ContentType':'application/json'} 
                except Exception as e:
                    print(f"Update Image Ordering Errors: {str(e)}")
        else:
            return jsonify({'message': 'Invalid request'}), 400
        
    @app.route('/api/data', methods=['POST'])
    def handle_data():
        if request.is_json: 
            data = request.get_json()
            # Process the data
            print(data, '****')
            print(type(data), '**type**')
            # print(data["app_package_name"], '****')
            return data, 200
        else:
            return jsonify({'message': 'Invalid request'}), 400
