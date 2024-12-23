import json
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from models.db import attemptConnectToDB
from models.queries import queries_templates
import os

def init_image_routes(app):
    @app.route('/image', methods=['GET'])
    def image():
        if 'username' not in session:
            return redirect(url_for('login'))
        
        connection = attemptConnectToDB()
        cursor = connection.cursor()
        cursor.execute(queries_templates['sql_select_categories'])
        categories = cursor.fetchall()
        
        return render_template('image.html', categories=categories)
    
    @app.route('/image/<int:categoryID>', methods=['GET'])
    def getImageByCategoryID(categoryID):
        connection = attemptConnectToDB()
        cursor = connection.cursor()
        
        cursor.execute(queries_templates['sql_select_images_by_category_id'], (categoryID))
        images = cursor.fetchall()
        
        cursor.execute(queries_templates['sql_select_categories'])
        categories = cursor.fetchall()
        
        return render_template('image.html', categories=categories, images=images)
    
    @app.route('/image/delete/<int:categoryID>/<int:imageID>', methods=['POST'])
    def deleteImage(categoryID,imageID):
        if not 'username' in session:
            return redirect(url_for('login'))
        
        connection = attemptConnectToDB()
        cursor = connection.cursor()
        
        cursor.execute(queries_templates['sql_select_images_by_image_and_category_id'], (categoryID, imageID))
                    
        image = cursor.fetchone()
        
        os.remove(os.getcwd() + image['ImageURL'])
                    
        cursor.execute(queries_templates['sql_delete_image_by_image_and_category_id'], (categoryID, imageID))
        
        connection.commit()
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    
    @app.route('/image/ordering', methods=['POST'])
    def handleImageOrder():
        if request.is_json: 
            data = request.get_json()
            
            connection = attemptConnectToDB()
            cursor = connection.cursor()
            for image in data:
                    cursor.execute(queries_templates['sql_update_image_order'], (image["Ordering"], int(image["ImageID"]), int(image["CategoryID"])))
                        
            connection.commit()
                    
            return jsonify({'success':True}), 200, {'ContentType':'application/json'} 
        else:
            return jsonify({'message': 'Invalid request'}), 400