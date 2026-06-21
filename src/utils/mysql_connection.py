import mysql.connector
import pandas as pd
import os
from dotenv import load_dotenv

# -----------------------------
# DB CONFIG (TEMP - later move to yaml)
# -----------------------------

load_dotenv()  # Load environment variables from .env file

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}


# -----------------------------
# CONNECT MYSQL
# -----------------------------
def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ MySQL Connected")
        return conn
    except Exception as e:
        print("❌ MySQL Connection Failed")
        raise e


# -----------------------------
# READ TABLE INTO DATAFRAME
# -----------------------------
def read_table(query: str):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


if __name__ == "__main__":
    # Quick manual test when running this module directly
    try:
        conn = get_connection()
        # Close immediately — avoid running any queries by default
        conn.close()
        print("Connection test completed.")
    except Exception as e:
        print(f"Connection test failed: {e}")

query = "SELECT * FROM customers LIMIT 5;"  # Replace with your actual table name
df = read_table(query)
print(df)
