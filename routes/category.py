from flask import Flask, render_template, request, redirect, url_for, session
from models.db import attemptConnectToDB
from markupsafe import escape
from models.queries import queries_templates

def init_category_routes(app):
    @app.route('/api/categories', methods=['GET'])
    def getCategories():

        categories = []

        connection = attemptConnectToDB()
        cursor = connection.cursor()
        cursor.execute(queries_templates['sql_select_categories'])
        categories = cursor.fetchall()
        
        for category in categories:
                        cursor.execute(queries_templates['sql_select_images'], (category["CategoryID"]))
                        category["UploadImages"] = cursor.fetchall()
        
        return categories
        
    @app.route('/category', methods=['GET'])
    def category():
        if 'username' not in session:
            return redirect(url_for('login'))
        
        categories = []
        
        connection = attemptConnectToDB()
        cursor = connection.cursor()
        cursor.execute(queries_templates['sql_select_categories'])
        
        categories = cursor.fetchall()
        
        for category in categories:
                        cursor.execute(queries_templates['sql_select_images_by_category_id'], (category["CategoryID"]))
                        category["UploadImages"] = cursor.fetchall()
        
        return render_template('category.html', categories=categories)
    
    @app.route('/category/<path:create>', methods=['POST', 'GET'])
    def createCategory(create):
        
        if request.method == 'POST':
            category_name = request.form['category_name']
            category_description = request.form['category_description']
            category_ordering = request.form['category_ordering'] or 1
            
            if len(category_name) <= 0:
                return render_template('category.html', error='Name is required!')
            
            connection = attemptConnectToDB()
            cursor = connection.cursor()
            cursor.execute(queries_templates['sql_create_category'], (category_name, category_description, category_ordering))
            connection.commit()
            
            return render_template('create_category.html')

        return render_template('create_category.html')

    @app.route('/category/delete/<int:categoryID>', methods=['POST'])
    def deleteCategory(categoryID):
        
        connection = attemptConnectToDB()
        cursor = connection.cursor()
        cursor.execute(queries_templates['sql_delete_cateory'], (request.form['CategoryID']))
        connection.commit()
        
        return redirect(url_for('category'))
    
    @app.route('/category/edit/<int:categoryID>', methods=['POST', 'GET'])
    def editCategory(categoryID):
        if request.method == 'POST':
            category_name = request.form['category_name']
            category_description = request.form['category_description']
            category_ordering = request.form['category_ordering']
            
            connection = attemptConnectToDB()
            cursor = connection.cursor()
            cursor.execute(queries_templates['sql_update_category'], (category_name, category_description, category_ordering, categoryID))
            connection.commit()
            
        category = None
        images = None
        
        connection = attemptConnectToDB()
        cursor = connection.cursor()
        
        cursor.execute(queries_templates['sql_select_category_by_id'], (categoryID))
        category = cursor.fetchone()
        
        cursor.execute(queries_templates['sql_select_images_by_category_id'], (categoryID))
        images = cursor.fetchall()

        return render_template('edit_category.html', category=category, images=images)