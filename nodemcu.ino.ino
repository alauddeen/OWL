#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <Servo.h>
#include <ArduinoJson.h>

const char* ssid = "Kartik";        // Replace with your WiFi SSID
const char* password = "12345678";     // Replace with your WiFi password

ESP8266WebServer server(80);

Servo servo1; // First servo motor
Servo servo2; // Second servo motor

const int servo1Pin = D6; // GPIO pin for the first servo
const int servo2Pin = D8; // GPIO pin for the second servo

int positionServo1 = 90;  // Middle position for servo1
int positionServo2 = 90;  // Middle position for servo2

// const int turnStep = 40;  // Degrees to turn for turn commands
// const int moveStep = 40;  // Degrees to move for move commands

void setup() {
  Serial.begin(115200);
  servo1.attach(servo1Pin);
  servo2.attach(servo2Pin);

  Serial.println("Connecting to WiFi...");

  WiFi.begin(ssid, password);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 40) { // Try to connect for a certain number of attempts
    delay(1000); // Wait a second between attempts
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("");
    Serial.println("Failed to connect to WiFi. Please check your credentials and signal strength.");
    return; // Stop further execution if not connected to WiFi
  }

  Serial.println("");
  Serial.println("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/command", handleCommand);

  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}

void handleCommand() {
  // Debug: print all headers
  //Serial.println("Received headers:");
  for (int i = 0; i < server.headers(); i++) {
    Serial.print(server.headerName(i));
    Serial.print(": ");
    Serial.println(server.header(i));
  }
  
  if (server.hasArg("plain")) {
    String data = server.arg("plain");
    Serial.print("Received data: ");
    Serial.println(data);

    StaticJsonDocument<200> doc;
    DeserializationError error = deserializeJson(doc, data);

    if (!error) {
      if (doc.containsKey("command")) {
        int command = doc["command"];
        Serial.print("Executing command: ");
        Serial.println(command);

        executeCommand(command);
        server.send(200, "application/json", "{\"status\":\"success\"}");
      } else {
        Serial.println("JSON does not contain 'command' key.");
        server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"JSON does not contain 'command' key.\"}");
      }
    } else {
      Serial.print("deserializeJson() failed: ");
      Serial.println(error.c_str());

      server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"Invalid JSON format\"}");
    }
  } else {
    server.send(400, "application/json", "{\"status\":\"error\",\"message\":\"No data received\"}");
  }
}

void executeCommand(int command) {
  // Define smaller steps for precise movement
  const int turnStep = 5;
  const int moveStep = 5;
  // Define delay duration after each command execution
  const int commandDelay = 50; // milliseconds
  switch (command) {
    case 200: // Turn right
      positionServo1 += turnStep;
      positionServo2 += turnStep;
      break;
    case 400: // Turn left
      positionServo1 -= turnStep;
      positionServo2 -= turnStep;
      break;
    case 100: // Move forward
      positionServo1 -= moveStep;
      positionServo2 += moveStep;
      break;
    case 300: // Move backward
      positionServo1 += moveStep;
      positionServo2 -= moveStep;
      break;
    default:
      Serial.print("Unknown command: ");
      Serial.println(command);
      return; // Exit the function if the command is not recognized
  }
  
  // Constrain servo positions to valid range (0 to 180 degrees)
  positionServo1 = constrain(positionServo1, 0, 180);
  positionServo2 = constrain(positionServo2, 0, 180);

  // Update servo positions
  servo1.write(positionServo1);
  servo2.write(positionServo2);
}