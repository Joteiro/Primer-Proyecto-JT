from pathlib import Path
import pandas as pd

def load_csv(path: Path) -> pd.DataFrame:
    """Carga un CSV desde la ruta indicada."""
    df = pd.read_csv(path)
    return df