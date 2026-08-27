import paho.mqtt.publish as publish

topic = "fabrika/uretim/istasyon_1"
payload = '{"station_id": "ISTASYON_1", "product_id": "URUN_999", "operator_id": "OPERATOR_1", "temperature": 25.4, "status": "RUNNING"}'

print("📡 Test verisi gönderiliyor...")
publish.single(topic, payload, hostname="test.mosquitto.org")
print("✅ Veri başarıyla gönderildi!")