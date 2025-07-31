# In Arduino IDE Library Manager, install:
- MPU6050 by Electronic Cats
- RTClib by Adafruit
- TinyGPSPlus by Mikal Hart
- NewPing by Tim Eckel




#include <Wire.h>
#include <MPU6050.h>
#include <RTClib.h>
#include <TinyGPS++.h>
#include <NewPing.h>

#define MOTOR1_RPWM 2
#define MOTOR1_LPWM 3
#define MOTOR1_R_EN 4
#define MOTOR1_L_EN 5
#define MOTOR1_R_IS A0
#define MOTOR1_L_IS A1
#define MOTOR2_RPWM 6
#define MOTOR2_LPWM 7
#define MOTOR2_R_EN 8
#define MOTOR2_L_EN 9
#define MOTOR2_R_IS A2
#define MOTOR2_L_IS A3
#define JOYSTICK_X A4
#define JOYSTICK_Y A5
#define JOYSTICK_BTN 22
#define BTN_EMERGENCY 23
#define BTN_SPEED_UP 24
#define BTN_SPEED_DOWN 25
#define BTN_MODE 26
#define BTN_HORN 27
#define BTN_LIGHTS 28
#define BTN_AI_ASSIST 29
#define BTN_CUSTOM1 30
#define BTN_CUSTOM2 31
#define TRIG_FRONT 32
#define ECHO_FRONT 33
#define TRIG_LEFT 34
#define ECHO_LEFT 35
#define TRIG_RIGHT 36
#define ECHO_RIGHT 37
#define BATTERY_VOLTAGE A6
#define FAN_CONTROL 38
#define LED_STATUS 39
#define BUZZER 40
#define ESP32_RX 16
#define ESP32_TX 17
#define GPS_RX 18
#define GPS_TX 19

#define SPEED_SLOW 100
#define SPEED_MEDIUM 180
#define SPEED_FAST 255
#define OBSTACLE_STOP_CM 30
#define OBSTACLE_SLOW_CM 100
#define MOTOR_CURRENT_LIMIT 30.0
#define BATTERY_LOW_VOLTAGE 22.0
#define BATTERY_CRITICAL 20.0
#define JOYSTICK_DEADZONE 50
#define JOYSTICK_CENTER 512
#define RAMP_RATE 5
#define TURN_RATE_FACTOR 0.7

MPU6050 mpu;
RTC_DS3231 rtc;
TinyGPSPlus gps;
NewPing sonarFront(TRIG_FRONT, ECHO_FRONT, 400);
NewPing sonarLeft(TRIG_LEFT, ECHO_LEFT, 400);
NewPing sonarRight(TRIG_RIGHT, ECHO_RIGHT, 400);

bool emergencyStop = false;
bool systemReady = false;
uint8_t speedMode = 1;
uint8_t controlMode = 0;
bool lightsOn = false;
bool fanOn = false;

int16_t currentSpeed1 = 0;
int16_t currentSpeed2 = 0;
int16_t targetSpeed1 = 0;
int16_t targetSpeed2 = 0;

float batteryVoltage = 24.0;
float motor1Current = 0.0;
float motor2Current = 0.0;
int16_t accelX, accelY, accelZ;
int16_t gyroX, gyroY, gyroZ;
uint16_t distanceFront = 400;
uint16_t distanceLeft = 400;
uint16_t distanceRight = 400;

double latitude = 0.0;
double longitude = 0.0;
float gpsSpeed = 0.0;
uint8_t satellites = 0;

unsigned long lastMotorUpdate = 0;
unsigned long lastSensorRead = 0;
unsigned long lastBatteryCheck = 0;
unsigned long lastGPSRead = 0;
unsigned long lastStatusBlink = 0;

char espBuffer[100];
uint8_t espBufferIndex = 0;

void setup() {
  Serial.begin(115200);
  Serial1.begin(9600);
  Serial2.begin(115200);
  
  pinMode(MOTOR1_RPWM, OUTPUT);
  pinMode(MOTOR1_LPWM, OUTPUT);
  pinMode(MOTOR1_R_EN, OUTPUT);
  pinMode(MOTOR1_L_EN, OUTPUT);
  pinMode(MOTOR2_RPWM, OUTPUT);
  pinMode(MOTOR2_LPWM, OUTPUT);
  pinMode(MOTOR2_R_EN, OUTPUT);
  pinMode(MOTOR2_L_EN, OUTPUT);
  
  digitalWrite(MOTOR1_R_EN, HIGH);
  digitalWrite(MOTOR1_L_EN, HIGH);
  digitalWrite(MOTOR2_R_EN, HIGH);
  digitalWrite(MOTOR2_L_EN, HIGH);
  
  pinMode(BTN_EMERGENCY, INPUT_PULLUP);
  pinMode(BTN_SPEED_UP, INPUT_PULLUP);
  pinMode(BTN_SPEED_DOWN, INPUT_PULLUP);
  pinMode(BTN_MODE, INPUT_PULLUP);
  pinMode(BTN_HORN, INPUT_PULLUP);
  pinMode(BTN_LIGHTS, INPUT_PULLUP);
  pinMode(BTN_AI_ASSIST, INPUT_PULLUP);
  pinMode(BTN_CUSTOM1, INPUT_PULLUP);
  pinMode(BTN_CUSTOM2, INPUT_PULLUP);
  pinMode(JOYSTICK_BTN, INPUT_PULLUP);
  
  pinMode(FAN_CONTROL, OUTPUT);
  pinMode(LED_STATUS, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  
  Wire.begin();
  mpu.initialize();
  rtc.begin();
  
  tone(BUZZER, 1000, 200);
  delay(200);
  tone(BUZZER, 1500, 200);
  
  systemReady = true;
}

void loop() {
  if (digitalRead(BTN_EMERGENCY) == LOW) {
    emergencyStop = true;
    stopMotors();
  }
  
  handleButtons();
  
  if (millis() - lastSensorRead >= 20) {
    readSensors();
    lastSensorRead = millis();
  }
  
  if (millis() - lastMotorUpdate >= 10 && !emergencyStop) {
    updateMotorControl();
    lastMotorUpdate = millis();
  }
  
  if (millis() - lastBatteryCheck >= 1000) {
    checkBattery();
    lastBatteryCheck = millis();
  }
  
  if (millis() - lastGPSRead >= 200) {
    updateGPS();
    lastGPSRead = millis();
  }
  
  handleESP32Communication();
  updateStatusLED();
  manageCooling();
}

void updateMotorControl() {
  int joyX = analogRead(JOYSTICK_X);
  int joyY = analogRead(JOYSTICK_Y);
  
  if (abs(joyX - JOYSTICK_CENTER) < JOYSTICK_DEADZONE) joyX = JOYSTICK_CENTER;
  if (abs(joyY - JOYSTICK_CENTER) < JOYSTICK_DEADZONE) joyY = JOYSTICK_CENTER;
  
  int16_t xSpeed = map(joyX, 0, 1023, -255, 255);
  int16_t ySpeed = map(joyY, 0, 1023, -255, 255);
  
  int maxSpeed = SPEED_MEDIUM;
  switch(speedMode) {
    case 0: maxSpeed = SPEED_SLOW; break;
    case 1: maxSpeed = SPEED_MEDIUM; break;
    case 2: maxSpeed = SPEED_FAST; break;
  }
  
  targetSpeed1 = constrain(ySpeed + (xSpeed * TURN_RATE_FACTOR), -maxSpeed, maxSpeed);
  targetSpeed2 = constrain(ySpeed - (xSpeed * TURN_RATE_FACTOR), -maxSpeed, maxSpeed);
  
  if (controlMode == 1) {
    applyObstacleAvoidance();
  }
  
  if (currentSpeed1 < targetSpeed1) {
    currentSpeed1 = min(currentSpeed1 + RAMP_RATE, targetSpeed1);
  } else if (currentSpeed1 > targetSpeed1) {
    currentSpeed1 = max(currentSpeed1 - RAMP_RATE, targetSpeed1);
  }
  
  if (currentSpeed2 < targetSpeed2) {
    currentSpeed2 = min(currentSpeed2 + RAMP_RATE, targetSpeed2);
  } else if (currentSpeed2 > targetSpeed2) {
    currentSpeed2 = max(currentSpeed2 - RAMP_RATE, targetSpeed2);
  }
  
  if (motor1Current > MOTOR_CURRENT_LIMIT || motor2Current > MOTOR_CURRENT_LIMIT) {
    currentSpeed1 = currentSpeed1 * 0.8;
    currentSpeed2 = currentSpeed2 * 0.8;
    tone(BUZZER, 2000, 100);
  }
  
  setMotor1Speed(currentSpeed1);
  setMotor2Speed(currentSpeed2);
}

void setMotor1Speed(int16_t speed) {
  if (speed > 0) {
    analogWrite(MOTOR1_RPWM, speed);
    analogWrite(MOTOR1_LPWM, 0);
  } else if (speed < 0) {
    analogWrite(MOTOR1_RPWM, 0);
    analogWrite(MOTOR1_LPWM, -speed);
  } else {
    analogWrite(MOTOR1_RPWM, 0);
    analogWrite(MOTOR1_LPWM, 0);
  }
}

void setMotor2Speed(int16_t speed) {
  if (speed > 0) {
    analogWrite(MOTOR2_RPWM, speed);
    analogWrite(MOTOR2_LPWM, 0);
  } else if (speed < 0) {
    analogWrite(MOTOR2_RPWM, 0);
    analogWrite(MOTOR2_LPWM, -speed);
  } else {
    analogWrite(MOTOR2_RPWM, 0);
    analogWrite(MOTOR2_LPWM, 0);
  }
}

void stopMotors() {
  currentSpeed1 = 0;
  currentSpeed2 = 0;
  targetSpeed1 = 0;
  targetSpeed2 = 0;
  setMotor1Speed(0);
  setMotor2Speed(0);
}

void readSensors() {
  static uint8_t sensorIndex = 0;
  switch(sensorIndex) {
    case 0:
      distanceFront = sonarFront.ping_cm();
      if (distanceFront == 0) distanceFront = 400;
      break;
    case 1:
      distanceLeft = sonarLeft.ping_cm();
      if (distanceLeft == 0) distanceLeft = 400;
      break;
    case 2:
      distanceRight = sonarRight.ping_cm();
      if (distanceRight == 0) distanceRight = 400;
      break;
  }
  sensorIndex = (sensorIndex + 1) % 3;
  
  static uint8_t mpuCounter = 0;
  if (++mpuCounter >= 3) {
    mpuCounter = 0;
    mpu.getMotion6(&accelX, &accelY, &accelZ, &gyroX, &gyroY, &gyroZ);
  }
  
  int raw1 = analogRead(MOTOR1_R_IS) + analogRead(MOTOR1_L_IS);
  int raw2 = analogRead(MOTOR2_R_IS) + analogRead(MOTOR2_L_IS);
  motor1Current = (raw1 / 2.0) * (43.0 / 1023.0);
  motor2Current = (raw2 / 2.0) * (43.0 / 1023.0);
}

void checkBattery() {
  int rawADC = analogRead(BATTERY_VOLTAGE);
  batteryVoltage = rawADC * (5.0 / 1023.0) * 5.68;
  
  if (batteryVoltage < BATTERY_CRITICAL) {
    emergencyStop = true;
    tone(BUZZER, 500, 1000);
  } else if (batteryVoltage < BATTERY_LOW_VOLTAGE) {
    static unsigned long lastWarning = 0;
    if (millis() - lastWarning > 10000) {
      tone(BUZZER, 1000, 200);
      lastWarning = millis();
    }
  }
}

void updateGPS() {
  while (Serial1.available()) {
    if (gps.encode(Serial1.read())) {
      if (gps.location.isValid()) {
        latitude = gps.location.lat();
        longitude = gps.location.lng();
      }
      if (gps.speed.isValid()) {
        gpsSpeed = gps.speed.kmph();
      }
      satellites = gps.satellites.value();
    }
  }
}

void applyObstacleAvoidance() {
  if (distanceFront < OBSTACLE_STOP_CM) {
    if (targetSpeed1 > 0 && targetSpeed2 > 0) {
      targetSpeed1 = 0;
      targetSpeed2 = 0;
      tone(BUZZER, 2000, 200);
    }
  }
  else if (distanceFront < OBSTACLE_SLOW_CM) {
    if (targetSpeed1 > 0 && targetSpeed2 > 0) {
      float factor = (float)distanceFront / OBSTACLE_SLOW_CM;
      targetSpeed1 *= factor;
      targetSpeed2 *= factor;
    }
  }
  
  if (distanceLeft < OBSTACLE_SLOW_CM && targetSpeed1 > targetSpeed2) {
    targetSpeed1 = targetSpeed2;
  }
  if (distanceRight < OBSTACLE_SLOW_CM && targetSpeed2 > targetSpeed1) {
    targetSpeed2 = targetSpeed1;
  }
}

void handleButtons() {
  static unsigned long lastDebounce[10] = {0};
  unsigned long now = millis();
  
  if (digitalRead(BTN_SPEED_UP) == LOW && now - lastDebounce[0] > 200) {
    lastDebounce[0] = now;
    if (speedMode < 2) {
      speedMode++;
      tone(BUZZER, 1500, 100);
    }
  }
  
  if (digitalRead(BTN_SPEED_DOWN) == LOW && now - lastDebounce[1] > 200) {
    lastDebounce[1] = now;
    if (speedMode > 0) {
      speedMode--;
      tone(BUZZER, 1000, 100);
    }
  }
  
  if (digitalRead(BTN_MODE) == LOW && now - lastDebounce[2] > 500) {
    lastDebounce[2] = now;
    controlMode = !controlMode;
    tone(BUZZER, controlMode ? 2000 : 1000, 200);
  }
  
  if (digitalRead(BTN_HORN) == LOW) {
    tone(BUZZER, 440, 0);
  } else {
    noTone(BUZZER);
  }
  
  if (digitalRead(BTN_LIGHTS) == LOW && now - lastDebounce[3] > 200) {
    lastDebounce[3] = now;
    lightsOn = !lightsOn;
    Serial2.println(lightsOn ? "LIGHTS:ON" : "LIGHTS:OFF");
  }
  
  if (digitalRead(BTN_AI_ASSIST) == LOW && now - lastDebounce[4] > 500) {
    lastDebounce[4] = now;
    Serial2.println("AI:WAKE");
    tone(BUZZER, 2000, 100);
    delay(100);
    tone(BUZZER, 2500, 100);
  }
  
  if (digitalRead(BTN_CUSTOM1) == LOW && now - lastDebounce[5] > 200) {
    lastDebounce[5] = now;
    fanOn = !fanOn;
    digitalWrite(FAN_CONTROL, fanOn);
  }
  
  if (digitalRead(BTN_CUSTOM2) == LOW && digitalRead(JOYSTICK_BTN) == LOW) {
    if (emergencyStop && now - lastDebounce[6] > 1000) {
      lastDebounce[6] = now;
      emergencyStop = false;
      tone(BUZZER, 1000, 100);
      delay(150);
      tone(BUZZER, 1500, 100);
    }
  }
}

void handleESP32Communication() {
  while (Serial2.available()) {
    char c = Serial2.read();
    if (c == '\n') {
      espBuffer[espBufferIndex] = '\0';
      processESP32Command(espBuffer);
      espBufferIndex = 0;
    } else if (espBufferIndex < 99) {
      espBuffer[espBufferIndex++] = c;
    }
  }
  
  static unsigned long lastStatusUpdate = 0;
  if (millis() - lastStatusUpdate >= 100) {
    lastStatusUpdate = millis();
    sendStatusToESP32();
  }
}

void processESP32Command(char* cmd) {
  if (strncmp(cmd, "MOVE:", 5) == 0) {
    int x, y;
    if (sscanf(cmd + 5, "%d,%d", &x, &y) == 2) {
      // Override implementation
    }
  }
  else if (strcmp(cmd, "STOP") == 0) {
    emergencyStop = true;
    stopMotors();
  }
  else if (strncmp(cmd, "SPEED:", 6) == 0) {
    int newSpeed = atoi(cmd + 6);
    speedMode = constrain(newSpeed, 0, 2);
  }
  else if (strcmp(cmd, "STATUS?") == 0) {
    sendStatusToESP32();
  }
  else if (strncmp(cmd, "GOTO:", 5) == 0) {
    double targetLat, targetLon;
    if (sscanf(cmd + 5, "%lf,%lf", &targetLat, &targetLon) == 2) {
      // Navigation implementation
    }
  }
}

void sendStatusToESP32() {
  Serial2.print("{");
  Serial2.print("\"battery\":");
  Serial2.print(batteryVoltage);
  Serial2.print(",\"speed1\":");
  Serial2.print(currentSpeed1);
  Serial2.print(",\"speed2\":");
  Serial2.print(currentSpeed2);
  Serial2.print(",\"current1\":");
  Serial2.print(motor1Current);
  Serial2.print(",\"current2\":");
  Serial2.print(motor2Current);
  Serial2.print(",\"obstacles\":{");
  Serial2.print("\"front\":");
  Serial2.print(distanceFront);
  Serial2.print(",\"left\":");
  Serial2.print(distanceLeft);
  Serial2.print(",\"right\":");
  Serial2.print(distanceRight);
  Serial2.print("},\"gps\":{");
  Serial2.print("\"lat\":");
  Serial2.print(latitude, 6);
  Serial2.print(",\"lon\":");
  Serial2.print(longitude, 6);
  Serial2.print(",\"sats\":");
  Serial2.print(satellites);
  Serial2.print("},\"mode\":");
  Serial2.print(controlMode);
  Serial2.print(",\"emergency\":");
  Serial2.print(emergencyStop ? "true" : "false");
  Serial2.println("}");
}

void updateStatusLED() {
  static bool ledState = false;
  unsigned long now = millis();
  
  if (emergencyStop) {
    if (now - lastStatusBlink >= 100) {
      ledState = !ledState;
      digitalWrite(LED_STATUS, ledState);
      lastStatusBlink = now;
    }
  }
  else if (!systemReady) {
    if (now - lastStatusBlink >= 1000) {
      ledState = !ledState;
      digitalWrite(LED_STATUS, ledState);
      lastStatusBlink = now;
    }
  }
  else if (batteryVoltage < BATTERY_LOW_VOLTAGE) {
    static uint8_t blinkCount = 0;
    if (now - lastStatusBlink >= 200) {
      if (blinkCount < 4) {
        ledState = !ledState;
        digitalWrite(LED_STATUS, ledState);
        blinkCount++;
      } else if (blinkCount >= 10) {
        blinkCount = 0;
      } else {
        blinkCount++;
      }
      lastStatusBlink = now;
    }
  }
  else {
    digitalWrite(LED_STATUS, HIGH);
  }
}

void manageCooling() {
  bool shouldFanRun = (motor1Current > 10.0 || motor2Current > 10.0) || fanOn;
  
  static bool fanRunning = false;
  static unsigned long fanChangeTime = 0;
  
  if (shouldFanRun && !fanRunning && millis() - fanChangeTime > 5000) {
    fanRunning = true;
    digitalWrite(FAN_CONTROL, HIGH);
    fanChangeTime = millis();
  }
  else if (!shouldFanRun && fanRunning && millis() - fanChangeTime > 30000) {
    fanRunning = false;
    digitalWrite(FAN_CONTROL, LOW);
    fanChangeTime = millis();
  }
}
