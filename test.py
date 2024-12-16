import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='admin',
                             password='12345678',
                             database='SecondTask',
                             cursorclass=pymysql.cursors.DictCursor)

def migrate(): 
    with connection.cursor() as cursor:
        # Tables dict
        tables_dict = {
            "users": "CREATE TABLE IF NOT EXISTS `users3` (`id` int NOT NULL AUTO_INCREMENT,`email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL,`password` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL,PRIMARY KEY (`id`))",
            "category": "CREATE TABLE IF NOT EXISTS `users3` (`id` int NOT NULL AUTO_INCREMENT,`email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL,`password` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL,PRIMARY KEY (`id`))"
            
        }
        
        # sql= "CREATE TABLE IF NOT EXISTS `users3` (`id` int NOT NULL AUTO_INCREMENT,`email` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL,`password` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_bin NOT NULL,PRIMARY KEY (`id`))"
        
        # Iterate through to migrate tables
        for key, value in tables_dict.items():
            try: 
                cursor.execute(value)
                # print(key, value)
            except Exception as e:
                print(f"Migrate Errors: Table -> {key} - {str(e)}")
sql = """ INSERT INTO `Categories` (`CategoryName`, `Description`) VALUES (%s, %s) """        
with connection.cursor() as cursor:
    print(sql)
    cursor.execute(sql, ('aDddasd', 'asfadsfasdf'))
    connection.commit()
# migrate()

# with connection:
#     with connection.cursor() as cursor:
#         # Create a new record
#         sql = "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
#         cursor.execute(sql, ('webmaster@python.org', 'very-secret'))
        
    

#     # connection is not autocommit by default. So you must commit to save
#     # your changes.
#     connection.commit()
#     connection.close()

#     with connection.cursor() as cursor:
#         # Read a single record
#         sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
#         cursor.execute(sql, ('webmaster@python.org',))
#         result = cursor.fetchone()
#         print(result)

# connection.close()
# raise err.Error("Already closed")


from flask import Flask, send_from_directory

app = Flask(__name__)

# Define the paths to your static folders
STATIC_FOLDER_1 = 'static_folder_1'
STATIC_FOLDER_2 = 'static_folder_2'

# Route to serve files from the first static folder
@app.route('/static1/<path:filename>')
def serve_static_folder_1(filename):
    return send_from_directory(STATIC_FOLDER_1, filename)

# Route to serve files from the second static folder
@app.route('/static2/<path:filename>')
def serve_static_folder_2(filename):
    return send_from_directory(STATIC_FOLDER_2, filename)

# Example route to serve an HTML file
@app.route('/')
def index():
    return '''
    <h1>Serving Multiple Static Folders</h1>
    <ul>
        <li><a href="/static1/file1.txt">File from Static Folder 1</a></li>
        <li><a href="/static2/file2.txt">File from Static Folder 2</a></li>
    </ul>
    '''

# Run the application
if __name__ == '__main__':
    app.run(debug=True)