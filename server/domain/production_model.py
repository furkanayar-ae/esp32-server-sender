class ProductionData:
    def __init__(self, station_id: str, product_id: str, operator_id: str, temperature: float, status: str):
        self.station_id = station_id
        self.product_id = product_id
        self.operator_id = operator_id
        self.temperature = temperature
        self.status = status

    def to_dict(self):
        return {
            "station_id": self.station_id,
            "product_id": self.product_id,
            "operator_id": self.operator_id,
            "temperature": self.temperature,
            "status": self.status
        }
    