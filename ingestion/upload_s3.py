import os
import boto3
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

S3_BUCKET  = os.getenv("S3_BUCKET")
AWS_REGION = os.getenv("AWS_REGION")

def upload_to_s3(local_path: str, source_name: str) -> str:
    date_partition = datetime.utcnow().strftime("%Y/%m/%d")
    timestamp      = datetime.utcnow().strftime("%H%M%S")
    s3_key = f"raw/{source_name}/{date_partition}/{source_name}_{timestamp}.csv"

    logger.info(f"Uploading {local_path} to s3://{S3_BUCKET}/{s3_key}")

    s3 = boto3.client("s3", region_name=AWS_REGION)
    s3.upload_file(local_path, S3_BUCKET, s3_key)

    logger.info(f"Upload complete: s3://{S3_BUCKET}/{s3_key}")
    return s3_key

if __name__ == "__main__":
    key = upload_to_s3(
        local_path="data/cleaned/retail_sales_cleaned.csv",
        source_name="retail_sales"
    )
    print(f"\nFile uploaded successfully to:")
    print(f"s3://{S3_BUCKET}/{key}")