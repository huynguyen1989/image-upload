from flask import Flask, render_template, request, redirect, url_for, session
from models.db import connection
from markupsafe import escape

def init_category_routes(app):
    @app.route('/api/categories', methods=['GET'])
    def getCategories():
        sql_select_categories ="""SELECT `CategoryID`, `CategoryName`, `Description` FROM Categories c ORDER BY c.`Ordering`"""
        sql_select_images = """SELECT `ImageID`, `ImageURL`, `Ordering` FROM Images i WHERE i.CategoryID = %s ORDER BY i.Ordering"""
        categories = []
        with connection.cursor() as cursor:
                try:
                    cursor.execute(sql_select_categories)
                    categories = cursor.fetchall()
                    
                    for category in categories:
                        cursor.execute(sql_select_images, (category["CategoryID"]))
                        category["UploadImages"] = cursor.fetchall()
                except Exception as e:
                    print(f"Get All Categories Errors: {str(e)}")      
        return categories
        
    @app.route('/category', methods=['GET'])
    def category():
        if 'username' not in session:
            return redirect(url_for('login'))
        
        sql_select_categories ="""SELECT `CategoryID`, `CategoryName`, `Description` FROM Categories c ORDER BY c.`Ordering`"""
        sql_select_images = """SELECT `ImageID`, `ImageURL`, `Ordering` FROM Images i WHERE i.CategoryID = %s ORDER BY i.Ordering"""
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
        return render_template('category.html', categories=categories)
    
    @app.route('/category/<path:create>', methods=['POST', 'GET'])
    def createCategory(create):
        # show the subpath after /path/
        if request.method == 'POST':
            category_name = request.form['category_name']
            category_description = request.form['category_description']
            category_ordering = request.form['category_ordering'] or 1
            
            if len(category_name) <= 0:
                return render_template('category.html', error='Name is required!')
            
            sql = """ INSERT INTO `Categories` (`CategoryName`, `Description`, `Ordering`) VALUES (%s, %s, %s) """
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql, (category_name, category_description, category_ordering))
                    connection.commit()
                except Exception as e:
                    print(f"Create Categories Errors: {str(e)}")

            
            return render_template('create_category.html')

        return render_template('create_category.html')

    @app.route('/category/delete/<int:categoryID>', methods=['POST'])
    def deleteCategory(categoryID):
        sql = """DELETE FROM `Categories` WHERE CategoryID=%s"""
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql, (request.form['CategoryID']))
                connection.commit()
            except Exception as e:
                print(f"Delete Category Errors: {str(e)}")

        return redirect(url_for('category'))
    
    @app.route('/category/edit/<int:categoryID>', methods=['POST', 'GET'])
    def editCategory(categoryID):
        if request.method == 'POST':
            category_name = request.form['category_name']
            category_description = request.form['category_description']
            category_ordering = request.form['category_ordering']
            sql_update_category= """UPDATE Categories SET CategoryName=%s, Description=%s, Ordering=%s WHERE CategoryID=%s"""
            with connection.cursor() as cursor:
                try:
                    cursor.execute(sql_update_category, (category_name, category_description, category_ordering, categoryID))
                    connection.commit()
                except Exception as e:
                    print(f"Update Category Errors: {str(e)}")
            return redirect(url_for('category'))
        
        sql_select_category = """SELECT `CategoryID`, `CategoryName`, `Description`, `Ordering` FROM Categories c WHERE c.CategoryID=%s"""
        sql_select_category_images = """SELECT i.ImageID, i.ImageURL FROM Images i WHERE i.CategoryID = %s"""
        category = None
        images = None
        with connection.cursor() as cursor:
            try:
                cursor.execute(sql_select_category, (categoryID))
                category = cursor.fetchone()
                
                cursor.execute(sql_select_category_images, (categoryID))
                images = cursor.fetchall()
            except Exception as e:
                print(f"Edit Category Errors: {str(e)}")

        return render_template('edit_category.html', category=category, images=images)
        
    # show the post with the given id, the id is an integer