from server.domain.production_model import ProductionData

class ProcessProductionDataUseCase:
    def execute(self, raw_data: dict) -> ProductionData:
        # MES İş Kuralı: Veriyi doğrula, model oluştur ve durumu logla
        production = ProductionData(
            station_id=raw_data.get("station_id", "UNKNOWN_STATION"),
            product_id=raw_data.get("product_id", "UNKNOWN_PRODUCT"),
            operator_id=raw_data.get("operator_id", "NO_OPERATOR"),
            temperature=float(raw_data.get("temperature", 0.0)),
            status=raw_data.get("status", "IN_PROGRESS")
        )
        
        print("\n" + "="*40)
        print("🏭 [MES - Üretim Takip Sistemi]")
        print(f"📍 İstasyon : {production.station_id}")
        print(f"📦 Ürün ID  : {production.product_id}")
        print(f"👷 Operatör : {production.operator_id}")
        print(f"🌡️ Sıcaklık : {production.temperature}°C")
        print(f"⚡ Durum    : {production.status}")
        print("="*40 + "\n")
        
        return production