"""Veri keşif analizi (gelişme raporu Bölüm 4). Çıktılar results/eda/ altına yazılır."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

KOK = Path(__file__).resolve().parents[1]
CIKTI = KOK / "results" / "eda"
CIKTI.mkdir(parents=True, exist_ok=True)


def bist_eda(yol=KOK / "data" / "raw" / "xu100.csv") -> pd.DataFrame:
    df = pd.read_csv(yol, index_col=0, parse_dates=True).sort_index()
    ozet = {
        "satır": len(df),
        "sütun": df.shape[1],
        "başlangıç": df.index.min().date(),
        "bitiş": df.index.max().date(),
        "eksik değer (toplam)": int(df.isna().sum().sum()),
        "tekrar eden tarih": int(df.index.duplicated().sum()),
        "tarih sıralı mı": bool(df.index.is_monotonic_increasing),
        "Volume==0 gün": int((df.get("Volume", pd.Series(dtype=float)) == 0).sum()),
    }
    r = df["Close"].pct_change(fill_method=None)
    yon = (df["Close"].shift(-1) > df["Close"]).iloc[:-1]
    ozet["yükseliş günü oranı"] = round(float(yon.mean()), 4)
    ozet["en büyük 5 mutlak getiri"] = r.abs().nlargest(5).round(4).to_dict()
    ozet["getiri ort./std"] = (round(float(r.mean()), 5), round(float(r.std()), 5))
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

    fig, ax = plt.subplots(figsize=(4, 4))
    yon.value_counts().sort_index().rename({False: "Düşüş/aynı", True: "Yükseliş"}).plot.bar(ax=ax)
    ax.set_title("Ertesi gün yönü")
    fig.tight_layout()
    fig.savefig(CIKTI / "bist_yon.png", dpi=150)
    plt.close(fig)
    return tablo


def fraud_eda(yol=KOK / "data" / "raw" / "creditcard.csv") -> pd.DataFrame:
    df = pd.read_csv(yol).sort_values("Time").reset_index(drop=True)
    kesim = int(len(df) * 0.8)
    test = df.iloc[kesim:]
    ozet = {
        "satır": len(df),
        "sütun": df.shape[1],
        "eksik değer (toplam)": int(df.isna().sum().sum()),
        "tekrar eden satır": int(df.duplicated().sum()),
        "dolandırıcılık sayısı": int(df["Class"].sum()),
        "dolandırıcılık oranı": round(float(df["Class"].mean()), 5),
        "Time aralığı (saat)": round(float(df["Time"].max() - df["Time"].min()) / 3600, 2),
        "son %20 testte işlem": len(test),
        "son %20 testte dolandırıcılık": int(test["Class"].sum()),
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
    hedef = sys.argv[1] if len(sys.argv) > 1 else "hepsi"
    if hedef in ("bist", "hepsi"):
        print(bist_eda())
    if hedef in ("fraud", "hepsi"):
        print(fraud_eda())
