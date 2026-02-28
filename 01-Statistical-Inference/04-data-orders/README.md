## Yaklaşımımız

Olist CEO'sunun isteğine yanıt vermeden önce (_"kötü değerlendirmelerin çok para kaybettirdiği göz önünde bulundurulduğunda, iş marjını nasıl iyileştirebiliriz?"_) kötü `review_score`'a neyin sebep olduğunu araştırmalıyız.

Bu tür bir problem için iyi bir uygulama, her biri o boyuta ait bir **unique_id** içeren ve bu boyutun tüm olası özelliklerini sütun olarak listeleyen ara tablolar (Boyut Tabloları) oluşturmaktır.

Örneğin:
- `orders` tablosu (**id**, `review_score`, `amount`, satıcı ve müşteri arasındaki mesafe...)
- `sellers` tablosu (**id**, ortalama `review_score`, ortalama bekleme süresi...)
- `products` tablosu (**id**, ortalama `review_score`, kategoriler, renkler, bedenler...)
- `customers` tablosu (**id**, bu müşterinin bazı özellikleri)
- `reviews` tablosu (**id**, çevrilmiş metin, bu metnin özellikleri...)

Bu tabloları makine öğrenimi algoritmaları için eğitim setleri olarak düşünebilirsiniz.

## `Orders` ile başlayalım 🏋🏽‍♂️

Tek bir DataFrame oluşturacağız; benzersiz `order_id` indeks olacak ve bu siparişlerin tüm olası özellikleri sütunlar olarak yer alacak.

Eğitim setini sipariş düzeyinde döndürecek mantığı `olist/order.py` içinde saklayacağız. Bu, bir sonraki modelleme aşamamızda işe yarayacak.

👉 `orders.ipynb` dosyasını açın ve talimatları izleyin.
