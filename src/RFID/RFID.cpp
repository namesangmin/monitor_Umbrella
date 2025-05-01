#include "RFID.h"

MFRC522 rfid(SS_Pin, RST_Pin);

void initRFID(){
    SPI.begin();
    rfid.PCD_Init();
}

String funcRFID() {
    if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
      String uid = "";
      for (byte i = 0; i < rfid.uid.size; i++) {
        uid += String(rfid.uid.uidByte[i], HEX);
      }
      uid.toUpperCase();
      rfid.PICC_HaltA();
      return uid;
    }
    return "";
  }