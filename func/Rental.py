import json
from DB_connect import connection
from datetime import datetime, timedelta

def Rental(payload, client):
    print(f"[Rental Umbrella]: {payload}")
    try:
        data = json.loads(payload)
        uid = data.get("uid")
        location_id = 1 #data.get("location_id")

        conn = connection()
        with conn.cursor() as cursor:
            sql_stock = """
            UPDATE umbrella_count 
            SET current_count = current_count - 1 
            WHERE location_id = %s AND current_count > 0
            """
            cursor.execute(sql_stock, (location_id,))
            if cursor.rowcount == 0:
                print("재고 없음")
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

            print(f"대여 완료: {uid}, 반납 예정일: {return_due}")
    except Exception as e:
        print("Error function rental Umbrella:", e)
        client.publish("uid/response", json.dumps({"status": "FAIL"}))
