#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

// Wi-Fi Bilgileri
const char* ssid = "iPhone 15 pro";
const char* password = "furk4nn12";

// MQTT Broker Bilgileri (Sunucumuzun dinlediği broker)
const char* mqtt_server = "test.mosquitto.org";
const int mqtt_port = 1883;
const char* mqtt_topic = "fabrika/uretim/istasyon_1";

WiFiClient espClient;
PubSubClient client(espClient);

void setup_wifi() {
  delay(10);
  Serial.println("Wi-Fi'a bağlanılıyor...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWi-Fi bağlandı! IP adresi: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("MQTT Broker'a bağlanılıyor...");
    // Benzersiz bir client ID oluşturuyoruz
    if (client.connect("ESP32_MES_Station_01")) {
      Serial.println(" BAĞLANDI!");
    } else {
      Serial.print(" başarısız, rc=");
      Serial.print(client.state());
      Serial.println(" 5 saniye sonra tekrar denenecek...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, mqtt_port);
}

unsigned long lastMsg = 0;

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  unsigned long now = millis();
  // Her 5 saniyede bir MES verisi fırlat
  if (now - lastMsg > 5000) {
    lastMsg = now;

    // JSON Veri Paketi Oluşturma (MES Standardı)
    StaticJsonDocument<200> doc;
    doc["station_id"] = "STATION_01";
    doc["product_id"] = "PRD-2026-99";
    doc["operator_id"] = "OP_FURKAN_07";
    doc["temperature"] = 38.4;
    doc["status"] = "processing";

    char jsonBuffer[256];
    serializeJson(doc, jsonBuffer);

    // MQTT Topic'ine gönder (Publish)
    client.publish(mqtt_topic, jsonBuffer);
    Serial.println("MES Verisi MQTT üzerinden gönderildi: " + String(jsonBuffer));
  }
}