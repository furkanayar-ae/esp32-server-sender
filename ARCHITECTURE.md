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

    graph LR
    subgraph Sistem Sınırı [MES / IoT Üretim Takip Sistemi]
        UC1[ESP32 Telemetri Verisi Yayınla]
        UC2[MQTT Mesajlarını Dinle / Subscribe]
        UC3[Clean Architecture ile Veriyi Doğrula]
        UC4[Üretim Verisini Domain Model'e Dönüştür]
        UC5[MES Log Paneline Anlık Veri Bas]
        UC6[GitHub'da Kod ve Mimariyi Yönet]
    end

    Operator((Operatör / İstasyon)) --> UC1
    ESP32Device((ESP32 Donanım)) --> UC1
    
    UC1 -->|MQTT Publish| Broker[MQTT Broker]
    Broker -->|MQTT Subscribe| Backend[Python Backend]
    
    Backend --> UC2
    Backend --> UC3
    UC3 --> UC4
    UC4 --> UC5
    
    Developer((Geliştirici / Stajyer)) --> UC6

    graph TD
    Start([Başlangıç: İstasyon Tetiklendi]) --> ReadSensor[ESP32 Sensörleri Okur<br/>Sıcaklık, Durum vb.]
    ReadSensor --> CreateJSON[Veriler JSON Formatına Dönüştürülür<br/>station_id, product_id, operator_id, temperature]
    
    CreateJSON --> MQTTPublish[ESP32, MQTT Broker'a Veriyi Yayımlar<br/>Topic: fabrika/uretim/istasyon_1]
    
    MQTTPublish --> BrokerQueue{MQTT Broker<br/>test.mosquitto.org}
    
    BrokerQueue -->|Asenkron Mesaj İletimi| PythonSubscribe[Python Backend Arayüzü<br/>MQTT Broker'ı Dinler / Subscribe]
    
    PythonSubscribe --> CleanArch{Clean Architecture Katmanları}
    
    CleanArch -->|1. Interface Adapters| ParseData[Ham Bayt Verisi JSON String'e Çevrilir]
    ParseData -->|2. Use Cases| ValidateData[İş Kuralları ve Veri Doğrulama Çalıştırılır]
    ValidateData -->|3. Domain Layer| DomainModel[Saf Veri Modeli 'ProductionData' Oluşturulur]
    
    DomainModel --> OutputLog[MES Anlık Takip Paneline ve Konsola Log Basılır]
    
    OutputLog --> End([İşlem Başarıyla Tamamlandı])

    server/
├── domain/                  # 1. Domain Katmanı (Saf Veri Modelleri)
│   └── production_model.py  # Üretim veri yapısı (ProductionData)
├── use_cases/               # 2. Use Cases Katmanı (İş Kuralları)
│   └── handle_production.py # Veri doğrulama ve MES loglama mantığı
├── interface_adapters/      # 3. Interface Adapters Katmanı
│   └── mqtt_controller.py   # MQTT mesajlarını yakalayan ve use case'e ileten kontrolcü
└── main.py                  # 4. Infrastructure & Entrypoint (MQTT Client Bağlantısı)