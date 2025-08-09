#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

int soundSensor = 2;
int clapCount = 0;
unsigned long lastClapTime = 0;
unsigned long clapTimeout = 2000; // 2 sec reset
bool lastSoundState = LOW; // To track changes

void setup() {
  pinMode(soundSensor, INPUT);
  lcd.init();
  lcd.backlight();
  Serial.begin(9600);
  lcd.setCursor(0,0);
  lcd.print("Waiting...");
}

void loop() {
  bool soundState = digitalRead(soundSensor);

  // Detect rising edge (LOW -> HIGH)
  if (soundState == HIGH && lastSoundState == LOW) {
    unsigned long now = millis();
    if (now - lastClapTime > 150) { // debounce 150 ms
      clapCount++;
      displayClapCount();
      lastClapTime = now;
    }
  }
  lastSoundState = soundState;

  // Reset after timeout
  if (millis() - lastClapTime > clapTimeout && clapCount > 0) {
    clapCount = 0;
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("Silent mode");
    lcd.setCursor(0,1);
    lcd.print("Claps: 0");
  }
}

void displayClapCount() {
  lcd.clear();
  lcd.setCursor(0,0);
  lcd.print("Claps detected");
  lcd.setCursor(0,1);
  lcd.print("Claps: ");
  lcd.print(clapCount);
  Serial.println(clapCount);
}
