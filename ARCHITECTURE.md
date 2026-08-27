# 🏭 MES IoT End-to-End Architecture

Bu döküman, ESP32 uç cihazları ile Python tabanlı arka plan sunucusu arasındaki haberleşmeyi sağlayan Clean Architecture mimarisini içerir.

## System Design & Data Flow Diyagramı

```mermaid
graph TD
    subgraph EdgeLayer [1. Donanım Katmanı]
        ESP32[ESP32 Mikrodenetleyici] -->|Sensör Okuma & JSON| Payload[JSON Payload:<br/>station_id, temperature, status]
    end

    subgraph BrokerLayer [2. Haberleşme Katmanı]
        Payload -->|MQTT Publish| Broker[MQTT Broker<br/>test.mosquitto.org]
    end

    subgraph BackendLayer [3. Clean Architecture Backend]
        Broker -->|MQTT Subscribe| Adapter[MQTT Controller]
        Adapter -->|Ham Veri| UseCase[ProcessProductionData]
        UseCase -->|Doğrulama| Domain[ProductionData Saf Model]
    end
    ## 2. Detaylı Sequence Diagram

```mermaid
sequenceDiagram
    autonumber
    participant ESP32 as ESP32 Cihazı
    participant Broker as MQTT Broker
    participant Backend as Python Backend
    participant Domain as Domain Katmanı

    ESP32->>Broker: MQTT Publish (JSON Verisi)
    Broker->>Backend: MQTT Subscribe (Ham Veri)
    Backend->>Domain: ProductionData Modeli Oluşturulur
    Domain-->>Backend: Doğrulama Başarılı
    ## 3. Use Case Diagram

```mermaid
graph LR
    subgraph Sistem Sınırı
        UC1[ESP32 Veri Yayınla]
        UC2[MQTT Dinle]
        UC3[Clean Architecture Doğrulama]
    end

    Operator((Operatör)) --> UC1
    UC1 -->|MQTT| Broker[MQTT Broker]
    Broker -->|Subscribe| Backend[Python Backend]
    Backend --> UC2
    Backend --> UC3
    ## 4. Flowchart (İş Akış Şeması)

```mermaid
graph TD
    Start([Başlangıç: Sensör Okuma]) --> CreateJSON[JSON Verisi Hazırlanır]
    CreateJSON --> MQTTPublish[MQTT Broker'a Yayımlanır]
    MQTTPublish --> PythonSub[Python Backend Dinler]
    PythonSub --> Validate[Clean Architecture ile Doğrulanır]
    Validate --> End([MES Log Paneline Basılır])
    ## 5. Katmanlı Mimari Dosya Yapısı

```text
server/
├── domain/                  # 1. Domain Katmanı (Saf Veri Modelleri)
│   └── production_model.py  # Üretim veri yapısı (ProductionData)
├── use_cases/               # 2. Use Cases Katmanı (İş Kuralları)
│   └── handle_production.py # Veri doğrulama ve MES loglama mantığı
├── interface_adapters/      # 3. Interface Adapters Katmanı
│   └── mqtt_controller.py   # MQTT mesajlarını yakalayan ve use case'e ileten kontrolcü
└── main.py                  # 4. Infrastructure & Entrypoint (MQTT Client Bağlantısı)