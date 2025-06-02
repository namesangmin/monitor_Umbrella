from flask import Blueprint, request, jsonify
import DB.Flask_DB as DB
from datetime import datetime

user_info_bp = Blueprint('user_info', __name__)
@user_info_bp.route('/user_info', methods=['GET'])
def user_info():
    try:
        student_id = request.args.get('student_id')
        if not student_id :
            return jsonify({'error' : '[user info] student_id 오류'}), 400
        
        conn = DB.get_db()
        cursor = conn.cursor()
        # ?? student_id�� ��ȣ�� �ذ�: user.student_id�� ����
        cursor.execute("""
            SELECT coupon_count, borrow_day, pre_return_day, name, penalty_days, location_id, umbrella_id, umbrella_uid
            FROM user
            WHERE student_id = %s
        """, (student_id,))
        
        user = cursor.fetchone()
        if not user:
            return jsonify({'error' : '해당 학번의 유저를 찾을 수 없습니다'}), 404
        
        location_id = user['location_id']
        umbrella_id = user['umbrella_id']
        umbrella_uid = user['umbrella_uid']
        
        # cursor.execute("""
        #                SELECT uid from umbrella
        #                WHERE location_id = %s and number = %s
        #                """, (location_id, umbrella_id))
        # uid_result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        coupon_count = user['coupon_count']
        borrow_day = user['borrow_day']
        pre_return_day = user['pre_return_day']
        name = user['name']  #student_info.name을 받아온다
        penalty = user['penalty_days']
        location_id = user['location_id']
        umbrella_id = user['umbrella_id']
        #umbrella_uid = uid_result['uid']
        #borrow_day나 per_return_day가 None인 경우에는
        #is_late,remian_time_minutes가 정의되지 않고 return 문에서 이 값들을
        #jsonify 할 때 오류가 난다(gpt)
        #수정 방향
        #is_late, remain_time_minutes에 조건문 밖에서 기본값을 지정하기
        #초기값 지정
        is_late = False
        remain_time_minutes = 0
        # status_message = "이용 내역이 없습니다"
        
        if borrow_day and pre_return_day:
            now = datetime.now()
            remain_time = pre_return_day - now
            
            total_seconds = int(remain_time.total_seconds())
            is_late = total_seconds < 0 
            
            abs_seconds = abs(total_seconds)
            days = abs_seconds // 86400
            hours = (abs_seconds % 86400) // 3600
            minutes = (abs_seconds % 3600) // 60
            
            # 분 단위로 전체 시간 계산
            remain_time_minutes = abs_seconds // 60
            if is_late:
                status_message = f"{days}일 {hours}시간 {minutes}분 연체 중"
            else:
                status_message = f"{days}일 {hours}시간 {minutes}분 남음"
        else:
            status_message = "이용 내역이 없습니다"
            
        return jsonify({
            'name' : name,
            'coupon_count' : coupon_count,
            'borrow_day' : borrow_day,
            'pre_return_day' : pre_return_day,
            'is_late' : is_late,
            'penalty' : penalty,
            # 변수하나 남은 시간 분 단위 
            'remain_time_minutes' : remain_time_minutes,
            'status' : status_message,
            # 몇 공학관
            'location_id' : location_id,
            # 몇 번 우산
            'umbrella_id' : umbrella_id,
            # 우산 고유 번호
            'umbrella_uid' : umbrella_uid
        })       
            
    except Exception as e:
        return jsonify({'error' : '유저 정보 시스템 오류 발생', 'detail' : str(e)}), 500
