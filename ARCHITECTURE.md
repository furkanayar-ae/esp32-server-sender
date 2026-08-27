# 🏭 MES IoT End-to-End Architecture

Bu döküman, **ESP32** uç cihazları ile **Python** tabanlı arka plan sunucusu arasındaki haberleşmeyi sağlayan, **Clean Architecture** prensiplerine ve **MES (Manufacturing Execution System)** standartlarına uygun olarak tasarlanmış endüstriyel IoT projesinin mimari detaylarını içerir.

---

## 1. System Design & Data Flow Diyagramı

```mermaid
graph TD
    subgraph EdgeLayer [1. Edge / Donanım Katmanı]
        ESP32[ESP32 Mikrodenetleyici] -->|Sensör Okuma & JSON| Payload[JSON Payload:<br/>station_id, product_id, operator_id, temperature, status]
    end

    subgraph BrokerLayer [2. Haberleşme / Broker Katmanı]
        Payload -->|MQTT Publish<br/>Topic: fabrika/uretim/istasyon_1| Broker[MQTT Broker<br/>test.mosquitto.org:1883]
    end

    subgraph BackendLayer [3. Clean Architecture Backend Python]
        Broker -->|MQTT Subscribe| Adapter[Interface Adapters:<br/>MQTT Controller]
        Adapter -->|Ham Veri İletimi| UseCase[Use Cases:<br/>ProcessProductionDataUseCase]
        UseCase -->|İş Kuralları & Doğrulama| Domain[Domain Layer:<br/>ProductionData Saf Model]
    end

    subgraph OutputLayer [4. İzleme / MES Katmanı]
        Domain -->|Formatlı Veri Çıktısı| Console[MES Anlık Takip Paneli / Loglama]
    end