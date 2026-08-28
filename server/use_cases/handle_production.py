from server.domain.production_model import ProductionData

class ProcessProductionDataUseCase:
    def __init__(self, database):
        self.database = database  # Veritabanı buraya enjekte ediliyor

    def execute(self, raw_data: dict) -> ProductionData:
        # MES İş Kuralı: Veriyi doğrula, model oluştur
        production = ProductionData(
            station_id=raw_data.get("station_id", "UNKNOWN_STATION"),
            product_id=raw_data.get("product_id", "UNKNOWN_PRODUCT"),
            operator_id=raw_data.get("operator_id", "NO_OPERATOR"),
            temperature=float(raw_data.get("temperature", 0.0)),
            status=raw_data.get("status", "IN_PROGRESS")
        )
        
        # 1. Veritabanına Kaydet
        try:
            self.database.save_production(production)
            db_status = "💾 Veritabanına Kaydedildi!"
        except Exception as e:
            db_status = f"❌ DB Kayıt Hatası: {e}"

        # 2. Konsol Logları
        print("\n" + "="*40)
        print("🏭 [MES - Üretim Takip Sistemi]")
        print(f"📍 İstasyon : {production.station_id}")
        print(f"📦 Ürün ID  : {production.product_id}")
        print(f"👷 Operatör : {production.operator_id}")
        print(f"🌡️ Sıcaklık : {production.temperature}°C")
        print(f"⚡ Durum    : {production.status}")
        print(f"Status      : {db_status}")
        print("="*40 + "\n")
        
        return production