#include "LCDControl.h"
#include "LCDSG90.h"

void SG90RentalChoice(int n){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Umbrella ");
    LCD.getLCD().print(n);
    LCD.getLCD().setCursor(0,1);    
    LCD.getLCD().print("Unlock Working.");
    delay(2000);
}
void SG90ReturnChoice(int n){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Umbrella ");
    LCD.getLCD().print(n);
    LCD.getLCD().setCursor(0,1);    
    LCD.getLCD().print("Lock Working.");
    delay(2000);
}