#include <Arduino.h>
#include <Servo.h>
//#include <LiquidCrystal.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

const int stage3Dist = 10;       // stage 3 active dist
const int stage3Angle = 90;     // stage 3 active angle

const int stage2Dist = 20;       // stage 2 active dist
const int stage2Angle = 60;      // stage 2 active angle

const int stage1Dist = 30;       // stage 1 active dist
const int stage1Angle = 30;      // stage 1 active dist

const int idleModeDist = 50;     // idle mode start dist (blink)


int cm = 0;
int intPosP = 0;
int intPosN = 180;

int buzPin = A0;                 // buzzer pin
int redLed = 13;                 // red led
int yellowLed = 12;              // yellow led
int greenLed = 11;               // green led

int servo01Pin = 10;
int servo02Pin = 9;

Servo servo01;
Servo servo02;
//LiquidCrystal lcd01(12, 11, 5, 4, 3, 2);
LiquidCrystal_I2C lcd01(0x27, 16, 2);

long readUltrasonicDistance(int triggerPin, int echoPin)
{
  pinMode(triggerPin, OUTPUT);  // Clear the trigger
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  // Sets the trigger pin to HIGH state for 10 microseconds
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);
  pinMode(echoPin, INPUT);
  // Reads the echo pin, and returns the sound wave travel time in microseconds
  return pulseIn(echoPin, HIGH);
}

void buzzTone(int dealyTime1, int delayTime2, bool emergStat) {
  if (emergStat == false)
  {
    tone(buzPin, 700);
    delay(dealyTime1);
    noTone(buzPin);
    delay(delayTime2);
  }
  else if (emergStat == true)
  {
    tone(buzPin, 950);
    delay(dealyTime1);
    noTone(buzPin);
    delay(delayTime2);

  }
  
  
}

// void ledIndicate(int ledPin) {
//   if (ledPin == 13)
//   {
//     digitalWrite(10, LOW);
//     digitalWrite(8, LOW);
//     digitalWrite(13, HIGH);
//   }
//   else if (ledPin == 10)
//   {
//     digitalWrite(8, LOW);
//     digitalWrite(13, LOW);
//     digitalWrite(10, HIGH);
//   }
//   else if (ledPin == 8)
//   {
//     digitalWrite(13, LOW);
//     digitalWrite(10, LOW);
//     digitalWrite(8, HIGH);
//   }
  
// }

void servoWrite(int angle) {
  angle++; //if the angle is 180 its gonna stop at 179 cuz 0
  for (size_t i = 0; i < angle; i++)
  {
    servo01.write(i);
    servo02.write(180-i);
  }
  
}


void ledIndicate(int ledPin=0, bool state=true) {
  int pins[] = {greenLed, yellowLed, redLed};
  if (state == true)
  {
    for (int i = 0; i < sizeof(pins); i++) 
    {
      digitalWrite(pins[i], (pins[i] == ledPin) ? HIGH : LOW); // ternary operator -->  <condition> ? <value IF True> : <value IF False>;
    }
  }
  else if (state == false)
  {
    for (int i = 0; i < sizeof(pins); i++)
    {
      digitalWrite(pins[i], LOW);
    }
    
  }
  
  
  
}


void idleMode(bool blinkStat=false, int delayTime=0) {
  if (blinkStat == false)
  {
    lcd01.clear();
    lcd01.setCursor(1, 0);
    lcd01.print("System Online!");
    lcd01.setCursor(3, 1);
    lcd01.print("Idle Mode...");
  }
  else if (blinkStat == true)
  {
    lcd01.setCursor(3, 1);
    lcd01.print("                ");
    delay(delayTime);
    lcd01.setCursor(3, 1);
    lcd01.print("Idle Mode...");
    delay(delayTime);
  }
  
}

void stages(int stageNumb, bool blinkStat=false, int delayTime=0) {

  String stageStat = "Stage " + String(stageNumb) + " Active..";

  if (blinkStat == false)
  {
    lcd01.clear();
    lcd01.setCursor(3, 0);
    lcd01.print("Warning...");
    lcd01.setCursor(0, 1);
    lcd01.print(stageStat);
  }
  else if (blinkStat == true)
  {
    lcd01.setCursor(0, 1);
    lcd01.print("                ");
    delay(delayTime);
    lcd01.setCursor(0, 1);
    lcd01.print(stageStat);
    delay(delayTime);
  }
  
}

void setup()
{
  Serial.begin(115200);
  pinMode(redLed, OUTPUT);
  pinMode(yellowLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  pinMode(buzPin, OUTPUT);
  servo01.attach(servo01Pin, 500, 2500);
  servo02.attach(servo02Pin, 500, 2500);
  lcd01.begin();
  servo01.write(intPosP);
  servo02.write(intPosN);
  idleMode();


}

void loop()
{
  cm = 0.01723 * readUltrasonicDistance(6, 7);
  // for debug
  // Serial.print(cm);
  // Serial.println("cm");

  if (cm <= stage3Dist)
  {
    buzzTone(25, 50, true);

    if (servo01.read() != stage3Angle)
    {
      noTone(buzPin);
      stages(3);
      ledIndicate(redLed);
      //servo01.write(stage3Angle);
      servoWrite(stage3Angle);
      Serial.print("ultsnc_sens^");
      Serial.println(cm);
    }
    else
    {
      stages(3, true, 75);
    }

  }
  else if (cm <= stage2Dist)
  {
    buzzTone(50, 100, false);

    if (servo01.read() != stage2Angle)
    {
      noTone(buzPin);
      int tempServ = servo01.read(); // overwritten wena nisa
      stages(2);
      ledIndicate(yellowLed);
      //servo01.write(stage2Angle);
      servoWrite(stage2Angle);
      if (tempServ != stage3Angle)
      {
        Serial.print("ultsnc_sens^");
        Serial.println(cm);
      }
    }
    else
    {
      stages(2, true, 100);
    }
    
    
  }
  else if (cm <= stage1Dist)
  {
    if (servo01.read() != stage1Angle)
    {
      noTone(buzPin);
      int tempServ = servo01.read();
      stages(1);
      ledIndicate(greenLed);
      //servo01.write(stage1Angle);
      servoWrite(stage1Angle);
      if (tempServ != stage2Angle)
      {
        Serial.print("ultsnc_sens^");
        Serial.println(cm);
      }
      
    }
    else
    {
      stages(1, true, 125);
    }
    
    
  }
  else if (cm < idleModeDist)
  {
    if (servo01.read() != 0)
    {
      noTone(buzPin);
      idleMode();
      ledIndicate();
      servo01.write(intPosP);
      servo02.write(intPosN);
    }
    else if (servo01.read() == 0)
    {
      idleMode(true, 300);
    }
    
    
  }
  

  delay(100);
}


