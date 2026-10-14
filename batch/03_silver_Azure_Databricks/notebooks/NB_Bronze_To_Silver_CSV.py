# Databricks notebook source

# ============================================================
# SILVER LAYER PIPELINE
# ============================================================

from pyspark.sql.functions import *

# ============================================================
# ADLS Paths
# ============================================================

bronze_base = "abfss://lakehouse@atliqadls.dfs.core.windows.net/bronze"

# ============================================================
# Read Bronze Data
# ============================================================

supplier_price_list_df = spark.read.parquet(
    f"{bronze_base}/supplier_price_list/"
)

marketing_spend_df = spark.read.parquet(
    f"{bronze_base}/marketing_spend/"
)

# ============================================================
# SUPPLIER PRICE LIST
# Data Cleaning & Standardization
# ============================================================

supplier_price_list_df = (
    supplier_price_list_df
    .select(
        col("product_id").cast("int"),
        col("product_name").cast("string"),
        col("supplier_name").cast("string"),
        col("supplier_cost").cast("decimal(12,2)"),
        col("effective_date").cast("date")
    )
    # Remove duplicate records
    .dropDuplicates()
    # Remove invalid records
    .filter(col("product_id").isNotNull())
    .filter(col("supplier_cost").isNotNull())
    .filter(col("supplier_cost") > 0)
    # Handle null text values
    .fillna({
        "product_name": "Unknown Product",
        "supplier_name": "Unknown Supplier"
    })
    # Audit column
    .withColumn(
        "silver_loaded_at",
        current_timestamp()
    )
)

# ============================================================
# MARKETING SPEND
# Data Cleaning & Standardization
# ============================================================

marketing_spend_df = (
    marketing_spend_df
    .select(
        col("spend_date").cast("date"),
        col("channel").cast("string"),
        col("campaign").cast("string"),
        col("spend_amount").cast("decimal(12,2)"),
        col("clicks").cast("int")
    )
    # Remove duplicate records
    .dropDuplicates()
    # Remove invalid records
    .filter(col("spend_amount").isNotNull())
    .filter(col("spend_amount") >= 0)
    .filter(col("clicks") >= 0)
    # Handle null text values
    .fillna({
        "channel": "Unknown",
        "campaign": "Unknown Campaign"
    })
    # Audit column
    .withColumn(
        "silver_loaded_at",
        current_timestamp()
    )
)

# ============================================================
# WRITE TO UNITY CATALOG SILVER TABLES
# ============================================================

supplier_price_list_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("atliq_dbx.silver.supplier_price_list")

marketing_spend_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("atliq_dbx.silver.marketing_spend")

# ============================================================
# VALIDATION
# ============================================================

print("=" * 50)
print("SILVER LAYER LOAD SUMMARY")
print("=" * 50)

print(
    f"Supplier Price List Records: {supplier_price_list_df.count()}"
)

print(
    f"Marketing Spend Records: {marketing_spend_df.count()}"
)

print("=" * 50)
print("Silver tables loaded successfully.")
print("=" * 50)