from flask import Blueprint, request, jsonify
import DB.Flask_DB as DB

location_store_bp = Blueprint('umbrella_store_location', __name__)
location_find_bp = Blueprint('umbrella_find_location', __name__)

@location_store_bp.route('/umbrella_store_location', methods=['POST'])
def store_location():
    try:
        data = request.get_json()
        umbrella_uid = data.get('umbrella_uid')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not umbrella_uid or latitude is None or longitude is None:
            return jsonify({'error' : '요청 값 부족'}), 400
        
        conn = DB.get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
                       INSERT INTO umbrella_location (umbrella_uid, latitude, longitude)
                       VALUES (%s, %s, %s)
                       ON DUPLICATE KEY UPDATE
                       latitude = VALUES(latitude),
                       longitude = VALUES(longitude)
                       """, (umbrella_uid, latitude, longitude))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({'status' : 'success'}), 200
    except Exception as e:
        return jsonify({'error' : '[store_location] error', 'detail' : str(e)}), 500
        
@location_find_bp.route('/umbrella_find_location', methods=['POST'])
def find_location():
    try:
        # 앱에 저장되어 있는 uid가 오면 해당 uid와 일치하는 umbrella_uid를 select 하여 위도, 경도를 리턴함
        # 그러면 앱에서 해당 데이터를 받아서 지도 앱에 해당 위도, 경도를 나타내도록 하면 됨
        data = request.get_json()  # ✅ POST 요청에서는 request.args 대신 get_json() 사용
        get_uid = data.get('umbrella_uid')
        if not get_uid :
            return jsonify({'error' : '[find_location] umbrella_uid 오류'}), 400
        
        conn = DB.get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
                       SELECT umbrella_uid, latitude, longitude, recorded_at 
                       FROM umbrella_location
                       WHERE umbrella_uid = %s
                       """,(get_uid))
        result_umbrella_location = cursor.fetchone()

        cursor.close()
        conn.close()
        
        if not result_umbrella_location:
            return jsonify({'error' : '[find_location] no result'}), 400
        
        return jsonify({
            'umbrella_uid': result_umbrella_location['umbrella_uid'],
            'latitude': result_umbrella_location['latitude'],
            'longitude': result_umbrella_location['longitude'],
            'record_at': result_umbrella_location['recorded_at']
        })        

    except Exception as e:
        return jsonify({'error' : '[find_location] error', 'detail' : str(e)}), 500