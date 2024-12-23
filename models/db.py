import pymysql.cursors
import pymysql
import functools
from config import settings

def auto_reconnect(func):
    @functools.wraps(func)
    def wrapper( *args, **kwargs):
        weakConnection = func( *args, **kwargs)
        try:
            # Attempting connect to DB
            return weakConnection
        except pymysql.err.DatabaseError as e:
            print(f"DB Connection error: {e}")
            weakConnection.connect(host=settings["DATABASE_HOST"],
                             user=settings["DATABASE_USER"],
                             password=settings["DATABASE_PASSWORD"],
                             database=settings["DATABASE_NAME"],
                             cursorclass=pymysql.cursors.DictCursor)
            return weakConnection
    return wrapper

@auto_reconnect
def attemptConnectToDB():
    return pymysql.connect(host=settings["DATABASE_HOST"],
                             user=settings["DATABASE_USER"],
                             password=settings["DATABASE_PASSWORD"],
                             database=settings["DATABASE_NAME"],
                             cursorclass=pymysql.cursors.DictCursor)
    

connection = attemptConnectToDB()
