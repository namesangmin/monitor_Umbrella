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
        cursor = conn.cursor(dictionary = True)
        cursor.execute("""
                       SELECT coupon_count, borrow_day, pre_return_day
                       FROM user
                       WHERE student_id = %s
                       """, (student_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if not user:
            return jsonify({'error' : '해당 학번의 유저를 찾을 수 없습니다'}), 404
        
        coupon_count = user['coupon_count']
        borrow_day = user['borrow_day']
        pre_return_day = user['pre_return_day']
        
        if borrow_day and pre_return_day:
            now = datetime.now()
            remain_time = pre_return_day - now
            
            total_seconds = int(remain_time.total_second())
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
            status_message = "대여 기록 없음"
            
        return jsonify({
            'coupon_count' : coupon_count,
            'borrow_day' : borrow_day,
            'pre_return_day' : pre_return_day,
            'is_late' : is_late,
            
            # 변수하나 남은 시간 분 단위 
            'remain_time_minutes' : remain_time_minutes,
            'status' : status_message
        })       
    except Exception as e:
        return jsonify({'error' : '유저 정보 시스템 오류 발생', 'detail' : str(e)}), 500