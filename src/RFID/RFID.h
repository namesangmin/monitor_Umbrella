#ifndef RFID_H
#define RFID_H

#include <SPI.h>
#include <MFRC522.h>

extern MFRC522 rfid;
extern const int RST_Pin;
extern const int SS_Pin;
void initRFID();
String funcRFID();
#endif
