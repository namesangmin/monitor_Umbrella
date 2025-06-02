from flask import Blueprint, request, jsonify, Response
import DB.Flask_DB as DB
import requests
from datetime import date
import json

# curl -X POST http://localhost:5000/penalty
# 이 명령어로 직접 요청을 보낼 수 있음

weather_bp = Blueprint('weather', __name__)
last_run_date = {"date" : None}
def get_samcheok_weather():
    key = "36ecd38f615772379597686df2c13c9f"
    url = f"https://api.openweathermap.org/data/2.5/weather?q=Samcheok&appid={key}&units=metric&lang=kr"
    try:
        response = requests.get(url)
        data = response.json()
        weather = data['weather'][0]['main']
        #print("삼척의 날씨 상태:", data['weather'][0]['main'])
        print("현재 날씨:", weather)
        #print("온도:", data['main']['temp'], "°C")
        return weather in ['Rain', 'Snow', 'Drizzle', 'Thunderstorm']
    except Exception as e:
        print("에러 발생:", e)
        return False

@weather_bp.route('/penalty', methods=['POST'])
def penalty():
    today = date.today().isoformat()

    def json_response(obj):
        return Response(
            json.dumps(obj, ensure_ascii=False),  # 🔥 핵심
            content_type="application/json; charset=utf-8"
        )

    if last_run_date["date"] == today:
        return json_response({"status": "skipped", "message": "오늘은 이미 처리했습니다."})

    try:
        if get_samcheok_weather():
            conn = DB.get_db()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE user 
                SET penalty_days = penalty_days - 1
                WHERE penalty_days > 0
            """)
            conn.commit()
            cursor.close()
            conn.close()

            last_run_date["date"] = today
            return json_response({"status": "updated", "message": "연체일 1일 감소"})
        else:
            return json_response({"status": "no_update", "message": "오늘은 비/눈이 아니므로 연체일 차감하지 않음"})

    except Exception as e:
        return json_response({"status": "error", "message": str(e)}), 500
