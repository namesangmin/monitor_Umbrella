from flask import Flask, request, jsonify, render_template
import pymysql

app = Flask(__name__)

# DB 연결
db = pymysql.connect(
    host='localhost',
    user='lee',
    password='1234',
    database='practice',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# HTML 테이블로 보여주기
@app.route('/view', methods=['GET'])
def view_sensor_data():
    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM sensor_data ORDER BY id ASC"
            cursor.execute(sql)
            result = cursor.fetchall()
            return render_template('sensor_table.html', sensors=result)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
