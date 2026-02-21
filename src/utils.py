def assert_columns(df, required):
    """Valida que todas las columnas requeridas existan en el DataFrame."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f'Missing columns: {missing}')