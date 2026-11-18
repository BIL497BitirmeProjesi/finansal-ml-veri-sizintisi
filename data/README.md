# Veri setleri

Ham veri dosyaları repoya yüklenmez (`.gitignore`). Her üye aşağıdaki adımlarla kendi bilgisayarına indirir.

## 1. BIST 100 (XU100.IS)

- **Kaynak:** Yahoo Finance, `yfinance` kütüphanesi
- **İndirme:** `python src/veri_indir.py bist` → `yf.download("XU100.IS", start="2016-10-01", end="2026-10-02", auto_adjust=False)`; `end` hariç olduğu için 01.10.2026 dahildir. Deneylerde `Close` sütunu kullanılır.
- **Dosya:** `data/raw/xu100.csv`: 2.500 işlem günü, 03.10.2016 – 01.10.2026; sütunlar Open, High, Low, Close, Adj Close (float64), Volume (int64)
- **İndirme tarihi:** 18.11.2026 (yfinance 1.8.0). Aynı gün iki ayrı indirme bayt bayt aynı çıktı.
- **SHA-256:** `0f4af2d646866a3c57e572cd022605b6a87beb3920d7883b1009ecb85c724679`
- **Boş günler:** Yahoo'nun ham yanıtında (chart API) 2.536 gün var ve bunların 36'sı tamamen boş. 28'i Türkiye'deki resmî tatillere denk geliyor. Kalan 8'i Türkiye'de tatil değil: 25 Aralık 2017, 2018, 2019, 2020, 2023, 2024 ve 2025 ile 02.04.2021. Bu günler için Yahoo veri sağlamıyor. `yfinance` boş satırları attığı için dosyada 2.500 gün kalıyor. Ham yanıt, boş günler çıkarıldığında bu dosyayla aynı tarihleri ve kapanış değerlerini veriyor (18.11.2026'da karşılaştırıldı). 17.11.2026'daki ilk analizde chart API'sinden doğrudan alınan dosya (2.536 satır, SHA-256 `4c3b9224…6891`) kullanılmıştı; özet değerleri bu dosyanınkiyle aynı.
- **Hacmi 0 olan günler:** 19.04.2019 ve 08.02.2023. Hacim öznitelik olarak kullanılmadığından deneyleri etkilemez.
- **27.07.2020 (iki sıfır atma):** Seride kırılma yok (24.07.2020: 1.192,02 → 27.07.2020: 1.195,70 → 28.07.2020: 1.152,70); Yahoo seriyi düzeltilmiş veriyor. `src/eda.py` bu tarihleri her çalıştırmada yazdırır.
- **Not:** Yahoo geçmiş verileri sonradan güncelleyebilir. Yeniden indirilen dosyanın SHA-256 özeti farklıysa `src/eda.py` çıktısını `results/eda/bist_ozet.csv` ile karşılaştırın.

## 2. Kredi Kartı Dolandırıcılığı (ULB)

- **Kaynak:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud (Dal Pozzolo ve ark., 2015)
- **İçerik:** 284.807 işlem, 31 sütun: Time, V1–V28 (PCA), Amount (float64), Class (int64). 492 dolandırıcılık (%0,173).
- **Dosya:** `data/raw/creditcard.csv` (150.828.752 bayt, ~144 MB). GitHub'ın 100 MB dosya sınırını aştığı için repoya yüklenemez.
- **İndirme tarihi:** 17.11.2026. 18.11.2026'da yeniden indirildi; SHA-256 özeti aynı çıktı.
- **Nasıl indirildi:** Kaggle girişi gerektirdiği için Google'ın TensorFlow yansısından indirildi: `storage.googleapis.com/download.tensorflow.org/data/creditcard.csv`. 17.11.2026'da Kaggle'dan doğrudan indirilen orijinal dosyayla SHA-256 özeti karşılaştırıldı ve birebir eşleşti.
- **SHA-256:** `76274b691b16a6c49d3f159c883398e03ccd6d1ee12d9d8ee38f4b4b98551a89`
- **Doğrulama:** `python src/veri_indir.py fraud` satır sayısını ve SHA-256 özetini yazdırır.

SHA-256 özetini hesaplamak için (Windows PowerShell):

```powershell
Get-FileHash data\raw\creditcard.csv -Algorithm SHA256
```
