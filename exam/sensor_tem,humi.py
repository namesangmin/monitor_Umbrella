from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)

# 데이터베이스 연결
db = pymysql.connect(
    host='localhost',
    user='lee',
    password='1234',
    database='practice',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# 온도/습도 데이터 저장 API
@app.route('/sensor', methods=['POST'])
def save_sensor_data():
    data = request.get_json()
    temperature = data.get('temperature')
    humidity = data.get('humidity')

    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO sensor_data (temperature, humidity) VALUES (%s, %s)"
            cursor.execute(sql, (temperature, humidity))
            db.commit()
            return jsonify({'status': 'success', 'message': 'Sensor data saved'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
