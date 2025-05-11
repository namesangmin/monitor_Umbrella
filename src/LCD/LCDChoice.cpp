#include "LCDControl.h"
#include "LCDChoice.h"

void ChoiceRental(){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Renting...");
    LCD.getLCD().setCursor(0,1);    
    LCD.getLCD().print("Select slot");
    delay(1000);
}

void ChoiceReturn(){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Returning...");
    LCD.getLCD().setCursor(0,1);    
    LCD.getLCD().print("Select slot");
    delay(1000);
}

void ChoiceNotResister(){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Unregistered");
    LCD.getLCD().setCursor(0,1);    
    LCD.getLCD().print("user");
    delay(2000);
    ChoiceGoMain();
}

void ChoiceAlreadyBorrow(){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Rental denied:");
    LCD.getLCD().setCursor(0,1);    
    LCD.getLCD().print("Already rented");
    delay(2000);
    ChoiceGoMain();

}

void ChoiceNotBorrow(){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Rental denied:");
    LCD.getLCD().setCursor(0,1);    
    LCD.getLCD().print("No rental found");
    delay(2000);
    ChoiceGoMain();
}

void ChoiceGoMain(){
    LCD.getLCD().clear();
    LCD.getLCD().setCursor(0,0);
    LCD.getLCD().print("Returning to");
    LCD.getLCD().setCursor(0,1);    
    LCD.getLCD().print("main menu");
    delay(2000);
}