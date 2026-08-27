import time
import paho.mqtt.client as mqtt
from server.interface_adapters.mqtt_controller import MQTTController
from server.infrastructure.database import LocalDatabase

# Public test MQTT Broker ayarları
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "fabrika/uretim/istasyon_1"

# 1. Local veritabanını başlatıyoruz
db = LocalDatabase()

# 2. Controller'ı parametresiz başlatıyoruz (veritabanı Use Case içinde yönetiliyor)
controller = MQTTController(database=db)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ MQTT Broker'a bağlandı ({MQTT_BROKER})")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Dinleniyor: {MQTT_TOPIC}")
    else:
        print(f"❌ Bağlantı başarısız! Hata kodu: {rc}")

def on_message(client, userdata, msg):
    print(f"\n📥 MESAJ YAKALANDI -> Topic: {msg.topic}")
    try:
        payload_str = msg.payload.decode('utf-8')
        print(f"📦 Gelen Payload: {payload_str}")
        
        # Gelen MQTT mesajı Controller'a iletiliyor
        controller.handle_message(msg.topic, msg.payload)
        print("✅ Mesaj başarıyla işlendi!")
    except Exception as e:
        print(f"❌ HATA OLUŞTU: {e}")

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print("🚀 MES & MQTT Sunucusu Başlatılıyor (Local DB Aktif)...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Sürekli dinlemede kal
    client.loop_forever()