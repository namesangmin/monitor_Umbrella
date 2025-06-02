from flask import Blueprint, request, jsonify
import DB.Flask_DB as DB

ranking_bp = Blueprint('ranking', __name__)
@ranking_bp.route('/ranking', methods=['GET']) 
def ranking():
    try:
        conn = DB.get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT s.name, u.penalty_days AS score, u.major
            FROM user u
            JOIN student_info s ON u.student_id = s.student_id
            ORDER BY score DESC
        """)
        user = cursor.fetchall()
        cursor.execute("""
            SELECT major, ROUND(AVG(penalty_days), 1) AS avg
            FROM user
            GROUP BY major
            ORDER BY avg DESC
        """)
        major = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({'user': user, 'majors': major})
    except Exception as e:
        return jsonify({'error': '랭킹 시스템 오류 발생', 'detail' : str(e)}), 500