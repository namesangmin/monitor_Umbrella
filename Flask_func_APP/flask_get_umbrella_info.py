from flask import Blueprint, request, jsonify
import DB.Flask_DB as DB

get_umbrella_info_bp = Blueprint('get_umbrella_info', __name__)
store_umbrella_place_bp = Blueprint('store_umbrella_place', __name__)
get_umbrella_place_bp = Blueprint('get_umbrella_place', __name__)
@get_umbrella_info_bp.route('/get_umbrella_info', methods = ['POST'])
def umbrella_info():
    try:
        data = request.get_json()
        uid = data.get('uid')
        if not uid:
            return jsonify({"error": "UID 누락"}), 400
        
        conn = DB.get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
                    SELECT location_id, number
                    FROM umbrella
                    WHERE uid = %s
                    """,(uid))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if result:
            return jsonify({
                'location' : result['location_id'],
                'number' : result['number']
            })
        else:
            return jsonify({"error": "해당 UID를 찾을 수 없습니다"}), 404
    except Exception as e:
        return jsonify({"error" : "DB error", "detail" : str(e)}), 500
    
@store_umbrella_place_bp.route('/store_location', methods= ['POST'])
def store_umbrella_place():
    try:
        data = request.get_json()
        uid = data.get('UID')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not uid or latitude is None or longitude is None:
                return jsonify({'error': '필수값 누락'}), 400

        conn = DB.get_db()
        cursor = conn.cursor()
        print("[DEBUG] uid repr:", repr(uid))
        print("[DEBUG] uid:", uid)
        print("[DEBUG] latitude:", latitude, type(latitude))
        print("[DEBUG] longitude:", longitude, type(longitude))

        
        cursor.execute("""   
                        INSERT INTO umbrella_location (umbrella_uid, latitude, longitude)
                        VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE
                        latitude = VALUES(latitude),
                        longitude = VALUES(longitude),
                        recorded_at = CURRENT_TIMESTAMP
                """, (uid, latitude, longitude))
        cursor.close()
        conn.commit()
        conn.close()
        return jsonify({'status': 'success'}), 200
    except Exception as e:
        import traceback
        traceback.print_exc()  #
        return jsonify({'error' : '[store_umbrella_place] DB error', 'detail' : str(e)}), 500

@get_umbrella_place_bp.route('/get_location', methods = ['POST'])
def get_umbrella():
    try:
        data = request.get_json()
        uid = data.get('uid')
        
        if not uid:
            return jsonify({'error': '우산 uid 누락'}), 400
        conn = DB.get_db()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT umbrella_uid, latitude, longitude, recorded_at
                       FROM umbrella_location
                       WHERE umbrella_uid = %s
                       """, (uid))
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        if result:
            return jsonify({
                'uid' : result['umbrella_uid'],
                'latitude' : result['latitude'],
                'longitude' : result['longitude'],
                'recorded_at': result['recorded_at'].strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            return jsonify({'error' : '[get_umbrella] 조회된 우산 정보 없음'}), 404

    except Exception as e:
        return jsonify({'error' : '[get_umbrella] DB error', 'detail' : str(e)}), 500