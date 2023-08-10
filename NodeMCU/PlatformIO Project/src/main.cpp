#include <Arduino.h>
#include <ESP8266WiFi.h>
#include <FirebaseESP8266.h>
#include <ESP8266HTTPClient.h>

// Replace with your network credentials
const char* ssid = "YOUR-WIFI-SSID";
const char* password = "YOUR-WIFI-PASSWORD";


int redLed = D0;
int greenLed = D1;
int yellowLed = D2;

// Replace with your Firebase project's credentials
#define FIREBASE_HOST "YOUR-DATABSE-URL"
#define FIREBASE_AUTH "YOUR-AUTH-KEY"

FirebaseData firebaseData;

void blink(int pin, int time) {
  digitalWrite(pin, HIGH);
  delay(time);
  digitalWrite(pin, LOW);
  delay(time);
  digitalWrite(pin, HIGH);
  delay(time);
  digitalWrite(pin, LOW);
  delay(time);
}

void setup() {
  Serial.begin(115200);
  pinMode(redLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(yellowLed, OUTPUT);

  WiFi.begin(ssid, password);
  
  while (WiFi.status() != WL_CONNECTED) {
    blink(redLed, 200);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected...");

  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
  digitalWrite(greenLed, HIGH);
}


void loop() {
  static String inputString;

  while (Serial.available()) {
    char c = Serial.read();
    if (c == '\n') {
      Serial.print("Input received: ");
      Serial.println(inputString);
      digitalWrite(redLed, LOW); //red
      digitalWrite(greenLed, LOW); //green
      blink(yellowLed, 100); // yellow

      // Split the input string by '#' delimiter
      int lastIndex = 0;
      while (true) {
        int separatorIndex = inputString.indexOf('#', lastIndex);
        if (separatorIndex == -1) {
          separatorIndex = inputString.length();
        }
        String sensorValuePair = inputString.substring(lastIndex, separatorIndex);
        int commaIndex = sensorValuePair.indexOf('^');
        if (commaIndex > 0 && commaIndex < sensorValuePair.length() - 1) {
          String sensorId = sensorValuePair.substring(0, commaIndex);
          String sensorValue = sensorValuePair.substring(commaIndex + 1);
          String firebasePath = "/" + sensorId;

          // Check if the input value is a number or a string
          if (sensorValue.toInt() != 0 || sensorValue.equals("0")) {
            Firebase.setInt(firebaseData, firebasePath.c_str(), sensorValue.toInt());
          } else {
            Firebase.setString(firebaseData, firebasePath.c_str(), sensorValue.c_str());
          }

          if (firebaseData.httpCode() == HTTP_CODE_OK) {
            Serial.println("Data uploaded to Firebase");
            digitalWrite(greenLed, HIGH);
          } else {
            Serial.println("Data upload failed");
            blink(redLed, 100);
            digitalWrite(redLed, HIGH);
          }
        }
        if (separatorIndex == inputString.length()) {
          break;
        } else {
          lastIndex = separatorIndex + 1;
        }
      }

      inputString = "";
    } else if (c != '\r') {
      inputString += c;
    }
  }

  delay(100);
}

