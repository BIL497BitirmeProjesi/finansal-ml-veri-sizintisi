"""Veri keşif analizi (gelişme raporu Bölüm 4). Çıktılar results/eda/ altına yazılır.

Kullanım: python src/eda.py [bist|fraud|hepsi]   (önce: python src/veri_indir.py bist / fraud)
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

KOK = Path(__file__).resolve().parents[1]
CIKTI = KOK / "results" / "eda"
CIKTI.mkdir(parents=True, exist_ok=True)
TEST_ORANI = 0.2  # kronolojik %80/%20 bölme


def _tarih(t) -> str:
    return pd.Timestamp(t).strftime("%d.%m.%Y")


def _turler(df: pd.DataFrame) -> str:
    return "; ".join(f"{t}: {', '.join(s)}" for t, s in df.columns.groupby(df.dtypes.astype(str)).items())


def bist_eda(yol=KOK / "data" / "raw" / "xu100.csv") -> pd.DataFrame:
    df = pd.read_csv(yol, index_col=0, parse_dates=True).sort_index()
    hacim0 = df.index[df["Volume"] == 0] if "Volume" in df else []
    ozet = {
        "satır": len(df),
        "sütun": df.shape[1],
        "veri türleri": _turler(df),
        "başlangıç": _tarih(df.index.min()),
        "bitiş": _tarih(df.index.max()),
        "eksik değer (toplam)": int(df.isna().sum().sum()),
        "tamamen boş satır": int(df.isna().all(axis=1).sum()),
        "tekrar eden tarih": int(df.index.duplicated().sum()),
        "tarih sıralı mı": bool(df.index.is_monotonic_increasing),
        "Volume==0 gün": f"{len(hacim0)} ({', '.join(_tarih(t) for t in hacim0)})",
    }
    kapanis = df["Close"].dropna()  # tatil/boş günler yön ve getiri hesabına girmesin
    r = kapanis.pct_change().dropna()
    yon = (kapanis.shift(-1) > kapanis).iloc[:-1]  # hedef: ertesi kapanış bugünden yüksek mi
    ozet["geçerli işlem günü"] = len(kapanis)
    ozet["yükseliş günü oranı"] = f"{yon.mean():.4f} ({int(yon.sum())}/{len(yon)})"
    ozet["getiri sayısı / ort. / std"] = f"{len(r)} / {r.mean():.5f} / {r.std():.5f}"
    ozet["en büyük 5 mutlak getiri"] = ", ".join(f"{_tarih(t)}: {v:.4f}" for t, v in r.abs().nlargest(5).items())
    for gun in ("2020-07-24", "2020-07-27", "2020-07-28"):
        if pd.Timestamp(gun) in kapanis.index:
            ozet[f"kapanış {_tarih(gun)}"] = round(float(kapanis[gun]), 2)
    kesim = int(len(yon) * (1 - TEST_ORANI))
    test = yon.iloc[kesim:]
    ozet["kronolojik test (gün)"] = f"{len(test)} ({_tarih(test.index[0])} – {_tarih(test.index[-1])})"
    ozet["testte yükseliş oranı"] = round(float(test.mean()), 4)
    tablo = pd.Series(ozet, name="değer").astype(str).to_frame()
    tablo.to_csv(CIKTI / "bist_ozet.csv")

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(df.index, df["Close"], lw=0.8)
    kirilma = pd.Timestamp("2020-07-27")
    if df.index.min() <= kirilma <= df.index.max():
        ax.axvline(kirilma, color="red", ls="--", label="27.07.2020 (iki sıfır atma)")
        ax.legend()
    ax.set_title("XU100 kapanış serisi")
    ax.set_ylabel("Kapanış")
    fig.tight_layout()
    fig.savefig(CIKTI / "bist_kapanis.png", dpi=150)
    plt.close(fig)

    sayilar = yon.value_counts().reindex([False, True], fill_value=0)
    fig, ax = plt.subplots(figsize=(4, 4))
    cubuk = ax.bar(["Düşüş/aynı", "Yükseliş"], sayilar.values, color=["#c0504d", "#4f81bd"])
    ax.bar_label(cubuk, labels=[f"{n} (%{100 * n / len(yon):.1f})" for n in sayilar.values])
    ax.set_title(f"Ertesi gün yönü ({len(yon)} gün)")
    fig.tight_layout()
    fig.savefig(CIKTI / "bist_yon.png", dpi=150)
    plt.close(fig)
    return tablo


def fraud_eda(yol=KOK / "data" / "raw" / "creditcard.csv") -> pd.DataFrame:
    df = pd.read_csv(yol).sort_values("Time", kind="stable").reset_index(drop=True)
    kesim = int(len(df) * (1 - TEST_ORANI))
    test = df.iloc[kesim:]
    tekrar = df.duplicated()
    ozet = {
        "satır": len(df),
        "sütun": df.shape[1],
        "veri türleri": f"float64: {(df.dtypes == 'float64').sum()} sütun; Class: {df['Class'].dtype}",
        "eksik değer (toplam)": int(df.isna().sum().sum()),
        "tekrar eden satır": int(tekrar.sum()),
        "tekrar edenlerde dolandırıcılık": int(df.loc[tekrar, "Class"].sum()),
        "Amount==0 işlem (dolandırıcılık)": f"{int((df['Amount'] == 0).sum())} ({int(df.loc[df['Amount'] == 0, 'Class'].sum())})",
        "dolandırıcılık sayısı": int(df["Class"].sum()),
        "dolandırıcılık oranı": round(float(df["Class"].mean()), 5),
        "hepsine 0 diyen modelin doğruluğu": round(1 - float(df["Class"].mean()), 5),
        "Time aralığı (saat)": round(float(df["Time"].max() - df["Time"].min()) / 3600, 2),
        "son %20 testte işlem": len(test),
        "son %20 testte dolandırıcılık": int(test["Class"].sum()),
        "kesim (saat)": round(float(df["Time"].iloc[kesim]) / 3600, 2),
        "Amount ort./medyan/maks": (
            round(float(df["Amount"].mean()), 2),
            round(float(df["Amount"].median()), 2),
            round(float(df["Amount"].max()), 2),
        ),
    }
    tablo = pd.Series(ozet, name="değer").astype(str).to_frame()
    tablo.to_csv(CIKTI / "fraud_ozet.csv")

    fig, ax = plt.subplots(figsize=(4, 4))
    df["Class"].value_counts().sort_index().plot.bar(ax=ax, logy=True)
    ax.set_title("Sınıf dağılımı (log ölçek)")
    ax.set_xlabel("Class (0=normal, 1=dolandırıcılık)")
    fig.tight_layout()
    fig.savefig(CIKTI / "fraud_sinif.png", dpi=150)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(9, 3.5))
    saat = df.loc[df["Class"] == 1, "Time"] / 3600
    ax.hist(saat, bins=48)
    ax.axvline(df["Time"].iloc[kesim] / 3600, color="red", ls="--", label="%80/%20 kesim")
    ax.set_xlabel("Saat")
    ax.set_ylabel("Dolandırıcılık işlemi")
    ax.set_title("Dolandırıcılığın zamana dağılımı")
    ax.legend()
    fig.tight_layout()
    fig.savefig(CIKTI / "fraud_zaman.png", dpi=150)
    plt.close(fig)
    return tablo


if __name__ == "__main__":
    import sys
    pd.set_option("display.max_colwidth", None)
    hedef = sys.argv[1] if len(sys.argv) > 1 else "hepsi"
    if hedef in ("bist", "hepsi"):
        print(bist_eda())
    if hedef in ("fraud", "hepsi"):
        print(fraud_eda())
