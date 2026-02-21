from pathlib import Path
from src.io import load_csv
from src.cleaning import clean
from src.features import build_features

def main():
    root = Path(__file__).resolve().parent
    raw_path = root / "data" / "raw" / "vivino_raw.csv"
    out_path = root / "data" / "processed" / "vivino_clean.csv"

    df = load_csv(raw_path)
    df = clean(df)
    df = build_features(df)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()