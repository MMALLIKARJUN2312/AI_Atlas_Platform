from pathlib import Path

import pandas as pd

COLUMN_ALIASES = {
    "Financial Impact (â‚¬)": "Financial Impact (€)",
    "MÃ¼ller": "Müller",
}


def read_csv(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(
        file_path,
        encoding="utf-8-sig",
    )

    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\ufeff", "", regex=False)
    )

    df.rename(columns=COLUMN_ALIASES, inplace=True)

    return df