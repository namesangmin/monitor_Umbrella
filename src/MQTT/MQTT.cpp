#include "MQTT.h"
#include "Button/Button.h"
#include "SG90/SG90.h"

WiFiClient espClient;
PubSubClient client(espClient);

void initMQTT(){
    client.setServer(mqtt_server, port);
    client.setCallback(callback);
}

void reconnect() {
    while (!client.connected()) {
      Serial.print("Attempting MQTT connection...");
      if (client.connect("ESP32Client")) {
        Serial.println("connected");
        client.subscribe("uid/response");
      } else {
        Serial.print("failed, rc=");
        Serial.print(client.state());
        delay(2000);
      }
    }
}

// 대여 
void Rental(String uid) {
    Serial.println("등록된 사용자, 우산 대여 진행 중...");
    int btn = waitForButtonPress();
    unlockUmbrella(btn);
    
    StaticJsonDocument<256> doc;
    doc["uid"] = uid;
    doc["location_id"] = 2; // 원래는 여기에 공학관 위치를 넣어야 함

    char buffer[256];
    serializeJson(doc, buffer);
    client.publish("umbrella/rental", buffer);
}

// 빈닙
void Return(String uid) {
    Serial.println("반납 요청 처리 중...");
    int btn = waitForButtonPress();
    unlockUmbrella(btn);
  
    StaticJsonDocument<256> doc;
    doc["uid"] = uid;
    doc["location_id"] = 2; // 원래는 여기에 공학관 위치를 넣어야 함
      
    char buffer[256];
    serializeJson(doc, buffer);
    client.publish("umbrella/return", buffer);
}
  

  // 카드를 태그하고 버튼이 활성화되게 -> 대여 반납 버튼을 누르면 -> 우산 버튼이 활성화되게게
void callback(char* topic, byte* payload, unsigned int length) {
    StaticJsonDocument<256> doc;
    DeserializationError error = deserializeJson(doc, payload, length);
    int available = -1;
    if (error) {
      Serial.print("JSON 파싱 오류: ");
      Serial.println(error.f_str());
      return;
    }
  
    const char* status = doc["status"];
    if (String(status) != "OK") {
        Serial.println("등록되지 않은 사용자");
        return;
    }

    available = doc["coupon_count"].as<int>();
    String uid = doc["uid"].as<String>();
    String action = waitForAction();
    // 대여 요청인데 쿠폰이 없으면 막음
    if (action == "rental" && available == 0) {
        Serial.println("대여 불가: 이미 우산을 빌린 상태입니다.");
        return;
    }
    // 반납 요청인데 쿠폰이 1이면 이미 반납된 상태
    if (action == "return" && available == 1) {
        Serial.println("반납 불가: 우산을 대여한 상태가 아닙니다.");
        return;
    }
    if (action == "rental"){
        Rental(uid);
    }
    else if(action == "return"){
        Return(uid);
    }
}