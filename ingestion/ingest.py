import os
import logging
import pandas as pd
from dotenv import load_dotenv
from cleaning.validate import clean_and_validate

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

RAW_DATA_PATH     = "data/raw/retail_sales_dataset.csv"
CLEANED_DATA_PATH = "data/cleaned/retail_sales_cleaned.csv"

def ingest_csv():
    logger.info(f"Reading raw CSV: {RAW_DATA_PATH}")
    df = pd.read_csv(RAW_DATA_PATH)
    logger.info(f"Loaded {len(df)} rows")

    df_clean = clean_and_validate(df)

    os.makedirs("data/cleaned", exist_ok=True)
    df_clean.to_csv(CLEANED_DATA_PATH, index=False)
    logger.info(f"Cleaned file saved to {CLEANED_DATA_PATH}")

    return df_clean

if __name__ == "__main__":
    df = ingest_csv()
    print(f"\nCleaned dataset shape: {df.shape}")
    print(f"Columns: {df.columns.tolist()}")
    print(f"\nSample:")
    print(df.head(3).to_string())