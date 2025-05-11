#include "LCDControl.h"

LCDControl LCD;
LCDControl::LCDControl() : lcd(0x27,16,2) {}

void LCDControl::init(){
    Wire.begin(21,22); // SDA, SCL
    lcd.init();
    lcd.backlight();
    lcd.clear();
}

void LCDControl::MainPrint(){
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Tag Student ID");
    lcd.setCursor(0,1);
    lcd.print("Card");
}

LiquidCrystal_I2C& LCDControl::getLCD(){
    return lcd;
}