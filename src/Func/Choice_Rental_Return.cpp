#include "Choice_Rental_Return.h"

  // 대여 
void Rental(String uid) {
  Serial.println("등록된 사용자, 우산 대여 진행 중... 대여할 우산을 선택하세요.");
  int btn = waitForButtonPress();
  char buffer[256];
  StaticJsonDocument<256> doc;
  Rental_unlockUmbrella(btn);
  
  doc["uid"] = uid;
  doc["location_id"] = 2; // 원래는 여기에 공학관 위치를 넣어야 함

  serializeJson(doc, buffer);
  client.publish("umbrella/rental", buffer);
}
  
  // 빈닙
void Return(String uid) {
  Serial.println("등록된 사용자, 반납 요청 처리 중... 반납할 우산꽂이을 선택하세요.");
  int btn = waitForButtonPress();
  char buffer[256];
  StaticJsonDocument<256> doc;

  Return_unlockUmbrella(btn);

  doc["uid"] = uid;
  doc["location_id"] = 2; // 원래는 여기에 공학관 위치를 넣어야 함
    
  serializeJson(doc, buffer);
  client.publish("umbrella/return", buffer);
}
  
void choice_Rental_Return(JsonDocument& doc){
  int available = -1;
  const char* status = doc["status"];
  available = doc["coupon_count"].as<int>();
  String uid = doc["uid"].as<String>();

  if (String(status) != "OK") {
      Serial.println("등록되지 않은 사용자");
      Serial.println("메인으로 돌아갑니다.\n");
      return;
  }

  String action = waitForAction();
  
  // 대여 요청인데 쿠폰이 없으면 막음
  if (action == "rental" && available == 0) {
    Serial.println("대여 불가: 이미 우산을 빌린 상태입니다.");
    Serial.println("메인으로 돌아갑니다.\n");
    return;
  }

  // 반납 요청인데 쿠폰이 1이면 이미 반납된 상태
  if (action == "return" && available == 1) {
      Serial.println("반납 불가: 우산을 대여한 상태가 아닙니다.");
      Serial.println("메인으로 돌아갑니다.\n");
      return;
  }

  if (action == "rental"){
      Rental(uid);
  }
  else if(action == "return"){
      Return(uid);
  }

  Serial.println("메인으로 돌아갑니다.\n");
}