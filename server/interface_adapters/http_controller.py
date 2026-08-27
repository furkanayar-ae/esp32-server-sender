import json
from server.use_cases.process_data import ProcessSensorDataUseCase

class SensorController:
    def __init__(self):
        self.use_case = ProcessSensorDataUseCase()

    def handle_post_request(self, request_body_bytes):
        try:
            body_str = request_body_bytes.decode('utf-8')
            raw_data = json.loads(body_str)
            
            # İş katmanını çağırıyoruz
            processed_data = self.use_case.execute(raw_data)
            return {"status": "success", "data": processed_data.to_dict()}
        except Exception as e:
            return {"status": "error", "message": str(e)}