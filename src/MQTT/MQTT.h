#ifndef MQTT_H
#define MQTT_H

#include <PubSubClient.h>
#include <WiFi.h>
#include <ArduinoJson.h>  

extern const char* mqtt_server;
extern const int port;
extern WiFiClient espClient;
extern PubSubClient client;

void initMQTT();
void reconnect();
void callback(char* topic, byte* payload, unsigned int length);
#endif