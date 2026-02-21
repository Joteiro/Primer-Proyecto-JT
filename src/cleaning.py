import pandas as pd
import numpy as np
import re

def clean(df: pd.DataFrame) -> pd.DataFrame:
    """Limpieza de columnas y datos del dataset Vivino."""

    # ---------------------------
    # 1️⃣ Limpiar columna 'stock'
    # ---------------------------
    text_to_num = {
        "cero": 0, "uno": 1, "dos": 2, "tres": 3, "cuatro": 4,
        "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
        "diez": 10
    }

    df["stock"] = (
        df["stock"]
            .astype(str)
            .str.strip()
            .str.lower()
            .replace(text_to_num)
            .pipe(pd.to_numeric, errors="coerce")
            .fillna(0)
            .astype(int)
    )

    # ---------------------------
    # 2️⃣ Imputación de valores missing (ejemplo White Ribera)
    # ---------------------------
    num_cols = ["style_body", "style_acidity", "intensity", "sweetness"]
    cat_cols = ["style"]

    df_missing = df[df[num_cols].isna().any(axis=1)]
    for idx in df_missing.index:
        row = df.loc[idx]
        group = df[(df["wine_type"] == row["wine_type"]) & (df["region"] == row["region"])]
        # Imputar numéricas
        group_means = group[num_cols].mean()
        for col in num_cols:
            df.loc[idx, col] = group_means[col]
        # Imputar categórica
        group_mode = group["style"].mode()
        df.loc[idx, "style"] = group_mode[0] if len(group_mode) > 0 else np.nan

    # ---------------------------
    # 3️⃣ Limpiar nombres y estilos
    # ---------------------------
    # Eliminar año final del wine_name
    pattern = r'\s?(19\d{2}|20\d{2})$'
    df["wine_name"] = df["wine_name"].str.replace(pattern, '', regex=True).str.strip()

    # Quitar "(España)" de style
    df["style"] = df["style"].str.replace(r'\(España\)', '', regex=True).str.strip()

    # Eliminar columnas innecesarias
    drop_cols = ["country", "year_from_name", "year_candidates"]
    df = df.drop(columns=[c for c in drop_cols if c in df.columns])

    return df