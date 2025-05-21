from flask import Blueprint, request, jsonify
import DB.Flask_DB as DB


login_bp = Blueprint('login', __name__)
@login_bp.route('/login', methods = ['POST'])
def login():
    data = request.get_json()
    student_id = data.get('student_id')
    password = data.get('password')
    
    if not student_id or not password:
        return jsonify({'error' : '학번 또는 비밀번호가 누락되었습니다.'}), 400
    
    conn = DB.get_db()
    cursor = conn.cursor(dictionary = True)
    cursor.execute("""
                   SELECT * FROM student_info
                   WHERE student_id = %s AND password = %s
                   """,(student_id, password))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not user:
        return jsonify({'error' : '로그인 실패'}), 401
    
    return jsonify({
        'message' : '로그인 성공',
        'student_id' : user['student_id'],
        'name' : user['name']
    })