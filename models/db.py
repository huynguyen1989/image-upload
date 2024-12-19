import pymysql.cursors
import pymysql
import functools

host='localhost'
user='admin'
password='12345678'
database='SecondTask'

def auto_reconnect(func):
    @functools.wraps(func)
    def wrapper( *args, **kwargs):
        weakConnection = None
        try:
            print("Attempting connect to DB")
            weakConnection = func( *args, **kwargs)
            return weakConnection
        except pymysql.err.OperationalError as e:
            print(f"DB Connection error: {e}")
            weakConnection.connect(host=host,
                             user=user,
                             password=password,
                             database=database,
                             cursorclass=pymysql.cursors.DictCursor)
            return weakConnection
    return wrapper

@auto_reconnect
def attemptConnectToDB():
    return pymysql.connect(host=host,
                             user=user,
                             password=password,
                             database=database,
                             cursorclass=pymysql.cursors.DictCursor)
    

connection = attemptConnectToDB()