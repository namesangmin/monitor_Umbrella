#ifndef LCDCONTROL_H
#define LCDCONTROL_H
#include <Arduino.h>
#include <LiquidCrystal_I2C.h>

class LCDControl{
public:
    LCDControl();
    void init();
    void MainPrint();
    LiquidCrystal_I2C& getLCD();

private:
    LiquidCrystal_I2C lcd;
};
extern LCDControl LCD;

#endif 
