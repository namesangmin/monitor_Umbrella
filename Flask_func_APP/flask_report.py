from flask import Blueprint, request, jsonify
import DB.Flask_DB as DB

# 신고
report_bp = Blueprint('report', __name__)
@report_bp.route('/report',methods=['POST'])
def report():
    try:
        data = request.get_json()
        student_id = data.get('user_id')
        title = data.get('title')
        content = data.get('content')

        if not title or not content:
            return jsonify({'status': 'fail', 'message': '제목 또는 내용이 비었습니다.'}), 400

        conn = DB.get_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reports (user_id, title, content)
            VALUES (%s, %s, %s)
        """, (student_id, title, content))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'success'}), 200

    except Exception as e:
        print(f'신고 기능 오류: {e}')
        return jsonify({'status': 'error', 'message': str(e)}), 500