import pymysql
from datetime import datetime
from DB_connect import connection

def check_overdue_users():
    conn = connection()
    with conn.cursor() as cursor:
        now = datetime.now()
        sql = """
            SELECT UID, name, pre_return_day
            FROM user
            WHERE coupon_count = 0
              AND pre_return_day IS NOT NULL
              AND pre_return_day < %s
        """
        cursor.execute(sql, (now,))
        overdue_users = cursor.fetchall()

        for user in overdue_users:
            print(f"[알림] {user['name']}님({user['UID']}) 우산 반납일({user['pre_return_day']})이 지났습니다!")
