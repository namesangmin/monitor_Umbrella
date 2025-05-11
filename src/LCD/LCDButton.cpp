#include "LCDControl.h"
#include "LCDButton.h"

void ButtonPrompt(){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Press Rental or");
    LCD.getLCD().setCursor(0,1);
    LCD.getLCD().print("Return (10s)");
    delay(1000);
}

void ButtonRentalPressed(){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Rental Selected");
    delay(2000);
}

void ButtonReturnPressed(){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Return Selected");
    delay(2000);
}

void ButtonUmbrellaPressed(int n){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Umbrella");
    LCD.getLCD().setCursor(0,1);
    LCD.getLCD().print(n);
    LCD.getLCD().print(" Pressed");
    delay(2000);
}

void TimeoutPrint() {
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0, 0);
    LCD.getLCD().print("Timeout");
    delay(2000);
}