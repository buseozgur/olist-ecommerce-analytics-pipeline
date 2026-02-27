## Objectives of the module

Bu modülde, **Olist** adlı bir e‑ticaret pazar yerinin sağladığı bir dataset’i analiz ederek CEO’nun şu sorusuna cevap arayacağız:

> Olist kârını nasıl artırabilir?

## About Olist 🇧🇷

Olist, satıcıları Brezilya’daki büyük pazar yerlerine bağlayan lider bir e‑ticaret servisidir. Ürün yönetimi, değerlendirme ve müşteri iletişimi takibi, lojistik hizmetler gibi geniş bir yelpazede hizmet sunar.

Olist, satıcılardan aylık bir ücret alır. Bu ücret, sipariş hacmi arttıkça kademeli olarak artan (progressive) bir yapıya sahiptir.

Aşağıda satıcı ve müşteri iş akışları yer alıyor:

**Seller:**

* Seller Olist’e katılır
* Seller ürün kataloğunu yükler
* Bir ürün satıldığında seller bilgilendirilir
* Seller ürünü lojistik taşıyıcıya teslim eder

👉 Tek bir müşteri siparişi için birden fazla seller sürece dahil olabilir!

**Customer:**

* Marketplace üzerinde ürünleri inceler
* Olist.store üzerinden ürün satın alır
* Teslimat için tahmini bir tarih alır
* Siparişi teslim alır
* Sipariş hakkında bir review bırakır

👉 Bir review, sipariş gönderildiği anda bırakılabilir; yani müşteri henüz siparişi almamış olsa bile review yazabilir!

## Dataset

Dataset, 2016–2018 yılları arasında Olist store üzerinden verilmiş yaklaşık 100 bin siparişten oluşur ve Le Wagon S3 bucket’ında CSV dosyaları olarak bulunmaktadır (❗️Kaggle üzerindeki dataset’ler biraz farklı olabilir).

💾 `data` klasörünü bu challenge klasörünün *dışına* koyalım ki diğer tüm challenge’lar tarafından da erişilebilsin. Zaten `git` tarafından takip edilmesini de istemiyoruz!

```bash
# Create the data folder
mkdir -p ~/.workintech/olist/data/csv
```

✅ `olist.zip` dosyasında sıkıştırılmış 9 dataset’i indirin, unzip edin ve `~/.workintech/olist/data/csv` klasörünüzün içine koyun:

```bash
curl https://wagon-public-datasets.s3.amazonaws.com/olist/olist.zip > ~/.workintech/olist/data/olist.zip
unzip -d ~/.workintech/olist/data/csv/ ~/.workintech/olist/data/olist.zip
```

Makinenizde 9 dataset’in gerçekten olduğundan emin olun:

```bash
ls ~/.workintech/olist/data/csv
```

## Setup

### 1 - Project Structure

`olist` package’ımız için bir klasör oluşturalım. Tüm data‑processing mantığımızı bu `olist` package’i içindeki `.py` dosyalarına refactor edeceğiz.

Bu `olist` klasörünü modülün ana klasöründe oluşturacağız.

Bu challenge içinde sizin için hazırlanmış bir miktar "boilerplate" code bulunuyor. Bunu hedef `olist` klasörümüze taşıyalım:

Bu sprint için proje yapınız şu şekilde olmalı(dosya isimleriniz farklı olabilir-örnektir):

```bash

sprint-15
├── 01-Statistical-Inference    # Notebook’larınız ve analizleriniz, her bir konu için
│   ├── data-context-and-setup  # her bir proje için
│   ├── data-data-preparation
│   └── data-exploratory-analysis
├── 02-Linear-Regression
│   └── ...
└── olist                       # data-processing mantığınız
    ├── README.md               # package için dokümantasyon
    ├── __init__.py             # olist klasörünü bir "package"e çevirir
    ├── data.py
    ├── order.py
    ├── product.py
    ├── review.py
    ├── seller.py
    └── utils.py
```

Kurulumunuzu kontrol etmek için şunu çalıştırın:

```bash
tree
```

Bu aşamada tree çıktınız şöyle görünmelidir(örnek):

```bash
.
├── 01-Statistical-Inference
│   └── data-context-and-setup
│       └── ... [projects here]
└── olist
    ├── README.md
    ├── __init__.py
    ├── data.py
    ├── order.py
    ├── product.py
    ├── review.py
    ├── seller.py
    └── utils.py
```

Bu modül boyunca `olist` içindeki kodda değişiklikler yapacağız. Değişiklikleri bu klasörde commit etmeyi unutmayın!

### 2 - `PYTHONPATH`’i düzenleme

`olist` path’ini `PYTHONPATH`’inize ekleyin.

Bu sayede hafta boyunca notebook’larınızda `olist` içinde tanımlı modülleri kolayca import edebileceksiniz.

Terminalinizi açın ve home dizininize gidin:

```bash
cd
```

Şimdi `.zshrc` dosyanızı açmanız gerekiyor. Fark etmiş olabileceğiniz gibi, dosya nokta ile başlıyor; bu da onun hidden bir dosya olduğu anlamına gelir. Bu dosyayı terminalde görebilmek için aşağıdaki komutu çalıştırın; `-a` flag’i hidden dosyaları da gösterecektir. Nokta ile başlayan birden çok dosya göreceksiniz. Bunların çoğu configuration dosyalarıdır.

```bash
ls -a
```

Şimdi dosyayı text editor ile açalım:

```bash
code .zshrc
```

Şimdi terminalde en dıştaki dizininize gidin, yukarda sprint-15 dediğimiz dizin ve çalıştırın

```bash
echo "export PYTHONPATH=\"$(pwd):\$PYTHONPATH\""
```

👉 Terminalde çıkan bu satırı kopyalayın ve `~/.zshrc` dosyanızın en altına yapıştırın. Dosyayı kaydetmeyi unutmayın ve bu değişikliğin geçerli olması için tüm terminal pencerelerini yeniden başlatın.

---

### 🔥 Kurulumunu kontrol et

**Challenge klasörünüze** gidip bir `ipython` oturumu başlatın:

```bash
cd ~...("01-Statistical-Inference/data-context-and-setup") }}
ipython
```

Ardından, önceki egzersizdeki setup aşamasının çalıştığını kontrol etmek için şunları yazın:

```python
from olist.data import Olist
Olist().ping()
# => pong
```

Eğer `pong` dışında bir çıktı alıyorsanız, eğitmenden yardım alın. Muhtemelen `$PYTHONPATH` ile ilgili bir sorununuz vardır.

## Kodunu GitHub’a push et

```bash
git add .
git commit -m 'kick off olist challenge'
git push origin master
```

Tebrikler! Artık `olist` için tamamen hazırsınız 🚀🚀
