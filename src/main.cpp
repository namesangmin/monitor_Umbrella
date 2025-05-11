//#include <Arduino.h>
#include "WIFI/WIFI.h"
#include "SG90/SG90.h"
#include "MQTT/MQTT.h"
#include "RFID/RFID.h"
#include "Button/Button.h"
#include "LCD/LCDControl.h"

// 와이파이 아이디, 비밀번호
const char* ssid = "hello";
const char* password = "zktmxkem12";
// 라즈베리파이 외부 IP
const char* mqtt_server = "112.184.197.77";  // 라즈베리파이 IP -> MQTT 용
const int port = 1883;
//const char* serverURL = "http://112.184.197.77:5000/rfid_check"; -> Flask 용(HTTP)

// ESP32 버튼 핀 셋팅값(우산, 반납, 대여)
// 일단 5개임 더 늘릴 수 있는데 가지고 있는 버튼이 5개 밖에 없음
const int Umbrella1Pin = 4;  // 우산 1
const int Umbrella2Pin = 12;  // 우산 2
const int Umbrella3Pin = 13; // 우산 3
const int ReturnPin = 14; // 반납
const int RentalPin = 15; // 대여
// SG90 서보모터 셋팅값
const int servoPin = 16;
// RFID 셋팅값
const int RST_Pin = 17;
const int SS_Pin = 5;

bool waiting = true;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  delay(100); 
  initWiFi(); // 와이파이 셋팅값
  initButton(); // 버튼 셋팅값
  initServo(servoPin); // SG90 Servo 모터 셋팅값, myServo.attach(servoPin);
  initMQTT(); // MQTT 셋팅값
  initRFID(); // RFID 셋팅값
  LCD.init();
}

void loop() {
  // put your main code here, to run repeatedly:
  if(!client.connected()) reconnect();
  client.loop();
  if(waiting){
    LCD.MainPrint(); //Serial.println("학생증 카드 또는 학생증 앱을 태그해주세요.");
    waiting = false;
  }

  String uid = funcRFID();
  if (uid != "") {
    Serial.println("Tag UID: " + uid);
    client.publish("uid/check", uid.c_str());
    waiting = true;
    delay(2000);  
  }
}