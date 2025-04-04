const int in3 = 8; 
const int in4 = 9; 
const int enB = 10; 

void setup() {
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(enB, OUTPUT);
}

void loop() {
  analogWrite(enB, 250); 
  digitalWrite(in3, HIGH); 
  digitalWrite(in4, LOW); 
}

