# Flask 기반 대여 시스템

## 구조
### Flask_func 폴더
- `/ranking`: [GET] 연체 랭킹 확인
- `/report`: [POST] 신고하기
- `/rental_log`: [GET] 사용자 대여 기록 확인
- `/user_info`: [GET] 쿠폰/대여일자 등 확인
- `/login`: [POST] 학번 + 비밀번호 로그인
- '/current_umbrella'	[GET]	각 위치 우산 수량 확인

### Flask_rental_return
- `/rental`: [POST] 앱 인증 + RFID 태깅 대여
- `/return`: 반납인데 아직 필요없음

## 실행 방법
```bash
# 가상환경 활성화
source myenv/bin/activate

# 서버 실행
python app.py
```

## 시스템 흐름 요약
1. 카드만으로 대여하는 경우
리더기에 RFID 태깅 → UID만으로 바로 대여 처리

2. 앱으로 대여하는 경우
앱에서 /rental 호출 (학번 전달)

3. Flask 서버는 rental_session 테이블에 학번 기록

4. 사용자가 리더기에 학생증 태깅

5. 서버가 UID ↔ 학번 일치 여부 확인
   
6. 일치 → 대여 처리 / 불일치 → 오류 반환
   
7. 세션은 10초 이내 태깅이 없으면 무효화됩니다.
