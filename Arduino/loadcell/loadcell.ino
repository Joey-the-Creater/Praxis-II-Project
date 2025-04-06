#include "HX711.h"
#include <Servo.h>

#define DOUT  3
#define CLK  2

#define enA 12
#define in1 9
#define in2 8
#define in3 7
#define in4 6
#define enB 5

int speedFast = 230;
int speedSlow = 200;

char userinput;
HX711 scale;
Servo myservo;

float calibration_factor = 435197.81; //-7050 * 0.453592; // Adjusted for kilograms, later used for grams

void setup() {
  Serial.begin(9600);

  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
  pinMode(enB, OUTPUT);

  scale.begin(DOUT, CLK);
  scale.set_scale();
  scale.tare(); // Reset the scale to 0

  long zero_factor = scale.read_average(); // Get a baseline reading
  Serial.print("Zero factor: ");
  Serial.println(zero_factor); // Useful for permanent scale projects
  myservo.attach(11);

}

void loop() {
  analogWrite(enA, speedFast);
  digitalWrite(in1, HIGH);
  digitalWrite(in2, LOW);

  analogWrite(enB, speedSlow);
  digitalWrite(in3, HIGH);
  digitalWrite(in4, LOW);

  scale.set_scale(calibration_factor); // Adjust to this calibration factor

  // Convert the reading to grams
  float weight_in_grams = scale.get_units() * 1000;

  Serial.print("Reading: ");
  Serial.print(weight_in_grams, 1); // Display weight in grams
  Serial.print(" g"); 
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor);
  Serial.println();

  if (weight_in_grams >= 165) {
    Serial.println("ALERT: Bin is Full");  
    speedFast = 0;
    speedSlow = 0;
    while(1){
    }
  }

  delay(1000);

  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    int angle = input.toInt();

    int servoAngle = constrain(angle + 90, 0, 180); // Map -90–90 to 0–180
    myservo.write(servoAngle);
  }

  // if (Serial.available()) {
  //   char temp = Serial.read();
  //   if (temp == '+' || temp == 'a')
  //     calibration_factor += 1000; // Increase calibration factor
  //   else if (temp == '-' || temp == 'z')
  //     calibration_factor -= 1000; // Decrease calibration factor
  // }
}
