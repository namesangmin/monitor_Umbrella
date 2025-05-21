import json
from DB_connect import connection

def Uid_check(uid, client):
    print(f"[UID]: {uid}")
    try:
        print("test in check rfid")
        conn = connection()
        with conn.cursor() as cursor:
            sql = "SELECT name, student_id, major, coupon_count FROM user WHERE UID = %s"
            cursor.execute(sql, (uid,))
            result = cursor.fetchone()

            if result:
                print("DB SELECT 결과:")
                print(f"이름: {result['name']}")
                print(f"학번: {result['student_id']}")
                print(f"학과: {result['major']}")
                print(f"쿠폰 수: {result['coupon_count']}")
                result["uid"] = uid
                result["status"] = "OK"
                client.publish("uid/response", json.dumps(result, ensure_ascii=False))
                # print("test in check rfid2")

            else:
                client.publish("uid/response", json.dumps({"status": "FAIL"}))
                # print("test in check rfid3")

    except Exception as e:
        print("DB Error:", e)
        client.publish("uid/response", json.dumps({"status": "FAIL"}))
