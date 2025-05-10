#include "MQTT.h"
#include "Button/Button.h"
#include "SG90/SG90.h"
#include "Func/Choice_Rental_Return.h"

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

  // 카드를 태그하고 버튼이 활성화되게 -> 대여 반납 버튼을 누르면 -> 우산 버튼이 활성화되게게
void callback(char* topic, byte* payload, unsigned int length) {
  /////////////////////////////
  Serial.print("Message arrived on topic: ");
  Serial.println(topic);  // ✅ 추가
  // ✅ 추가: payload 출력
  Serial.print("Payload: ");
  for (int i = 0; i < length; i++) {
      Serial.print((char)payload[i]);
  }
  Serial.println();
  /////////////////////////////
  StaticJsonDocument<256> doc;
  DeserializationError error = deserializeJson(doc, payload, length);

  if (error) {
    Serial.print("JSON 파싱 오류: ");
    Serial.println(error.f_str());
    return;
  }

  deserializeJson(doc, payload, length);
  choice_Rental_Return(doc);
}