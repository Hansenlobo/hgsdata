#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Keypad.h>
#include <WiFi.h>
#include <HTTPClient.h>

// Replace with your SSID and Password
const char* ssid = "TP-xxxxxxxxxxxxxxxxxxxxxx";
const char* password = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx*";

// Supabase endpoint and API key
const char* supabaseEndpoint = "https://xxxxxxxxxxxxxxxx.supabase.co/rest/v1/dts";
const char* supabaseApiKey = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx";
LiquidCrystal_I2C lcd(0x27, 16, 2);  // Address 0x27 for a 16x2 LCD
bool inWelcomeScreen = true;

#define ROW_NUM     4 // four rows
#define COLUMN_NUM  4
char keys[ROW_NUM][COLUMN_NUM] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};
byte pin_rows[ROW_NUM]      = {19, 18, 5, 17}; // GPIO19, GPIO18, GPIO5, GPIO17 connect to the row pins
byte pin_column[COLUMN_NUM] = {16, 4, 0, 2};   // Connect to the column pinouts of the keypad
Keypad keypad = Keypad( makeKeymap(keys), pin_rows, pin_column, ROW_NUM, COLUMN_NUM );


String inputString = "";

void setup() {
  Serial.begin(115200);
  lcd.init();
  lcd.backlight();
  connectWiFi();
  displayWelcome();
}

void loop() {
  if (inWelcomeScreen) {
    if (keypad.getKey()) {
      inWelcomeScreen = false;
      lcd.clear();
    }
  } else {
    char key = keypad.getKey();
    if (key) {
      if (key == 'C') {
        sendDataToSupabase(inputString, "Credited");
        inWelcomeScreen = true; // Return to the welcome screen after sending data
        lcd.clear();
        displayWelcome();
      } else if (key == 'D') {
        sendDataToSupabase(inputString, "Debited");
        inWelcomeScreen = true; // Return to the welcome screen after sending data
        lcd.clear();
        displayWelcome();
      } else {
        inputString += key;
      }

      lcd.clear(); // Clear the LCD
      lcd.setCursor(0, 0);
      lcd.print("Key Pressed:");
      lcd.setCursor(0, 1);
      lcd.print(inputString);
    }
  }
}

void connectWiFi() {
  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void displayWelcome() {
  lcd.clear(); // Clear the LCD
  lcd.setCursor(0, 0);
  lcd.print("HGS SALES");
}
void sendDataToSupabase(String data,String transactionType) {
  if (data.isEmpty()) {
    // Don't send empty data
    return;
  }
  HTTPClient http;
  String jsonData = "{\"Transaction Type\":\"" + transactionType + "\", \"Amount\":\"" + data + "\"}";
  
  http.begin(supabaseEndpoint);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("apikey", supabaseApiKey);
  
  int httpResponseCode = http.POST(jsonData);
  
 if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("HTTP Response Code: " + String(httpResponseCode));
    Serial.println("Response: " + response);
    
    lcd.clear(); // Clear the LCD
    lcd.setCursor(0, 0);
    lcd.print("Data Sent!");
    lcd.setCursor(0, 1);
    lcd.print("Amount - " + data);
    delay(3000);
  } else {
    Serial.println("Error on HTTP request");
    lcd.clear(); // Clear the LCD
    lcd.setCursor(0, 0);
    lcd.print("Error Sending Data");
  }
  
  http.end();
  inputString = "";
}
