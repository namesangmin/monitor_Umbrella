import json
from DB_connect import connection
from datetime import datetime

def Return(payload, client):
    print(f"[Return Umbrella]: {payload}")
    try:
        data = json.loads(payload)
        uid = data.get("uid")
        location_id = data.get("location_id")

        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT pre_return_day FROM user WHERE UID = %s", (uid,))
            result = cursor.fetchone()

            if not result or result["pre_return_day"] is None:
                print("대여 기록 없음")
                print("메인으로 돌아갑니다.")
                return

            pre_return_day = result["pre_return_day"]
            today = datetime.now()
            penalty = 7 if today > pre_return_day else 0

            sql_stock = """
            UPDATE umbrella_count 
            SET current_count = current_count + 1 
            WHERE location_id = %s AND current_count < max_count
            """
            cursor.execute(sql_stock, (location_id,))
            
            sql_update_user = """
            UPDATE user 
            SET coupon_count = 1, borrow_day = NULL,
            pre_return_day = NULL, return_day = NULL, penalty_days = %s
            WHERE UID = %s
            """
            cursor.execute(sql_update_user, (penalty, uid))

            # 로그 업데이트
            sql_log_return = """
                UPDATE rental_log
                SET return_time = %s, is_late = %s
                WHERE uid = %s AND return_time IS NULL
                ORDER BY borrow_time DESC LIMIT 1
            """
            cursor.execute(sql_log_return, (today, penalty > 0, uid))
            
            conn.commit()

            print(f"반납 완료: {uid}, 연체 여부: {'있음' if penalty else '없음'}")
            print("메인으로 돌아갑니다.")
    except Exception as e:
        print("Error function return Umbrella:", e)
        client.publish("uid/response", json.dumps({"status": "FAIL"}))
