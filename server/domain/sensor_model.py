class SensorData:
    def __init__(self, device_id: str, temperature: float, status: str):
        self.device_id = device_id
        self.temperature = temperature
        self.status = status

    def to_dict(self):
        return {
            "device_id": self.device_id,
            "temperature": self.temperature,
            "status": self.status
        }