#include "Button.h"

void initButton(){
    pinMode(button1Pin, INPUT_PULLUP);
    pinMode(button2Pin, INPUT_PULLUP);
    pinMode(button3Pin, INPUT_PULLUP);
    pinMode(button4Pin, INPUT_PULLUP);
    pinMode(button5Pin, INPUT_PULLUP);
}
// 버튼 누를 때까지 기다림
int waitForButtonPress() {
    int button = -1;
    while (button == -1) {
      button = funcButton(); 
    }
    return button;
}

int funcButton(){
    const int NUM_BUTTONS = 5;
    const int buttonPins[NUM_BUTTONS] = {button1Pin, button2Pin, button3Pin, button4Pin, button5Pin};

    for (int i = 0; i < NUM_BUTTONS; i++) {
        if (digitalRead(buttonPins[i]) == LOW) {
          Serial.printf("우산 %d번 버튼 눌림 - 잠금/해제 동작\n", i + 1);
          delay(200);  // 디바운싱(여러 번 누를 수 있으니까)
          return i + 1;  
        }
      }
      return -1; 
}