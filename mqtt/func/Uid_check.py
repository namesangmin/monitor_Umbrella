import json
from DB_connect import connection


# 학생증인지.. 우산에 있는 카드인지 파악하고 리턴을 해줘
def Uid_check(payload, client):
    data = json.loads(payload)
    uid = data.get("uid")
    location_id = data.get("location_id")
    print(f"[UID]: {uid}")
    try:
        conn = connection()
        with conn.cursor() as cursor:
            # 1. 학생증, 기기일 때때
            cursor.execute("SELECT name, student_id, major, coupon_count FROM user WHERE UID = %s", (uid,))
            user = cursor.fetchone()

            if user:
                cursor.execute("""SELECT current_count FROM umbrella_count
                               WHERE location_id = %s
                               """,(location_id,))
                stock = cursor.fetchone()
                current_count = stock['current_count'] if stock else 0
                
                user["uid"] = uid
                user["status"] = "USER"
                user["current_count"] = current_count
                client.publish("uid/response", json.dumps(user, ensure_ascii=False))
                conn.close()
                return
                
            # 2. 우산에 있는 카드일 때
            sql__umbrella_uid = "SELECT name, student_id, major FROM user WHERE umbrella_uid = %s"
            cursor.execute(sql__umbrella_uid,(uid,))
            umbrella = cursor.fetchone()
            
            if umbrella:
                umbrella["uid"] = uid
                umbrella["status"] = "UMBRELLA"
                client.publish("uid/response", json.dumps(umbrella, ensure_ascii=False))
                conn.close()
                return

            client.publish("uid/response", json.dumps({
                "status": "FAIL",
                "reason" : "NO_SELECT"}))
            conn.close()

    except Exception as e:
        print("DB Error:", e)
        client.publish("uid/response", json.dumps({
            "status": "FAIL",
            "reason" : "DB_Error"}))