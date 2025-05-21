import pymysql

def get_db():
    return pymysql.connect(
        host='localhost',
        user='lee',
        password='1234',
        db='project_umbrella',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
