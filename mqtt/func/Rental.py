import json
from DB_connect import connection
from datetime import datetime, timedelta

def Rental(payload, client):
    print(f"[Rental Umbrella]: {payload}")
    try:
        data = json.loads(payload)
        uid = data.get("uid")
        location_id = data.get("location_id")

        conn = connection()
        with conn.cursor(dictionary = True) as cursor:
            
            cursor.execute("SELECT student_id FROM user WHERE uid = %s", (uid,))
            user = cursor. fetchone()
            
            if not user:
                # print("해당 UID를 가진 사용자가 없습니다.")
                return
            
            uid_student_id = user['student_id']
            
            cursor.execute("""
                           SELECT created_at FROM rental_session 
                           WHERE student_id = %s
                           """, (uid_student_id,))
            session = cursor.fetchone()
            if session:
                session_time = session['created_at']
                if datetime.now() - session_time > timedelta(seconds=10):
                    print("시간 초과: 대여 실패")
                    cursor.execute("DELETE FROM rental_session WHERE student_id = %s", (uid_student_id,))
                    conn.commit()
                    return
                
                print("앱 인증 대여: 세선 확인 완료")
                cursor.execute("DELETE FROM rental_session WHERE student_id = %s", (uid_student_id,))
            else:
                print("일반 카드 태깅으로 대여")
            
            sql_stock = """
            UPDATE umbrella_count 
            SET current_count = current_count - 1 
            WHERE location_id = %s AND current_count > 0
            """
            cursor.execute(sql_stock, (location_id,))
            if cursor.rowcount == 0:
                # print("재고 없음")
                # print("메인으로 돌아갑니다.")
                return

            today = datetime.now()
            return_due = today + timedelta(days=3)
            sql_user = """
                UPDATE user 
                SET coupon_count = 0, borrow_day = %s, pre_return_day = %s,
                return_day = NULL, penalty_days = 0 WHERE UID = %s
            """
            cursor.execute(sql_user, (today, return_due, uid))
            
            sql_log_borrow = """
                INSERT INTO rental_log (uid, location_id, borrow_time)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql_log_borrow, (uid, location_id, today))
            conn.commit()

            # print(f"대여 완료: {uid}, 반납 예정일: {return_due}")
            # print("메인으로 돌아갑니다.")
    except Exception as e:
        # print("Error function rental Umbrella:", e)
        client.publish("uid/response", json.dumps({"status": "FAIL"}))
