#include <Servo.h>

Servo myservo;

void setup() {
  Serial.begin(9600);
  myservo.attach(11); // Connect servo signal wire to pin 9
}

void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    int angle = input.toInt();

    int servoAngle = constrain(angle + 90, 0, 180); // Map -90–90 to 0–180
    myservo.write(servoAngle);
  }
}
