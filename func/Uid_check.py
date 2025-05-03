import json
from DB_connect import connection

def Uid_check(uid, client):
    print(f"[UID]: {uid}")
    try:
        conn = connection()
        with conn.cursor() as cursor:
            sql = "SELECT name, student_id, major, coupon_count FROM user WHERE UID = %s"
            cursor.execute(sql, (uid,))
            result = cursor.fetchone()

            if result:
                result["uid"] = uid
                result["status"] = "OK"
                client.publish("uid/response", json.dumps(result))
            else:
                client.publish("uid/response", json.dumps({"status": "FAIL"}))
    except Exception as e:
        print("DB Error:", e)
        client.publish("uid/response", json.dumps({"status": "FAIL"}))
