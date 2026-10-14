# Databricks notebook source
# MAGIC %md
# MAGIC This notebook generates Silver layer data

# ============================================================
# Imports
# ============================================================

from pyspark.sql.functions import *
from pyspark.sql.window import Window

# ============================================================
# ADLS Paths (Unity Catalog External Location)
# ============================================================

bronze_base = "abfss://lakehouse@atliqadls.dfs.core.windows.net/bronze"
silver_base = "abfss://lakehouse@atliqadls.dfs.core.windows.net/silver"

# ============================================================
# Read Bronze Data
# ============================================================

orders_df = spark.read.parquet(f"{bronze_base}/orders/")
order_items_df = spark.read.parquet(f"{bronze_base}/order_items/")
payments_df = spark.read.parquet(f"{bronze_base}/payments/")
customers_df = spark.read.parquet(f"{bronze_base}/customers/")
products_df = spark.read.parquet(f"{bronze_base}/products/")

# ============================================================
# ORDERS
# Reviewer Fix:
# - Restore order_amount
# - Keep latest record by updated_at
# ============================================================

orders_window = Window.partitionBy("order_id") \
    .orderBy(col("updated_at").desc())

orders_df = (
    orders_df
    .select(
        col("order_id").cast("int"),
        col("customer_id").cast("int"),
        col("order_date").cast("date"),
        col("status").cast("string"),
        col("order_amount").cast("decimal(12,2)"),
        col("updated_at").cast("timestamp")
    )
    .withColumn(
        "rn",
        row_number().over(orders_window)
    )
    .filter(col("rn") == 1)
    .drop("rn")
    .fillna({"status": "unknown"})
    .withColumn(
        "silver_loaded_at",
        current_timestamp()
    )
)

# ============================================================
# ORDER ITEMS
# Reviewer Fix:
# - Restore item_price
# - Keep latest record
# ============================================================

order_items_window = Window.partitionBy("order_item_id") \
    .orderBy(col("created_at").desc())

order_items_df = (
    order_items_df
    .select(
        col("order_item_id").cast("int"),
        col("order_id").cast("int"),
        col("product_id").cast("int"),
        col("quantity").cast("int"),
        col("item_price").cast("decimal(10,2)"),
        col("created_at").cast("timestamp")
    )
    .withColumn(
        "rn",
        row_number().over(order_items_window)
    )
    .filter(col("rn") == 1)
    .drop("rn")
    .withColumn(
        "silver_loaded_at",
        current_timestamp()
    )
)

# ============================================================
# PAYMENTS
# Keep latest payment
# ============================================================

payments_window = Window.partitionBy("payment_id") \
    .orderBy(col("updated_at").desc())

payments_df = (
    payments_df
    .select(
        col("payment_id").cast("int"),
        col("order_id").cast("int"),
        col("amount").cast("double"),
        col("method").cast("string"),
        col("paid_at").cast("timestamp"),
        col("updated_at").cast("timestamp")
    )
    .withColumn(
        "rn",
        row_number().over(payments_window)
    )
    .filter(col("rn") == 1)
    .drop("rn")
    .withColumn(
        "silver_loaded_at",
        current_timestamp()
    )
)

# ============================================================
# CUSTOMERS
# Full refresh table
# ============================================================

customers_window = Window.partitionBy("customer_id") \
    .orderBy(col("updated_at").desc())

customers_df = (
    customers_df
    .select(
        col("customer_id").cast("int"),
        col("customer_name").cast("string"),
        col("email").cast("string"),
        col("city").cast("string"),
        col("signup_date").cast("date"),
        col("updated_at").cast("timestamp")
    )
    .withColumn(
        "rn",
        row_number().over(customers_window)
    )
    .filter(col("rn") == 1)
    .drop("rn")
    .withColumn(
        "silver_loaded_at",
        current_timestamp()
    )
)

# ============================================================
# PRODUCTS
# Full refresh table
# ============================================================

products_window = Window.partitionBy("product_id") \
    .orderBy(col("updated_at").desc())

products_df = (
    products_df
    .select(
        col("product_id").cast("int"),
        col("product_name").cast("string"),
        col("category").cast("string"),
        col("unit_price").cast("double"),
        col("updated_at").cast("timestamp")
    )
    .withColumn(
        "rn",
        row_number().over(products_window)
    )
    .filter(col("rn") == 1)
    .drop("rn")
    .withColumn(
        "silver_loaded_at",
        current_timestamp()
    )
)

# ============================================================
# WRITE TO UNITY CATALOG SILVER TABLES
# ============================================================

orders_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("atliq_dbx.silver.orders")

order_items_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("atliq_dbx.silver.order_items")

payments_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("atliq_dbx.silver.payments")

customers_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("atliq_dbx.silver.customers")

products_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("atliq_dbx.silver.products")

# ============================================================
# VALIDATION
# ============================================================

print("Orders:", orders_df.count())
print("Order Items:", order_items_df.count())
print("Payments:", payments_df.count())
print("Customers:", customers_df.count())
print("Products:", products_df.count())