import yaml
from google.cloud import storage, bigquery
import os

# -----------------------------
# CONFIG LOADER
# -----------------------------
def load_config():
    with open("configs/gcp_config.yaml", "r") as file:
        return yaml.safe_load(file)

config = load_config()

PROJECT_ID = config["project_id"]
BUCKETS = config["buckets"]


# -----------------------------
# SET AUTH (SA)
# -----------------------------
def set_gcp_auth():
    sa_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not sa_path:
        raise Exception("Service Account path not set in environment variable")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_path


# -----------------------------
# GCS CLIENT
# -----------------------------
def get_gcs_client():
    import os
    from google.cloud import storage

    # FORCE credentials explicitly
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\bandari.karthik\GCP_Migration\GCP_MIGRATION\service_account.json"

    return storage.Client(project=PROJECT_ID)

# -----------------------------
# BIGQUERY CLIENT
# -----------------------------
def get_bq_client():
    return bigquery.Client(project=PROJECT_ID)


# -----------------------------
# GET BUCKET BY TYPE
# -----------------------------
def get_bucket(bucket_type: str):
    """
    bucket_type: raw / processed / curated / logs / backup
    """
    client = get_gcs_client()
    return client.bucket(BUCKETS[bucket_type])


# -----------------------------
# TEST CONNECTION
# -----------------------------
def test_connection():
    try:
        client = get_gcs_client()
        buckets = list(client.list_buckets())

        print("\n✅ GCP CONNECTION SUCCESS")
        print("Buckets available:")

        for b in buckets:
            print("-", b.name)

    except Exception as e:
        print("\n❌ GCP CONNECTION FAILED")
        print(e)


# -----------------------------
# RUN DIRECT TEST
# -----------------------------
if __name__ == "__main__":
    test_connection()