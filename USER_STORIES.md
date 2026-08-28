# MES IoT Projesi - Kullanıcı Hikayeleri (User Stories)

Bu doküman, fabrikadaki 6 üretim istasyonu, vardiya çalışma/mola saatleri, ek görevler, üretilen parça detayları ve hedef ürün takibine göre hazırlanmıştır.

## 1. Üretim Operatörü
* **Hikaye:** Bir **Üretim Operatörü** olarak, çalıştığım istasyonda vardiya çalışma saatleri ve mola süreleri içerisinde üretim yaparken, işlediğim **üretilen parça** ve **hedef ürün** bilgilerini `ESP32` cihazım üzerinden sisteme otomatik olarak göndermek istiyorum; böylece parça ve hedef takibim hatasız yapılsın.
* **Kabul Kriterleri:**
    * ESP32 cihazı, `station_id` (1-6 arası), `operator_id`, `product_id` (hedef ürün/parça bilgisi), `temperature` ve `status` alanlarını eksiksiz göndermelidir.
    * Mola veya çalışma saatleri dışındaki operasyonel durumlar ya da şef tarafından verilen **ek görevler** sisteme işlenebilmelidir.

## 2. İstasyon Şefi
* **Hikaye:** Bir **İstasyon Şefi** olarak, sorumlu olduğum istasyondaki **üretilen parça** adetlerini, vardiya mola/çalışma düzenini ve personele atanan **ek görevleri** SQLite veritabanı üzerinden inceleyebilmek istiyorum; böylece hattımdaki ürün hedeflerinin tutup tutmadığını denetleyebilirim.
* **Kabul Kriterleri:**
    * Şefler, kendi istasyonlarındaki `ProductionLog` kayıtları üzerinden hangi **hedef ürünün** üretildiğini ve parça durumlarını takip edebilmelidir.
    * İstasyondaki hata durumları (`ERROR`) veya ek görevler log paneline yansıtılmalıdır.

## 3. Fabrika / Üretim Müdürü
* **Hikaye:** Bir **Üretim Müdürü** olarak, 6 istasyonun tamamında üretilen parçaların **hedef ürün** planlarına uygunluğunu, çalışma/mola saatlerini ve genel üretim akışını Clean Architecture altyapısı üzerinden yönetebilmek istiyorum; böylece fabrika genelindeki hedefleri ve operasyonel verimliliği kuşbakışı takip edebileyim.
* **Kabul Kriterleri:**
    * Tüm istasyonlardan gelen MQTT mesajları `MQTTController` ile karşılanmalıdır.
    * `ProcessProductionDataUseCase` katmanı, üretilen parça ve hedef ürün verilerini iş kurallarına göre doğrulayıp `SQLite` veritabanına kaydetmelidir.
