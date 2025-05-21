from flask import Blueprint, request, jsonify
import DB.Flask_DB as DB

# 보내는 방법
# final response = await http.get(
#   Uri.parse('http://라즈베리파이_IP:5000/current_umbrella?location_id=1'),
# );

current_umbrella_bp = Blueprint('current_umbrella', __name__)
@current_umbrella_bp.route('/current_umbrella', methods=['GET'])
def current_umbrella_map():
    try:
        location_id = int(request.args.get('location_id'))
        if not location_id:
            return jsonify({'error': '[current_umbrella_map] location_id가 필요합니다.'}), 400
        
        conn = DB.get_db()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("""SELECT current_count, max_count 
                       FROM umbrella_count
                       WHERE location_id=%s"""
                       ,(location_id,))
        current_count = cursor.fetchall()
        cursor.close()
        conn.close()
        
        if current_count is None:
            return jsonify({'error' : '해당 위치의 데이터가 존재하지 않습니다'}), 404
        return jsonify({'current_count':current_count})
    except Exception as e:
        return jsonify({'error': '우산 현황 조회 중 오류가 발생했습니다', 'detail': str(e)}), 500
        
        