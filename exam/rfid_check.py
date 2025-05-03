import paho.mqtt.client as mqtt
import pymysql
import json  # JSON 응답을 위해 추가
from datetime import datetime, timedelta

# MariaDB 연결 설정
db = pymysql.connect(
    host='localhost',
    user='lee',
    password='1234',
    database='project_umbrella',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# MQTT 연결 성공 시 호출
def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT with result code", rc)
    client.subscribe("uid/check")
    client.subscribe("umbrella/rental")  
    client.subscribe("umbrella/return")  

# 메시지 수신 시 호출
def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Received UID: {payload}")
    
    if topic == "uid/check":
        func_uid_check(payload, client)
    elif topic == "umbrella/rental":
        func_rental_umbrella(payload,client)
    elif topic == "umbrella/return":
        func_return_umbrella(payload,client)
        
def func_uid_check(uid, client):
    print(f"[UID]: {uid}")
    try:
        with db.cursor() as cursor:
            # UID로 사용자 정보 조회
            sql = "SELECT name, student_id, major, coupon_count FROM user WHERE UID = %s"
            cursor.execute(sql, (uid,))
            result = cursor.fetchone()

            if result:
                print("User Found:", result)
                response = {
                    "status": "OK",
                    "name": result["name"],
                    "student_id": result["student_id"],
                    "major": result["major"],
                    "coupon_count": result["coupon_count"],
                    "uid": uid
                }
                client.publish("uid/response", json.dumps(response))
            else:
                print("User Not Found")
                client.publish("uid/response", json.dumps({"status": "FAIL"}))
    except Exception as e:
        print("DB Error:", e)
        client.publish("uid/response", json.dumps({"status": "FAIL"}))
        
def func_rental_umbrella(payload, client):
    print(f"[Rental Umbrella]: {payload}")
    try:
        data = json.loads(payload)
        uid = data.get("uid")
        location_id = data.get("location_id")
        
        with db.cursor() as cursor:         
            today = datetime.now()
            return_due = today + timedelta(days=3)
            
            # 우산 개수 감소
            sql_stock = "UPDATE umbrella_count SET current_count = current_count - 1 WHERE location_id = %s AND current_count > 0"
            cursor.execute(sql_stock, (location_id,))
            if cursor.rowcount == 0:
                print("재고 없음")
                return
            
            # 사용자 정보 업데이트
            sql_user = "UPDATE user SET coupon_count = 0, borrow_day = %s, pre_return_day = %s, return_day = NULL, penalty_days = 0 WHERE UID = %s"
            cursor.execute(sql_user, (today, return_due, uid))
            db.commit()
            
            print(f"대여 완료: {uid}, 반납 예정일: {return_due}")

    except Exception as e:
        print("Error function rental Unbrella: ", e)
        client.publish("uid/response", json.dumps({"status": "FAIL"}))

def func_return_umbrella(payload, client): 
    print(f"[Rental Umbrella]: {payload}")       
    
    try:
        data = json.loads(payload)
        uid = data.get("uid")
        location_id = data.get("location_id")

        with db.cursor() as cursor:
            sql_user = "SELECT pre_return_day FROM user WHERE UID = %s"
            cursor.execute(sql_user,(uid,))
            result = cursor.fetchone()
            if not result or result["pre_return_day"] is None:
                print("사용자 정보 없음 또는 대여 기록 없음")
                return
            
            sql_stock =  "UPDATE umbrella_count SET current_count = current_count + 1 WHERE location_id = %s AND current_count < max_count"
            cursor.execute(sql_stock,(location_id,))
            
            pre_return_day = result["pre_return_day"]
            today = datetime.now()
            penalty = 7 if today > pre_return_day else 0 # 시간이 지남 
            
            sql_update_user = "UPDATE user SET coupon_count = 1, return_day = %s, penalty_days = %s WHERE UID = %s"
            cursor.execute(sql_update_user,(today,penalty,uid))
            
            db.commit()
            print(f"반납 완료: {uid}, 연체 여부: {'있음' if penalty else '없음'}")
            
    except Exception as e:
        print("Error function return Unbrella: ", e)
        client.publish("uid/response", json.dumps({"status": "FAIL"}))
        
# MQTT 클라이언트 설정 및 연결
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
