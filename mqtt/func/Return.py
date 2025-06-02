import json
from DB_connect import connection
from datetime import datetime

def Return(payload, client):
    print(f"[Return Umbrella]: {payload}")
    try:
        data = json.loads(payload)
        umbrella_uid = data.get("uid")
        location_id = data.get("location_id")
        btn = data.get("button")  # 슬롯 번호

        conn = connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT UID, student_id, pre_return_day FROM user WHERE umbrella_uid = %s", (umbrella_uid,))
            result = cursor.fetchone()

            if not result or result["pre_return_day"] is None:
                print("대여 기록 없음")
                print("메인으로 돌아갑니다.")
                client.publish("umbrella/return/response", json.dumps({
                    "status": "FAIL",
                    "reason": "NO_RENTAL_RECORD"
                }))
                return
            student_uid = result["UID"]
            student_id = result["student_id"]
            pre_return_day = result["pre_return_day"]
            today = datetime.now()
            penalty = 7 if today > pre_return_day else 0
            
            cursor.execute("""
                           SELECT * FROM umbrella
                           WHERE location_id = %s AND button = %s
                           """, (location_id, btn))
            slot = cursor.fetchone()

            if slot:
                print("해당 슬롯에 이미 우산이 있음")
                client.publish("umbrella/return/response", json.dumps({
                    "status" : "FAIL",
                    "reason" : "SLOT_OCCUPIED"
                }))
                return
            
            cursor.execute("""
                           SELECT number FROM umbrella
                           WHERE location_id = %s
                           """, (location_id,))
            used_numbers = [row['number'] for row in cursor.fetchall()]
            for num in range(1,23):
                if num not in used_numbers:
                    assigned_number = num
                    break
                
            if assigned_number is None:
                client.publish("umbrella/return/response", json.dumps({
                    "status" : "FAIL",
                    "reason" : "NO_AVAILABLE_SLOT"
                }))
                return
            
            cursor.execute("""
                           UPDATE umbrella
                           SET location_id = %s, status = 'available', number = %s, button = %s
                           WHERE uid = %s
                           """,(location_id, assigned_number, btn, umbrella_uid))
            # 재고 증가
            cursor.execute("""
            UPDATE umbrella_count 
            SET current_count = current_count + 1 
            WHERE location_id = %s AND current_count < max_count
            """, (location_id,))
            
            # 유저 정보 업데이트 
            cursor.execute("""
            UPDATE user 
            SET coupon_count = 1, borrow_day = NULL, location_id = NULL, umbrella_id = NULL, umbrella_uid = NULL,
            pre_return_day = NULL, return_day = NULL, penalty_days = %s
            WHERE UID = %s
            """, (penalty, student_uid))

            # 로그 업데이트
            cursor.execute("""
                UPDATE rental_log
                SET return_time = %s, is_late = %s
                WHERE uid = %s AND return_time IS NULL
                ORDER BY borrow_time DESC LIMIT 1
            """, (today, penalty > 0, student_uid))
            conn.commit()
            cursor.close()
            client.publish("umbrella/return/response", json.dumps({
                "status": "SUCCESS",
                "uid": student_uid,
                "penalty": penalty
            }))
            print(f"반납 완료: {student_uid}, 연체 여부: {'있음' if penalty else '없음'}")
            print("메인으로 돌아갑니다.")
    except Exception as e:
        print("Error function return Umbrella:", e)
        client.publish("uid/response", json.dumps({"status": "FAIL"}))
    finally:
        if conn:
            conn.close()
