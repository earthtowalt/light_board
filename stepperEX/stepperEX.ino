/*     Simple Stepper Motor Control Exaple Code
 *      
 *  by Dejan Nedelkovski, www.HowToMechatronics.com
 *  
 */
// defines pins numbers
const int stepPin = 10; 
const int dirPin = 9; 

int sensorPin = A1;
int height = 0;
int sensorValue;

void setup() {
  // Sets the two pins as Outputs
  Serial.begin(9600);
  Serial.println("initializing");
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
}
void loop() {

  sensorValue = map(analogRead(sensorPin), 0, 900, 0, 45);
  Serial.println(sensorValue);
  Serial.println(height);

  while(sensorValue < height){
    for(int i = 0; i <= 100; i++){
      digitalWrite(dirPin,HIGH);
      digitalWrite(stepPin,HIGH); 
      delayMicroseconds(500); 
      digitalWrite(stepPin,LOW); 
      delayMicroseconds(500);
    }
    sensorValue = map(analogRead(sensorPin), 0, 900, 0, 45);
    height = height - 1;
  }

  while(height < sensorValue){
    for(int i = 0; i <= 100; i++){
      digitalWrite(dirPin,LOW);
      digitalWrite(stepPin,HIGH); 
      delayMicroseconds(500); 
      digitalWrite(stepPin,LOW); 
      delayMicroseconds(500);
    }
    sensorValue = map(analogRead(sensorPin), 0, 900, 0, 45);
    height = height + 1;
  }
  
}
