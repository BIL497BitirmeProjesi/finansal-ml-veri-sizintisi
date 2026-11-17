# Veri setleri

Ham veri dosyaları repoya yüklenmez (`.gitignore`). Her üye aşağıdaki adımlarla kendi bilgisayarına indirir.

## 1. BIST 100 (XU100.IS)

- **Kaynak:** Yahoo Finance, `yfinance` kütüphanesi
- **Aralık:** `start="2016-10-01"`, `end="2026-10-01"` (end hariç), `auto_adjust=False`, `Close` sütunu
- **Dikkat:** 27.07.2020'de Borsa İstanbul endeksten iki sıfır attı. İndirilen Yahoo serisinde bu tarih civarında kırılma yok (27.07.2020: 1195,70 → 28.07.2020: 1152,70), seri zaten düzeltilmiş geliyor. Yine de EDA'da kontrol edilir.
- **Eksikler:** 2.536 satırın 36'sı tamamen boş (tatil günleri), 2 günde hacim 0. Bunlar deneylerde elenecek.
- **Dosya:** `data/raw/xu100.csv`
- **İndirme tarihi:** 17.11.2026 (2.536 satır, 03.10.2016 – 01.10.2026)
- **Nasıl indirildi:** Yahoo Finance chart API'si (`yfinance`'in kullandığı uç nokta) tarayıcıdan çağrılıp CSV'ye yazıldı; `yfinance` kütüphanesiyle tekrar indirmek için `python src/veri_indir.py bist`
- **SHA-256:** `4c3b9224b4402e528bc437ce38750aa8c22185f3a7b4233b9993082fd2056891`

## 2. Kredi Kartı Dolandırıcılığı (ULB)

- **Kaynak:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **İçerik:** 284.807 işlem, 492 dolandırıcılık (%0,172); Time, V1–V28 (PCA), Amount, Class
- **Dosya:** `data/raw/creditcard.csv` (~144 MB; GitHub'ın 100 MB dosya sınırını aştığı için repoya yüklenemez)
- **İndirme tarihi:** 17.11.2026
- **Nasıl indirildi:** Kaggle girişi gerektirdiği için Google'ın TensorFlow yansısından (`storage.googleapis.com/download.tensorflow.org/data/creditcard.csv`) indirildi. Boyut (150.828.752 bayt), satır ve sütun sayısı (284.807 × 31) Kaggle sürümüyle uyuşuyor. Kaggle'dan indirilen dosyanın özeti bununla karşılaştırılmalı.
- **SHA-256:** `76274b691b16a6c49d3f159c883398e03ccd6d1ee12d9d8ee38f4b4b98551a89`

SHA-256 özetini hesaplamak için (Windows PowerShell):

```powershell
Get-FileHash data\raw\creditcard.csv -Algorithm SHA256
```
