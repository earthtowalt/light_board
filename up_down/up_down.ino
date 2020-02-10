#include <Servo.h>

Servo left;
Servo right;

void setup() {
  right.attach(9);
  right.write(0);
  left.attach(8);
  left.write(160);
  delay(1000);

  //right.write(160);
  Serial.begin(9600);
}

void loop() {
  //while (true);
//  for (unsigned int i=10; i < 170; i+=1) {
//    
//    right.write(i);
//    left.write(160-i);
//    delay(50);
//    Serial.println(i);
//  }
  for (double theta=0; theta<2*PI; theta+=.02) {
    right.write(80*cos(theta) + 80);
    left.write(80*sin(theta) + 80);
    delay(70);
  }
  
}
