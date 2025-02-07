#include <SoftwareSerial.h>

// Define the relay pins (same as before)
const int relayPins[] = {4, 5, 6, 7, 8, 9, 10, 11, 12, A0, A1, A2};

// Define Bluetooth serial connection pins
SoftwareSerial BTSerial(2, 3);  // RX, TX (Arduino Pin 2 -> RX of HC-06, Pin 3 -> TX of HC-06)

void setup() {
  // Set all relay pins as OUTPUT
  for (int i = 0; i < 12; i++) {
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], HIGH); // Initialize all relays to OFF
    
  }
  Serial.begin(9600);
  // Start Bluetooth serial communication
  BTSerial.begin(9600);
  BTSerial.println("Bluetooth Control for 12-Channel Relay Module");
  BTSerial.println("Enter a number between 1 and 8 to trigger the corresponding relay or pattern.");
}

void loop() {
  // Check if data is available from the Bluetooth module
  if (BTSerial.available() > 0) {
    int input = BTSerial.parseInt();  // Read the number input from the Bluetooth module
    Serial.println(input);
    // Trigger corresponding light pattern based on input
    switch (input) {
      case 1:
        light_pattern_1();
        Serial.println("Pattern 1 activated.");
        break;
      case 2:
        light_pattern_2();
        Serial.println("Pattern 2 activated.");
        break;
      case 3:
        light_pattern_3();
        Serial.println("Pattern 3 activated.");
        break;
      case 4:
        light_pattern_4();
        Serial.println("Pattern 4 activated.");
        break;
      case 5:
        light_pattern_5();
        Serial.println("Pattern 5 activated.");
        break;
      case 6:
        light_pattern_6();
        Serial.println("Pattern 6 activated.");
        break;
      case 7:
        light_pattern_7();
        Serial.println("Pattern 7 activated.");
        break;
      case 8:
        light_pattern_8();
        Serial.println("Pattern 8 activated.");
        break;
      default:
        BTSerial.println("Invalid number. Please enter a number between 1 and 8.");
        break;
    }
  }
}

void light_pattern_1(){
  digitalWrite(relayPins[0], HIGH);
  digitalWrite(relayPins[1], HIGH);
  digitalWrite(relayPins[2], LOW);

  digitalWrite(relayPins[3], LOW);
  digitalWrite(relayPins[4], HIGH);
  digitalWrite(relayPins[5], HIGH);

  digitalWrite(relayPins[6], LOW);
  digitalWrite(relayPins[7], HIGH);
  digitalWrite(relayPins[8], HIGH);

  digitalWrite(relayPins[9], LOW);
  digitalWrite(relayPins[10], HIGH);
  digitalWrite(relayPins[11], HIGH);
}

void light_pattern_2(){
  digitalWrite(relayPins[0], HIGH);
  digitalWrite(relayPins[1], LOW);
  digitalWrite(relayPins[2], HIGH);

  digitalWrite(relayPins[3], LOW);
  digitalWrite(relayPins[4], HIGH);
  digitalWrite(relayPins[5], HIGH);

  digitalWrite(relayPins[6], LOW);
  digitalWrite(relayPins[7], HIGH);
  digitalWrite(relayPins[8], HIGH);

  digitalWrite(relayPins[9], LOW);
  digitalWrite(relayPins[10], HIGH);
  digitalWrite(relayPins[11], HIGH);
}


void light_pattern_3(){
  digitalWrite(relayPins[0], LOW);
  digitalWrite(relayPins[1], HIGH);
  digitalWrite(relayPins[2], HIGH);

  digitalWrite(relayPins[3], HIGH);
  digitalWrite(relayPins[4], HIGH);
  digitalWrite(relayPins[5], LOW);

  digitalWrite(relayPins[6], LOW);
  digitalWrite(relayPins[7], HIGH);
  digitalWrite(relayPins[8], HIGH);

  digitalWrite(relayPins[9], LOW);
  digitalWrite(relayPins[10], HIGH);
  digitalWrite(relayPins[11], HIGH);
}

void light_pattern_4(){
  digitalWrite(relayPins[0], LOW);
  digitalWrite(relayPins[1], HIGH);
  digitalWrite(relayPins[2], HIGH);

  digitalWrite(relayPins[3], HIGH);
  digitalWrite(relayPins[4], LOW);
  digitalWrite(relayPins[5], HIGH);

  digitalWrite(relayPins[6], LOW);
  digitalWrite(relayPins[7], HIGH);
  digitalWrite(relayPins[8], HIGH);

  digitalWrite(relayPins[9], LOW);
  digitalWrite(relayPins[10], HIGH);
  digitalWrite(relayPins[11], HIGH);
}

void light_pattern_5(){
  digitalWrite(relayPins[0], LOW);
  digitalWrite(relayPins[1], HIGH);
  digitalWrite(relayPins[2], HIGH);

  digitalWrite(relayPins[3], LOW);
  digitalWrite(relayPins[4], HIGH);
  digitalWrite(relayPins[5], HIGH);

  digitalWrite(relayPins[6], HIGH);
  digitalWrite(relayPins[7], HIGH);
  digitalWrite(relayPins[8], LOW);

  digitalWrite(relayPins[9], LOW);
  digitalWrite(relayPins[10], HIGH);
  digitalWrite(relayPins[11], HIGH);
}

void light_pattern_6(){
  digitalWrite(relayPins[0], LOW);
  digitalWrite(relayPins[1], HIGH);
  digitalWrite(relayPins[2], HIGH);

  digitalWrite(relayPins[3], LOW);
  digitalWrite(relayPins[4], HIGH);
  digitalWrite(relayPins[5], HIGH);

  digitalWrite(relayPins[6], HIGH);
  digitalWrite(relayPins[7], LOW);
  digitalWrite(relayPins[8], HIGH);

  digitalWrite(relayPins[9], LOW);
  digitalWrite(relayPins[10], HIGH);
  digitalWrite(relayPins[11], HIGH);
}


void light_pattern_7(){
  digitalWrite(relayPins[0], LOW);
  digitalWrite(relayPins[1], HIGH);
  digitalWrite(relayPins[2], HIGH);

  digitalWrite(relayPins[3], LOW);
  digitalWrite(relayPins[4], HIGH);
  digitalWrite(relayPins[5], HIGH);

  digitalWrite(relayPins[6], LOW);
  digitalWrite(relayPins[7], HIGH);
  digitalWrite(relayPins[8], HIGH);

  digitalWrite(relayPins[9], HIGH);
  digitalWrite(relayPins[10], HIGH);
  digitalWrite(relayPins[11], LOW);
}

void light_pattern_8(){
  digitalWrite(relayPins[0], LOW);
  digitalWrite(relayPins[1], HIGH);
  digitalWrite(relayPins[2], HIGH);

  digitalWrite(relayPins[3], LOW);
  digitalWrite(relayPins[4], HIGH);
  digitalWrite(relayPins[5], HIGH);

  digitalWrite(relayPins[6], LOW);
  digitalWrite(relayPins[7], HIGH);
  digitalWrite(relayPins[8], HIGH);

  digitalWrite(relayPins[9], HIGH);
  digitalWrite(relayPins[10], LOW);
  digitalWrite(relayPins[11], HIGH);
}






