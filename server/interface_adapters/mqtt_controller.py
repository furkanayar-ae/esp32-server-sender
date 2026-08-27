import json
from server.use_cases.handle_production import ProcessProductionDataUseCase

class MQTTController:
    def __init__(self):
        self.use_case = ProcessProductionDataUseCase()

    def handle_message(self, topic: str, payload_bytes: bytes):
        try:
            payload_str = payload_bytes.decode('utf-8')
            raw_data = json.loads(payload_str)
            print(f"[MQTT Adaptör] Konu: {topic} | Yeni veri yakalandı.")
            
            # Use Case katmanını tetikle
            return self.use_case.execute(raw_data)
        except Exception as e:
            print(f"[MQTT Hata] Veri işlenemedi: {e}")
            return None