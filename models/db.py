import pymysql.cursors

# Single Connect to the database
connection = pymysql.connect(host='localhost',
                             user='admin',
                             password='12345678',
                             database='SecondTask',
                             cursorclass=pymysql.cursors.DictCursor)
