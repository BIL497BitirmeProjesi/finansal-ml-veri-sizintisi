"""Veri indirme ve doğrulama. Kullanım: python src/veri_indir.py [bist|fraud]"""
import hashlib
import sys
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blok in iter(lambda: f.read(1 << 20), b""):
            h.update(blok)
    return h.hexdigest()


def bist() -> None:
    import yfinance as yf
    df = yf.download("XU100.IS", start="2016-10-01", end="2026-10-02", auto_adjust=False)
    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)
    yol = RAW / "xu100.csv"
    df.to_csv(yol)
    print(yol, df.shape)
    print("SHA-256:", sha256(yol))


def fraud() -> None:
    import pandas as pd
    yol = RAW / "creditcard.csv"
    if not yol.exists():
        sys.exit(f"{yol} yok. Kaggle'dan indirip data/raw/ altına koyun (bkz. data/README.md).")
    df = pd.read_csv(yol)
    print(yol, df.shape, "(beklenen: 284807, 31)")
    print("SHA-256:", sha256(yol))


if __name__ == "__main__":
    hedef = sys.argv[1] if len(sys.argv) > 1 else ""
    {"bist": bist, "fraud": fraud}.get(hedef, lambda: sys.exit(__doc__))()
