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