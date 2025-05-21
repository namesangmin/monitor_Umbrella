import pymysql

def connection():
    return pymysql.connect(
        host='localhost',
        user='lee',
        password='1234',
        database='project_umbrella',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
