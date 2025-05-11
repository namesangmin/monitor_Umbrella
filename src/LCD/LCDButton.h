#ifndef LCDButton_H
#define LCDButton_H

void ButtonPrompt();                // 대여/반납 안내
void ButtonRentalPressed();         // 대여 버튼 눌림
void ButtonReturnPressed();         // 반납 버튼 눌림
void ButtonUmbrellaPressed(int n);  // 우산 버튼 눌림
void TimeoutPrint();                // 입력 시간 초과
#endif 
