import json
from DB_connect import connection
from datetime import datetime, timedelta

def Rental(payload, client):
    print(f"[Rental Umbrella]: {payload}")
    try:
        data = json.loads(payload)
        uid = data.get("uid")
        location_id = data.get("location_id")
        btn = data.get("button")

        conn = connection()
        with conn.cursor() as cursor:
            # 유저확인
            cursor.execute("SELECT student_id FROM user WHERE uid = %s", (uid,))
            user = cursor. fetchone()
            if not user:
                print("해당 UID를 가진 사용자가 없습니다.")
                client.publish("umbrella/rental/response", json.dumps({
                    "status": "FAIL",
                    "reason" : "NO_USER"})) 
                conn.close()   
                return
            
            uid_student_id = user['student_id']
            
            # 재고 확인
            cursor.execute("""
                           SELECT current_count from umbrella_count 
                           WHERE location_id = %s
                           """,(location_id,))
            stock_info = cursor.fetchone()
            
            if not stock_info or stock_info['current_count'] <=0:
                print("재고 없음")
                client.publish("umbrella/rental/response", json.dumps({
                    "status": "FAIL",
                    "reason" : "NO_STOCK"}))    
                conn.close()
                return   
                 
            # 세션 확인(앱 or 학생증)
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
                    client.publish("umbrella/rental/response", json.dumps({
                        "status": "FAIL",
                        "reason": "SESSION_TIMEOUT"}))
                    conn.close()
                    return
                print("앱 인증 대여: 세선 확인 완료")
                cursor.execute("DELETE FROM rental_session WHERE student_id = %s", (uid_student_id,))
            else:
                print("일반 카드 태깅으로 대여")

            ##### 업데이트 #####
            # 재고 감소 업데이트
            cursor.execute("""
            UPDATE umbrella_count 
            SET current_count = current_count - 1 
            WHERE location_id = %s AND current_count > 0
            """, (location_id,))
            if cursor.rowcount == 0:
                print("재고 없음")
                client.publish("umbrella/rental/response", json.dumps({
                    "status": "FAIL",
                    "reason": "STOCK_UPDATE_FAIL"}))
                conn.close()
                return
            
            # 우산 대여여
            cursor.execute("""
                SELECT umbrella_id, uid, number FROM umbrella
                WHERE location_id = %s AND button = %s
            """, (location_id, btn))
            umbrella = cursor.fetchone() # 추후에 사용할 수 있음
            
            if not umbrella:
                client.publish("umbrella/rental/response", json.dumps({
                    "status": "FAIL",
                    "reason": "NO_UMBRELLA_IN_SLOT"
                }))
                return
            umbrella_number = umbrella["number"]
            umbrella_uid = umbrella["uid"]
            umbrella_id = umbrella["umbrella_id"]
            
            # 우산 상태 borrowed로 변경, button을 null로 변경 -> 해당 슬롯에 우산이 없음(대여 분실, 훼손)
            cursor.execute("""
                UPDATE umbrella
                SET status = 'borrowed', button = NULL
                WHERE location_id = %s AND number = %s
            """, (location_id, umbrella_number))
            
            # 유저 대여 정보 업데이트
            today = datetime.now()
            return_due = today + timedelta(days=3)
            
            cursor.execute("""
                UPDATE user 
                SET coupon_count = 0, borrow_day = %s, pre_return_day = %s,
                return_day = NULL, penalty_days = 0, location_id = %s, umbrella_id = %s, umbrella_uid = %s
                WHERE UID = %s
            """, (today, return_due, location_id, umbrella_number, umbrella_uid, uid))
            
            # 대여 로그 저장 업데이트
            cursor.execute("""
                INSERT INTO rental_log (uid, location_id, borrow_time, number, umbrella_uid)
                VALUES (%s, %s, %s, %s, %s)
            """, (uid, location_id, today, umbrella_number, umbrella_uid))
            conn.commit()
            
            # 대여 성공 응답
            client.publish("umbrella/rental/response", json.dumps({
                "status": "SUCCESS",
                "uid": uid
                #"return_due": return_due.strftime("%Y-%m-%d %H:%M:%S")
            }))
            print(f"대여 완료: {uid}, 반납 예정일: {return_due}")
            print("메인으로 돌아갑니다.")
            # conn.close()
            # cursor.close()
    except Exception as e:
        print("Error function rental Umbrella:", e)
        client.publish("uid/response", json.dumps({"status": "FAIL", 
                                                   "reason" : "EXCEPT_ERROR"}))
    finally:
        if conn:
            conn.close()