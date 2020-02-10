/*     Simple Stepper Motor Control Exaple Code
 *      
 *  by Dejan Nedelkovski, www.HowToMechatronics.com
 *  
 */
// defines pins numbers
const int sp1 = 10; 
const int dp1 = 9; 

int m1 = 0;
int d1 = 0;

String command;

void setup() {
  // Sets the two pins as Outputs
  Serial.begin(9600);
  Serial.println("initializing");
  
  pinMode(sp1,OUTPUT); 
  pinMode(dp1,OUTPUT);
  
  digitalWrite(dp1, HIGH);
}
void loop() {

  // wait until command sent
  Serial.print("waiting for command");
  while (!Serial.available()) {
    delay(100);
    //Serial.print(".");
  }
  command = Serial.readStringUntil('\r').c_str();
  Serial.println("\nCommand received: " + command);
  
  // interpret command
  int steps = command.toInt();

  // assume it is a number and we move n steps
  if (steps > 0) {
    digitalWrite(dp1, LOW);
  }
  else {
    digitalWrite(dp1, HIGH);
  }
  
  for (int i = 0; i < abs(steps); ++i) {
    digitalWrite(sp1, HIGH);
    delayMicroseconds(500);
    digitalWrite(sp1,LOW); 
    delayMicroseconds(500);
  }

  delay(10);
  
}
