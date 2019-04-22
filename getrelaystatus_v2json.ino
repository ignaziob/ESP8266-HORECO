/**
   BasicHTTPClient.ino

    Created on: 24.05.2015

*/
#define DEBUGLEVEL B01
#include <Arduino.h>

#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>

#include <ESP8266HTTPClient.h>

#include <WiFiClient.h>
ESP8266WiFiMulti WiFiMulti;

#include <ArduinoJson.h>

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);     // Initialize the LED_BUILTIN pin as an output

  Serial.begin(115200);
  // Serial.setDebugOutput(true);

  Serial.println();
  Serial.println();
  Serial.println();

  for (uint8_t t = 4; t > 0; t--) {
    Serial.printf("[SETUP] WAIT %d...\n", t);
    Serial.flush();
    delay(1000);
  }

  WiFi.mode(WIFI_STA);
  WiFiMulti.addAP("778116", "260237470");
}

void loop() {
  // wait for WiFi connection
  if ((WiFiMulti.run() == WL_CONNECTED)) {

    WiFiClient client;

    HTTPClient http;

    Serial.print("[HTTP] begin...\n");
    if (http.begin(client, "http://cuceglio.eu3.org/allactuatorstatus.php")) {  // HTTP - read relays desidered status
      // start connection and send HTTP header
      int httpCode = http.GET();

      // httpCode will be negative on error
      if (httpCode > 0) { // https://circuits4you.com/2019/01/11/nodemcu-esp8266-arduino-json-parsing-example/
        // HTTP header has been send and Server response header has been handled
        //Serial.printf("[HTTP] GET... code: %d\n", httpCode);

        // file found at server
        if (httpCode == HTTP_CODE_OK || httpCode == HTTP_CODE_MOVED_PERMANENTLY) {
          String payload = http.getString();
          Serial.println(payload);

          // Allocate JsonBuffer
          // Use arduinojson.org/assistant to compute the capacity.
          // const size_t capacity = JSON_OBJECT_SIZE(3) + JSON_ARRAY_SIZE(2) + 60;
          DynamicJsonDocument doc(512);
  
          // Parse JSON object
          DeserializationError error = deserializeJson(doc, payload);
          if ( (error) && (DEBUGLEVEL &B01) ){
            Serial.println(F("Parsing failed!"));
            return;
          }
  
          // Decode JSON/Extract values
          if (DEBUGLEVEL & B01) {
            Serial.print("DEBUG Relay 4 Json required status: ");
            serializeJson(doc["4"], Serial);
          }
          const char* relayvalue = doc["4"];
          if ( String(relayvalue) == String("ON"))
            digitalWrite(LED_BUILTIN, LOW);   // Turn the LED on (active low on the ESP-01)
             else 
          digitalWrite(LED_BUILTIN, HIGH);   // Turn the LED off (active low on the ESP-01)
        }      
      } else {
        Serial.printf("[HTTP] GET... failed, error: %s\n", http.errorToString(httpCode).c_str());
      }

      http.end();
    } else {
      Serial.printf("[HTTP} Unable to connect\n");
    }
  }
  delay(10000);
}
