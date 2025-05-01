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
    if (String(status) == "OK") {
        Serial.print("이름: "); Serial.println(doc["name"].as<const char*>());
        Serial.print("학번: "); Serial.println(doc["student_id"].as<const char*>());
        Serial.print("전공: "); Serial.println(doc["major"].as<const char*>());
        available = doc["coupon_count"].as<int>();
        // coupon_count가 0이면 더 이상 못 빌림 
        // 1인 사람들만 우산을 빌릴 수 있음 
        // doc["coupon_count"] 로 1인지 0인지 판단해야 함
        Serial.println("등록된 사용자, 우산 열기 대기중..!");

        int ButtonNum = waitForButtonPress();
        unlockUmbrella(ButtonNum);
    } else {
      Serial.println("등록되지 않은 사용자");
    }
  }
  