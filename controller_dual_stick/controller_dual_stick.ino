#include <Servo.h>

Servo left;
Servo right;

unsigned int rp = 0;
unsigned int lp = 160;
String command;

void setup() {
  right.attach(9);
  left.attach(8);
  //right.write(80);
  //left.write(80);
  //delay(500);
  //right.write(0);
  //left.write(160);
  //delay(250);

  //right.write(160);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\r').c_str();
    Serial.print(command);
    if (command == "lu" && lp < 160) {
      lp += 5;
      left.write(lp);
    }
    if (command == "ld" && lp > 0) {
      lp -= 5;
      left.write(lp);
    }
    else if (command == "ru" && rp > 0) {
      rp -=5;
      right.write(rp);
    }
    else if (command == "rd" && rp < 160) {
      rp += 5;
      right.write(rp);
    }
  }
  //delay(5);
  
}
