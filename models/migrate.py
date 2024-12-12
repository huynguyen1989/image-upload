import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='admin',
                             password='12345678',
                             database='SecondTask',
                             cursorclass=pymysql.cursors.DictCursor)

def migrate(): 
    with connection.cursor() as cursor:
        # Tables DDL
        tables_dict = {
            "category": """
            CREATE TABLE `Categories` (
            `CategoryID` int NOT NULL AUTO_INCREMENT,
            `CategoryName` varchar(255) NOT NULL,
            `Description` longtext,
            PRIMARY KEY (`CategoryID`)
            ) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """,
            "image": """
            CREATE TABLE `Images` (
            `ImageID` int NOT NULL AUTO_INCREMENT,
            `CategoryID` int NOT NULL,
            `ImageURL` varchar(255) NOT NULL,
            PRIMARY KEY (`ImageID`),
            KEY `UploadCategoryID` (`CategoryID`),
            CONSTRAINT `Images_Categories_FK` FOREIGN KEY (`CategoryID`) REFERENCES `Categories` (`CategoryID`) ON DELETE CASCADE ON UPDATE CASCADE
            ) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
            """
        }
        
        # Iterate through to migrate tables
        for key, value in tables_dict.items():
            try: 
                cursor.execute(value)
            except Exception as e:
                print(f"Migrate Errors: Table -> {key} - {str(e)}")
        

migrate()

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