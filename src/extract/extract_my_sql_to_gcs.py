from src.utils.mysql_connection import read_table
from src.utils.gcp_clients import get_gcs_client, config

import os

# -----------------------------
# TABLE CONFIG
# -----------------------------
TABLES = {
    "customers": "SELECT * FROM customers",
    "orders": "SELECT * FROM orders",
    "products": "SELECT * FROM products"
}


# -----------------------------
# GCS UPLOAD FUNCTION
# -----------------------------
def upload_to_gcs(file_path, bucket_name, destination_blob):
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)

    blob.upload_from_filename(file_path)

    print(f"✅ Uploaded: gs://{bucket_name}/{destination_blob}")


# -----------------------------
# MAIN PIPELINE
# -----------------------------
def run_pipeline():
    raw_bucket = config["buckets"]["raw"]

    for table_name, query in TABLES.items():

        print(f"\n🚀 Processing table: {table_name}")

        # STEP 1: Extract
        df = read_table(query)
        print(f"✅ Extracted {len(df)} rows from {table_name}")

        # STEP 2: Save CSV
        file_name = f"{table_name}.csv"
        df.to_csv(file_name, index=False)
        print(f"✅ CSV created: {file_name}")

        # STEP 3: Upload to GCS
        destination = f"{table_name}/{file_name}"
        upload_to_gcs(file_name, raw_bucket, destination)


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    run_pipeline()