from server.domain.sensor_model import SensorData

class ProcessSensorDataUseCase:
    def execute(self, raw_data: dict) -> SensorData:
        # Gelen ham veriyi iş kuralından geçirip domain modeline dönüştürüyoruz
        sensor = SensorData(
            device_id=raw_data.get("device_id", "UNKNOWN"),
            temperature=float(raw_data.get("temperature", 0.0)),
            status=raw_data.get("status", "ACTIVE")
        )
        print(f"[CleanArch UseCase] İşlenen Veri: {sensor.to_dict()}")
        return sensor