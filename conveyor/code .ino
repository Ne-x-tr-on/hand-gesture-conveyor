const int ledPin = 13; // Change if using other output
String command;

void setup() {
  pinMode(ledPin, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    command = Serial.readStringUntil('\n');
    command.trim(); // Remove any whitespace or newline

    if (command == "ON") {
      digitalWrite(ledPin, HIGH);
    } else if (command == "OFF") {
      digitalWrite(ledPin, LOW);
    }
  }
}
