from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, upper

# -----------------------------
# SPARK SESSION (GCS SAFE CONFIG)
# -----------------------------
spark = SparkSession.builder \
    .appName("MigrationPipeline") \
    .config("spark.sql.files.maxPartitionBytes", "134217728") \
    .config("spark.hadoop.fs.gs.outputstream.upload.chunk.size", "8388608") \
    .getOrCreate()

# -----------------------------
# INPUT
# -----------------------------
input_path = "gs://migration-raw-zone/customers/*.csv"

df = spark.read.option("header", True).csv(input_path)

# ❌ Avoid multiple full scans (remove duplicate count)
print("Raw count:", df.rdd.getNumPartitions())

# -----------------------------
# CLEANING
# -----------------------------
df = df.dropDuplicates()

df = df.withColumn("name", upper(trim(col("name"))))
df = df.filter(col("email").isNotNull())

# optional: cache BEFORE any action if reused
df.cache()

print("Cleaned rows approx ready")

# -----------------------------
# OUTPUT
# -----------------------------
output_path = "gs://migration-processed-zone/customers/"

# IMPORTANT: coalesce helps stabilize write on Dataproc small clusters
df.coalesce(4).write.mode("overwrite").parquet(output_path)

print("✅ Spark job completed successfully")