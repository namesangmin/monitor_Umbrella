from flask import Blueprint, request, jsonify
import DB.Flask_DB as DB
from datetime import datetime, timedelta

# 1. 대여 화면 버튼을 누르면 대여 페이지로 이동하는데 이때 앱에서 학번을 flask를 통해 전달
# 2. 학번이 오면 DB 조회를 해서 핸드폰이 태그될 때까지 기다림(최대 10초)
# 3. 10초 이내에 핸드폰을 태그 했을 때, uid가 읽히면서 user 테이블에 있는 학번과 uid가 일치하는지 확인함
# 4. 일치하면 빌릴 수 있고, 일치하지 않으면 정보가 일치하지 않다고 오류가 뜨게 함

rental_bp = Blueprint('rental', __name__)
@rental_bp.route('/rental', methods=['POST'])
def rental():
    student_id = request.json.get('student_id')
    
    conn = DB.get_db()
    cursor = conn.cursor(dictionary = True)
    cursor.execute("""
                   SELECT student_id 
                   FROM user
                   WHERE student_id = %s
                   """, (student_id,))
    student = cursor.fetchone()
    if not student:
        return jsonify({'error' : '사용자 없음'}), 404
    
    cursor.execute("""
                   REPLACE INTO rental_session (student_id)
                   VALUES (%s)
                   """, (student_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({'status' : 'READY', 'message' : '10초 이내에 학생증을 태그하세요.'})
    