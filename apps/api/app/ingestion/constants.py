from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATASET_DIR = BASE_DIR / "data"

COMPANIES_CSV = DATASET_DIR / "companies_germany.csv"
PROBLEMS_CSV = DATASET_DIR / "problems_germany.csv"
MAPPINGS_CSV = DATASET_DIR / "problem_company_mapping.csv"
SECTORS_CSV = DATASET_DIR / "sectors_reference.csv"
