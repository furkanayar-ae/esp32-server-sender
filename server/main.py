import time
import paho.mqtt.client as mqtt
from server.interface_adapters.mqtt_controller import MQTTController

# Public / Yerel test MQTT Broker adresi
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883
MQTT_TOPIC = "fabrika/uretim/istasyon_1"

controller = MQTTController()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ MQTT Broker'a bağlandı ({MQTT_BROKER})")
        client.subscribe(MQTT_TOPIC)
        print(f"📡 Dinleniyor: {MQTT_TOPIC}")
    else:
        print(f"❌ Bağlantı başarısız! Hata kodu: {rc}")

def on_message(client, userdata, msg):
    controller.handle_message(msg.topic, msg.payload)

if __name__ == "__main__":
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print("🚀 MES & MQTT Sunucusu Başlatılıyor...")
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Sürekli dinlemede kal
    client.loop_forever()