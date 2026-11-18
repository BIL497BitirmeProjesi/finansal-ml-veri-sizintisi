# Finansal Makine Öğrenmesinde Veri Sızıntısının Ölçülmesi

**Measuring Data Leakage in Financial Machine Learning: A Comparison of Flawed and Correct Experimental Setups**

İstanbul Medeniyet Üniversitesi, Bilgisayar Mühendisliği. BIL497/BIL498 Bitirme Projesi (2026–2027)

| Öğrenci No | Ad Soyad |
|---|---|
| 21120205711 | Yağızhan Can |
| 24120205080 | Furkan Topçu |

**Danışman:** Dr. Öğr. Üyesi Tamer Uçar

## Proje hakkında

Finansal ML çalışmalarında sık yapılan dört tasarım hatasının model başarısını ne kadar yapay olarak şişirdiğini kontrollü deneylerle ölçüyoruz:

| Kod | Hata | Doğrusu |
|---|---|---|
| (a) | Zaman serisini karıştırıp rastgele bölmek | Kronolojik %80/%20 bölme + 1 gün purge |
| (b) | Özniteliklerde gelecek bilgisi (`rolling(center=True)`) | Yalnızca geçmişe bakan `rolling(n)` |
| (c) | SMOTE'u bölmeden önce tüm veriye uygulamak | SMOTE yalnızca eğitimde, `imblearn` Pipeline içinde |
| (d) | Ölçekleyiciyi bölmeden önce tüm veriye uydurmak | StandardScaler yalnızca eğitimde |

**Veri setleri:** BIST 100 (XU100.IS, yfinance, 03.10.2016 → 01.10.2026, 2.500 işlem günü) ve ULB Kredi Kartı Dolandırıcılığı (Kaggle).
**Modeller:** Lojistik Regresyon, Random Forest, XGBoost. Her deney 5 tohumla (0–4) tekrarlanır.

## Klasör yapısı

```
data/
  raw/          ham veri (git'e girmez, bkz. data/README.md)
  processed/    işlenmiş veri (git'e girmez)
notebooks/      keşifsel analiz defterleri (01_veri_inceleme.ipynb ...)
src/            deney kodu (veri, öznitelik, kurulumlar, kontrol betikleri)
results/        eda/ (veri keşfi tabloları ve grafikleri), results.csv (deney sonuçları)
docs/           öneri formu, raporlar, literatür notları
```

## Kurulum

```bash
git clone https://github.com/BIL497BitirmeProjesi/finansal-ml-veri-sizintisi.git
cd finansal-ml-veri-sizintisi
python -m venv .venv
.venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

Google Colab'da ilk hücre: `!pip install -q -r requirements.txt`

## Çalıştırma

```bash
python src/veri_indir.py bist     # data/raw/xu100.csv dosyasını indirir, SHA-256 yazdırır
python src/veri_indir.py fraud    # data/raw/creditcard.csv dosyasını doğrular (indirme: data/README.md)
python src/eda.py                 # results/eda/ altına özet tabloları ve grafikleri yazar
```

Aynı analiz `notebooks/01_veri_inceleme.ipynb` defterinde çıktılarıyla birlikte durur.

## Çalışma düzeni

- `main` dalı her zaman çalışır durumda tutulur.
- Her iş için ayrı dal açılır (ör. `veri-inceleme`, `dogru-kurulum`), iş bitince `main` dalına birleştirilir (tercihen Pull Request ile).
- Ham veri, API anahtarları (`kaggle.json`) ve `.venv` repoya **yüklenmez**.

## Takvim

| Teslim | Tarih |
|---|---|
| Öneri formu | 27 Ekim 2026 (26 Ekim'de teslim edildi, `docs/oneri_formu/`) |
| Gelişme raporu | 20 Kasım 2026 (`docs/raporlar/BIL497_Gonderim2_Can_Topcu.pdf`) |
| Dönem sonu raporu | 18 Aralık 2026 |
