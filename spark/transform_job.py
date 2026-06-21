from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper

# -----------------------------
# CREATE SPARK SESSION
# -----------------------------
spark = SparkSession.builder \
    .appName("MigrationPipeline") \
    .getOrCreate()

# -----------------------------
# INPUT PATH (GCS RAW)
# -----------------------------
input_path = "gs://migration-raw-zone/customers/*.csv"

# -----------------------------
# READ DATA
# -----------------------------
df = spark.read.option("header", True).csv(input_path)

print("Raw count:", df.count())

# -----------------------------
# DATA CLEANING
# -----------------------------

# Remove duplicates
df = df.dropDuplicates()

# Trim + uppercase name column (example transformation)
df = df.withColumn("name", upper(trim(col("name"))))

# Remove null emails
df = df.filter(col("email").isNotNull())

print("Cleaned count:", df.count())

# -----------------------------
# OUTPUT PATH (PROCESSED ZONE)
# -----------------------------
output_path = "gs://migration-processed-zone/customers/"

# -----------------------------
# WRITE DATA
# -----------------------------
df.write.mode("overwrite").parquet(output_path)

print("✅ Spark job completed")