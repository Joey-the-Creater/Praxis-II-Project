#include "HX711.h"

#define DOUT  3
#define CLK  2

char userinput;
HX711 scale;

float calibration_factor = 435197.81; //-7050 * 0.453592; // Adjusted for kilograms, later used for grams

void setup() {
  Serial.begin(9600);

  scale.begin(DOUT, CLK);
  scale.set_scale();
  scale.tare(); // Reset the scale to 0

  long zero_factor = scale.read_average(); // Get a baseline reading
  Serial.print("Zero factor: ");
  Serial.println(zero_factor); // Useful for permanent scale projects
}

void loop() {
  scale.set_scale(calibration_factor); // Adjust to this calibration factor

  // Convert the reading to grams
  float weight_in_grams = scale.get_units() * 1000;

  Serial.print("Reading: ");
  Serial.print(weight_in_grams, 1); // Display weight in grams
  Serial.print(" g"); 
  Serial.print(" calibration_factor: ");
  Serial.print(calibration_factor);
  Serial.println();

  if (weight_in_grams >= 150) {
    Serial.println("ALERT: Bin is Full");  
  }

  delay(2000);

  // if (Serial.available()) {
  //   char temp = Serial.read();
  //   if (temp == '+' || temp == 'a')
  //     calibration_factor += 1000; // Increase calibration factor
  //   else if (temp == '-' || temp == 'z')
  //     calibration_factor -= 1000; // Decrease calibration factor
  // }
}
