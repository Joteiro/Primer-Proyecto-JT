from pathlib import Path
from src.io import load_csv
from src.cleaning import clean
from src.features import build_features
from src.viz import (
    create_graphs_folder,
    plot_histogram,
    plot_style_region_heatmaps,
    plot_year_analysis,
    plot_sankey
)

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

    create_graphs_folder()
    plot_histogram(df)
    plot_style_region_heatmaps(df)
    plot_year_analysis(df)
    plot_sankey(df)
    print("Proceso finalizado. CSV limpio y gráficos generados.")

if __name__ == "__main__":
    main()