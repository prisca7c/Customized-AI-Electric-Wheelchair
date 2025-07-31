Add ESP32 board support:
   - File → Preferences → Additional Board URLs
   - Add: https://dl.espressif.com/dl/package_esp32_index.json

Install libraries:
   - ArduinoJson by Benoit Blanchon
   - ESP32 BLE Arduino (comes with ESP32 core)




#include <WiFi.h>
#include <WebServer.h>
#include <ArduinoJson.h>
#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

const char* ssid = "MyWiFiNetwork";
const char* password = "MyPassword";

#define BLE_DEVICE_NAME "AI_Wheelchair"
#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHAR_UUID_TX "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define CHAR_UUID_RX "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

#define ATMEGA_SERIAL Serial1
#define RPI_SERIAL Serial
#define LED_WIFI 2
#define WAKE_WORD_PIN 3

WebServer server(80);
BLEServer* pServer = NULL;
BLECharacteristic* pTxChar;
bool deviceConnected = false;
bool oldDeviceConnected = false;

struct WheelchairStatus {
  float battery;
  int16_t speed1;
  int16_t speed2;
  float current1;
  float current2;
  uint16_t obstacleFront;
  uint16_t obstacleLeft;
  uint16_t obstacleRight;
  double latitude;
  double longitude;
  uint8_t satellites;
  uint8_t mode;
  bool emergency;
} status;

char atmegaBuffer[256];
uint8_t atmegaBufferIndex = 0;
char rpiBuffer[256];
uint8_t rpiBufferIndex = 0;

unsigned long lastWiFiCheck = 0;
unsigned long lastStatusRequest = 0;
unsigned long lastHeartbeat = 0;

class MyServerCallbacks: public BLEServerCallbacks {
  void onConnect(BLEServer* pServer) {
    deviceConnected = true;
  };
  
  void onDisconnect(BLEServer* pServer) {
    deviceConnected = false;
  }
};

class MyCallbacks: public BLECharacteristicCallbacks {
  void onWrite(BLECharacteristic *pCharacteristic) {
    std::string rxValue = pCharacteristic->getValue();
    if (rxValue.length() > 0) {
      for (int i = 0; i < rxValue.length(); i++) {
        ATMEGA_SERIAL.print(rxValue[i]);
      }
      ATMEGA_SERIAL.println();
    }
  }
};

void setup() {
  RPI_SERIAL.begin(115200);
  ATMEGA_SERIAL.begin(115200);
  
  pinMode(LED_WIFI, OUTPUT);
  pinMode(WAKE_WORD_PIN, OUTPUT);
  digitalWrite(WAKE_WORD_PIN, LOW);
  
  setupWiFi();
  setupBLE();
  setupWebServer();
}

void loop() {
  handleATmegaCommunication();
  handleRPiCommunication();
  handleBLE();
  server.handleClient();
  
  if (millis() - lastWiFiCheck >= 10000) {
    checkWiFiConnection();
    lastWiFiCheck = millis();
  }
  
  if (millis() - lastStatusRequest >= 500) {
    requestStatusFromATmega();
    lastStatusRequest = millis();
  }
  
  if (millis() - lastHeartbeat >= 1000) {
    sendHeartbeatToRPi();
    lastHeartbeat = millis();
  }
}

void setupWiFi() {
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    digitalWrite(LED_WIFI, !digitalRead(LED_WIFI));
    attempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    digitalWrite(LED_WIFI, HIGH);
  } else {
    digitalWrite(LED_WIFI, LOW);
  }
}

void checkWiFiConnection() {
  if (WiFi.status() != WL_CONNECTED) {
    digitalWrite(LED_WIFI, LOW);
    setupWiFi();
  } else {
    digitalWrite(LED_WIFI, HIGH);
  }
}

void setupBLE() {
  BLEDevice::init(BLE_DEVICE_NAME);
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  
  BLEService *pService = pServer->createService(SERVICE_UUID);
  
  pTxChar = pService->createCharacteristic(
    CHAR_UUID_TX,
    BLECharacteristic::PROPERTY_NOTIFY
  );
  pTxChar->addDescriptor(new BLE2902());
  
  BLECharacteristic * pRxChar = pService->createCharacteristic(
    CHAR_UUID_RX,
    BLECharacteristic::PROPERTY_WRITE
  );
  pRxChar->setCallbacks(new MyCallbacks());
  
  pService->start();
  pServer->getAdvertising()->start();
}

void handleBLE() {
  if (!deviceConnected && oldDeviceConnected) {
    delay(500);
    pServer->startAdvertising();
    oldDeviceConnected = deviceConnected;
  }
  
  if (deviceConnected && !oldDeviceConnected) {
    oldDeviceConnected = deviceConnected;
  }
  
  if (deviceConnected) {
    static unsigned long lastBLEUpdate = 0;
    if (millis() - lastBLEUpdate >= 1000) {
      sendStatusToBLE();
      lastBLEUpdate = millis();
    }
  }
}

void sendStatusToBLE() {
  char bleStatus[100];
  snprintf(bleStatus, sizeof(bleStatus), 
    "B:%.1f,S:%d,%d,O:%d,%d,%d",
    status.battery,
    status.speed1,
    status.speed2,
    status.obstacleFront,
    status.obstacleLeft,
    status.obstacleRight
  );
  
  pTxChar->setValue(bleStatus);
  pTxChar->notify();
}

void setupWebServer() {
  server.on("/", HTTP_GET, handleRoot);
  server.on("/status", HTTP_GET, handleStatus);
  server.on("/control", HTTP_POST, handleControl);
  server.on("/emergency", HTTP_POST, handleEmergencyStop);
  server.begin();
}

void handleRoot() {
  String html = "<!DOCTYPE html><html>";
  html += "<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">";
  html += "<title>AI Wheelchair Control</title>";
  html += "<style>";
  html += "body{font-family:Arial;text-align:center;background:#f0f0f0;}";
  html += ".container{max-width:600px;margin:auto;padding:20px;}";
  html += ".status{background:white;padding:20px;margin:10px;border-radius:10px;}";
  html += ".button{background:#4CAF50;color:white;padding:15px 30px;";
  html += "border:none;border-radius:5px;font-size:18px;margin:5px;cursor:pointer;}";
  html += ".button:hover{background:#45a049;}";
  html += ".emergency{background:#f44336;}";
  html += ".emergency:hover{background:#da190b;}";
  html += "</style></head><body>";
  html += "<div class=\"container\">";
  html += "<h1>AI Wheelchair Control</h1>";
  html += "<div class=\"status\">";
  html += "<h2>Status</h2>";
  html += "<p>Battery: <span id=\"battery\">--</span>V</p>";
  html += "<p>Speed: <span id=\"speed\">--</span></p>";
  html += "<p>Mode: <span id=\"mode\">--</span></p>";
  html += "<p>Obstacles: F:<span id=\"obstF\">--</span> ";
  html += "L:<span id=\"obstL\">--</span> R:<span id=\"obstR\">--</span></p>";
  html += "</div>";
  html += "<div class=\"controls\">";
  html += "<button class=\"button\" onclick=\"sendCommand('SPEED:0')\">Slow</button>";
  html += "<button class=\"button\" onclick=\"sendCommand('SPEED:1')\">Medium</button>";
  html += "<button class=\"button\" onclick=\"sendCommand('SPEED:2')\">Fast</button><br>";
  html += "<button class=\"button\" onclick=\"sendCommand('MODE:TOGGLE')\">Toggle Mode</button>";
  html += "<button class=\"button emergency\" onclick=\"emergency()\">EMERGENCY STOP</button>";
  html += "</div></div>";
  html += "<script>";
  html += "function updateStatus(){";
  html += "fetch('/status').then(r=>r.json()).then(data=>{";
  html += "document.getElementById('battery').textContent=data.battery.toFixed(1);";
  html += "document.getElementById('speed').textContent=data.speed1+','+data.speed2;";
  html += "document.getElementById('mode').textContent=data.mode==0?'Manual':'AI Assist';";
  html += "document.getElementById('obstF').textContent=data.obstacles.front;";
  html += "document.getElementById('obstL').textContent=data.obstacles.left;";
  html += "document.getElementById('obstR').textContent=data.obstacles.right;";
  html += "});}";
  html += "function sendCommand(cmd){fetch('/control',{method:'POST',body:cmd});}";
  html += "function emergency(){if(confirm('Emergency Stop?'))fetch('/emergency',{method:'POST'});}";
  html += "setInterval(updateStatus,1000);updateStatus();";
  html += "</script></body></html>";
  
  server.send(200, "text/html", html);
}

void handleStatus() {
  StaticJsonDocument<512> doc;
  doc["battery"] = status.battery;
  doc["speed1"] = status.speed1;
  doc["speed2"] = status.speed2;
  doc["current1"] = status.current1;
  doc["current2"] = status.current2;
  doc["mode"] = status.mode;
  doc["emergency"] = status.emergency;
  
  JsonObject obstacles = doc.createNestedObject("obstacles");
  obstacles["front"] = status.obstacleFront;
  obstacles["left"] = status.obstacleLeft;
  obstacles["right"] = status.obstacleRight;
  
  JsonObject gps = doc.createNestedObject("gps");
  gps["lat"] = status.latitude;
  gps["lon"] = status.longitude;
  gps["sats"] = status.satellites;
  
  String response;
  serializeJson(doc, response);
  server.send(200, "application/json", response);
}

void handleControl() {
  if (server.hasArg("plain")) {
    String command = server.arg("plain");
    ATMEGA_SERIAL.println(command);
    server.send(200, "text/plain", "OK");
  } else {
    server.send(400, "text/plain", "Bad Request");
  }
}

void handleEmergencyStop() {
  ATMEGA_SERIAL.println("STOP");
  server.send(200, "text/plain", "EMERGENCY STOP ACTIVATED");
}

void handleATmegaCommunication() {
  while (ATMEGA_SERIAL.available()) {
    char c = ATMEGA_SERIAL.read();
    
    if (c == '\n') {
      atmegaBuffer[atmegaBufferIndex] = '\0';
      processATmegaMessage(atmegaBuffer);
      atmegaBufferIndex = 0;
    } else if (atmegaBufferIndex < 255) {
      atmegaBuffer[atmegaBufferIndex++] = c;
    }
  }
}

void processATmegaMessage(char* msg) {
  RPI_SERIAL.print("ATMEGA:");
  RPI_SERIAL.println(msg);
  
  if (msg[0] == '{') {
    parseStatusJSON(msg);
  }
  else if (strncmp(msg, "ALERT:", 6) == 0) {
    handleAlert(msg + 6);
  }
}

void parseStatusJSON(char* json) {
  StaticJsonDocument<512> doc;
  DeserializationError error = deserializeJson(doc, json);
  
  if (!error) {
    status.battery = doc["battery"];
    status.speed1 = doc["speed1"];
    status.speed2 = doc["speed2"];
    status.current1 = doc["current1"];
    status.current2 = doc["current2"];
    status.obstacleFront = doc["obstacles"]["front"];
    status.obstacleLeft = doc["obstacles"]["left"];
    status.obstacleRight = doc["obstacles"]["right"];
    status.latitude = doc["gps"]["lat"];
    status.longitude = doc["gps"]["lon"];
    status.satellites = doc["gps"]["sats"];
    status.mode = doc["mode"];
    status.emergency = doc["emergency"];
  }
}

void handleAlert(char* alert) {
  RPI_SERIAL.print("ALERT:");
  RPI_SERIAL.println(alert);
}

void handleRPiCommunication() {
  while (RPI_SERIAL.available()) {
    char c = RPI_SERIAL.read();
    
    if (c == '\n') {
      rpiBuffer[rpiBufferIndex] = '\0';
      processRPiCommand(rpiBuffer);
      rpiBufferIndex = 0;
    } else if (rpiBufferIndex < 255) {
      rpiBuffer[rpiBufferIndex++] = c;
    }
  }
}

void processRPiCommand(char* cmd) {
  if (strncmp(cmd, "ATMEGA:", 7) == 0) {
    ATMEGA_SERIAL.println(cmd + 7);
  }
  else if (strncmp(cmd, "WAKE_WORD", 9) == 0) {
    handleWakeWord();
  }
  else if (strncmp(cmd, "NAV:", 4) == 0) {
    ATMEGA_SERIAL.print("GOTO:");
    ATMEGA_SERIAL.println(cmd + 4);
  }
  else if (strcmp(cmd, "REBOOT") == 0) {
    ESP.restart();
  }
}

void handleWakeWord() {
  digitalWrite(WAKE_WORD_PIN, HIGH);
  delay(100);
  digitalWrite(WAKE_WORD_PIN, LOW);
  ATMEGA_SERIAL.println("AI:ACTIVE");
}

void requestStatusFromATmega() {
  ATMEGA_SERIAL.println("STATUS?");
}

void sendHeartbeatToRPi() {
  RPI_SERIAL.println("HEARTBEAT");
  
  if (WiFi.status() == WL_CONNECTED) {
    RPI_SERIAL.print("WIFI:");
    RPI_SERIAL.println(WiFi.localIP());
  } else {
    RPI_SERIAL.println("WIFI:DISCONNECTED");
  }
  
  RPI_SERIAL.print("BLE:");
  RPI_SERIAL.println(deviceConnected ? "CONNECTED" : "WAITING");
}
