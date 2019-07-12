import pymysql
def getConnection():
     conn = pymysql.connect("localhost", "root", "root", "student24");
     return conn
