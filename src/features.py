import numpy as np
import pandas as pd

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """Genera columnas derivadas como rating_per_euro, índices y categorías."""

    # ---------------------------
    # Paso 0: Precios válidos
    # ---------------------------
    assert (df["price"] > 0).all(), "Hay precios negativos o nulos"

    # ---------------------------
    # Paso 1: rating_per_euro
    # ---------------------------
    df["rating_per_euro"] = (np.exp(df["rating"]) / np.log(df["price"])).round(2)

    # ---------------------------
    # Paso 2: índices
    # ---------------------------
    df["support_index"] = (df["tannin"] + df["style_acidity"]) / 2
    df["volume_index"] = (df["style_body"] + df["intensity"]) / 2

    # ---------------------------
    # Paso 3: clasificación en 3 categorías + Other
    # ---------------------------
    def classify_wine(row):
        IS = row["support_index"]
        IV = row["volume_index"]
        if IS == 0 and IV == 0:
            return "Other"
        elif IS > 3.5 and IV > 3.5:
            return "Structured"
        elif IS <= 2.5 or IV <= 2.5:
            return "Soft"
        else:
            return "Medium"

    df["wine_category"] = df.apply(classify_wine, axis=1)

    return df