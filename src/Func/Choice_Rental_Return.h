#ifndef FUNC_H
#define FUNC_H

#include "MQTT/MQTT.h"
#include "Button/Button.h"
#include "SG90/SG90.h"

void choice_Rental_Return(JsonDocument& doc);
void Rental(String uid);
void Return(String uid);

#endif