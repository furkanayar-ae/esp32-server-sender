#include <WiFi.h>
#include <HTTPClient.h>

// Telefonunun veya kullandığın ağın Wi-Fi adı ve şifresi
const char* ssid = "iPhone 15 pro";
const char* password = "furk4nn12";

// Bilgisayarının IP adresi ve Python sunucusunun portu
const char* serverName = "http://172.20.10.14:3000"; 

unsigned long lastTime = 0;
unsigned long timerDelay = 5000; // Her 5 saniyede bir veri gönder

void setup() {
  Serial.begin(115200);

  WiFi.begin(ssid, password);
  Serial.println("Wi-Fi'a bağlanılıyor...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi bağlandı!");
}

void loop() {
  if ((millis() - lastTime) > timerDelay) {
    if (WiFi.status() == WL_CONNECTED) {
      HTTPClient http;

      http.begin(serverName);
      http.addHeader("Content-Type", "application/json");

      // Gönderilecek örnek veri
      String httpRequestData = "{\"sensor_id\": \"esp32_dev_kit\", \"temperature\": 24.5}";

      int httpResponseCode = http.POST(httpRequestData);

      Serial.print("HTTP Yanıt kodu: ");
      Serial.println(httpResponseCode);

      http.end();
    } else {
      Serial.println("Wi-Fi bağlantısı kopuk!");
    }
    
    lastTime = millis();
  }
}