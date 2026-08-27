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


    ---

## 2. Detaylı Sequence Diagram (Zaman ve Mesaj Akışı)

ESP32 uç cihazından Python backend sunucusuna kadar olan asenkron veri akışının sıralama diyagramı:

```mermaid
sequenceDiagram
    autonumber
    actor Operator as Operatör / İstasyon
    participant ESP32 as ESP32 (Edge Device)
    participant Broker as MQTT Broker (Mosquitto)
    participant Backend as Python Backend (Main / MQTT Controller)
    participant UseCase as Use Case (ProcessProductionData)
    participant Domain as Domain Layer (ProductionData)

    Note over Operator, ESP32: Üretim verisi sensörlerden okunur
    Operator->>ESP32: İstasyon tetiklenir (Start / Process)
    
    Note over ESP32: JSON Payload hazırlanır (MES Standardı)<br/>station_id, product_id, operator_id, temperature, status
    
    ESP32->>Broker: PUBLISH (Topic: fabrika/uretim/istasyon_1)
    
    Note over Broker: Mesaj kuyruğa alınır ve ilgili abonelere dağıtılır
    
    Broker->>Backend: SUBSCRIBE (Gelen Ham Bayt Verisi)
    
    Note over Backend: Interface Adapters (MQTT Controller)<br/>Bayt verisi JSON string formatına çevrilir
    
    Backend->>UseCase: execute(raw_data) çağrılır
    
    Note over UseCase: İş kuralları kontrol edilir, alanlar doğrulanır
    
    UseCase->>Domain: ProductionData(saf model) nesnesi oluşturulur
    
    Note over Domain: Veri modeli mühürlenir ve konsola MES logu basılır
    
    Domain-->>Backend: Başarılı İşlem Tamamlandı