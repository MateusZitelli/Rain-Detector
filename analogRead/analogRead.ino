//(c) 2012 metamaquina.com.br Licensed under GPLv3 or later
void setup() {
  Serial.begin(9600);
}

void loop() {
  int sensorValue = analogRead(A5);
  Serial.println(sensorValue);
}
