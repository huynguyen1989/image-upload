import pymysql.cursors
import pymysql
import functools

def auto_reconnect(func):
    @functools.wraps(func)
    def wrapper( *args, **kwargs):
        try:
            return func( *args, **kwargs)
        except pymysql.err.OperationalError as e:
            print(f"DB Connection error: {e}")
            # self.reconnect()
            return func( *args, **kwargs)
    return wrapper

@auto_reconnect
def attemptConnectToDB():
    return pymysql.connect(host='localhost',
                             user='admin',
                             password='12345678',
                             database='SecondTask',
                             cursorclass=pymysql.cursors.DictCursor)
    

connection = attemptConnectToDB()