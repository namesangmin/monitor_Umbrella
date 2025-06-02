from flask import Blueprint, request, jsonify
import DB.Flask_DB as DB

rental_log_bp = Blueprint('rental_log', __name__)
@rental_log_bp.route('/rental_log', methods=['GET'])
def rental_log():
    try:
        # 앱에서 user id가 온다 ( 이게 핸드폰마다 user id가 다른데 어떻게 이걸 파악하지)
        # 회원가입이 되어 있는 것도 아니고, 학교 학생증이랑 연동을 했다고 간단하게 만든건데
        # User id 어떻게 받아와야 하는지 생각이 안 나
        # 만약에 내가 대여 기록을 확인하려고 해.
        # 관리자 입장에서는 모든 유저의 대여기록을 볼 수 있어
        # 그러나 내가 uid가 A5A1F63인 유저면 이 유저에 해당하는 대여 기록만 보여줘야 해
        # 그런데 앱에서 uid를 가지고 있지 않아 
        # 그냥 핸드폰을 리더기에 갖다 대면 나오는 번호를 각각 유저마다 핸드폰 안에 삽입을 해야하나
        student_id = request.args.get('student_id')
        if not student_id:
            return jsonify({'error': '[rental_log] student_id가 필요합니다'}), 400
        
        conn = DB.get_db()
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT rl.location_id, rl.borrow_time, rl.return_time
                    FROM rental_log rl
                    JOIN user u ON rl.uid = u.uid
                    WHERE u.student_id = %s
                    ORDER BY rl.borrow_time DESC
                """, (student_id,))
        logs = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return jsonify({'rental_log' : logs})
    except Exception as e:
        #print(f'대여 기록 오류 발생 : {e}')
        return jsonify({'error' : '대여 기록 오류 발생', 'detail' : str(e)}), 500
