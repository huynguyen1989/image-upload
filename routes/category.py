from flask import Flask, render_template, request, redirect, url_for, session
from models.db import connection
from markupsafe import escape

def init_category_routes(app):
    @app.route('/category', methods=['GET'])
    def category():
        if 'username' not in session:
            return redirect(url_for('login'))
        
        orderBy = request.args.get('q')
        if not orderBy:
            orderBy = 'CategoryID'
        
        sql_select_categories ="""SELECT `CategoryID`, `CategoryName`, `Description` FROM Categories c"""
        sql_select_images = """SELECT `ImageID`, `ImageURL` FROM Images i WHERE i.CategoryID IN (%s)"""
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
        return render_template('category.html', categories=categories)
    
    @app.route('/category/<path:create>', methods=['POST', 'GET'])
    def create(create):
        # show the subpath after /path/
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
                    print(f"Create Categories Errors: {str(e)}")

            
            return render_template('create_category.html')

        return render_template('create_category.html')

    @app.route('/category/delete/<int:categoryID>', methods=['POST'])
    def delete(categoryID):
        sql = """DELETE FROM `Categories` WHERE CategoryID=%s"""
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql, (request.form['CategoryID']))
                connection.commit()
            except Exception as e:
                print(f"Delete Category Errors: {str(e)}")

        return redirect(url_for('category'))
    
    @app.route('/category/edit/<int:categoryID>', methods=['POST', 'GET'])
    def edit(categoryID):
        if request.method == 'POST':
            return "Update Cat"
        sql = """SELECT `CategoryID`, `CategoryName`, `Description` FROM Categories c WHERE c.CategoryID=%s"""
        category = None
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql, (categoryID))
                category = cursor.fetchone()
            except Exception as e:
                print(f"Delete Category Errors: {str(e)}")

        print(category, '****')
        return render_template('edit_category.html', category=category)
        
    # show the post with the given id, the id is an integer