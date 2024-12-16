from flask import Flask, render_template, request, redirect, url_for, session
from models.db import connection

def init_dashboard_routes(app):
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
