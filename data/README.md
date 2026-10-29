# Veri setleri

Ham veri dosyaları repoya yüklenmez (`.gitignore`). Her üye aşağıdaki adımlarla kendi bilgisayarına indirir.

## 1. BIST 100 (XU100.IS)

- **Kaynak:** Yahoo Finance, `yfinance` kütüphanesi
- **Aralık:** `start="2016-10-01"`, `end="2026-10-01"` (end hariç), `auto_adjust=False`, `Close` sütunu
- **Dikkat:** 27.07.2020'de Borsa İstanbul endeksten iki sıfır attı. Bu tarihten önceki değerler 100'e bölünmemişse düzeltilmelidir.
- **Dosya:** `data/raw/xu100.csv`
- **İndirme tarihi:** …
- **yfinance sürümü:** …
- **SHA-256:** …

## 2. Kredi Kartı Dolandırıcılığı (ULB)

- **Kaynak:** https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **İçerik:** 284.807 işlem, 492 dolandırıcılık (%0,172); Time, V1–V28 (PCA), Amount, Class
- **Dosya:** `data/raw/creditcard.csv` (~144 MB; GitHub'ın 100 MB dosya sınırını aştığı için repoya yüklenemez)
- **İndirme tarihi:** …
- **SHA-256:** …

SHA-256 özetini hesaplamak için (Windows PowerShell):

```powershell
Get-FileHash data\raw\creditcard.csv -Algorithm SHA256
```
