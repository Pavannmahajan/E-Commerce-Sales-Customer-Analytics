import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Dataset folder
data_path = "data"

# Load datasets
customers = pd.read_csv(os.path.join(data_path, "olist_customers_dataset.csv"))
orders = pd.read_csv(os.path.join(data_path, "olist_orders_dataset.csv"))
order_items = pd.read_csv(os.path.join(data_path, "olist_order_items_dataset.csv"))
payments = pd.read_csv(os.path.join(data_path, "olist_order_payments_dataset.csv"))
reviews = pd.read_csv(os.path.join(data_path, "olist_order_reviews_dataset.csv"))
products = pd.read_csv(os.path.join(data_path, "olist_products_dataset.csv"))
sellers = pd.read_csv(os.path.join(data_path, "olist_sellers_dataset.csv"))
category_translation = pd.read_csv(
    os.path.join(data_path, "product_category_name_translation.csv")
)

print("All datasets loaded successfully!")

print("\nDataset Shapes:")
print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Order Items:", order_items.shape)
print("Payments:", payments.shape)
print("Reviews:", reviews.shape)
print("Products:", products.shape)
print("Sellers:", sellers.shape)
print("Category Translation:", category_translation.shape)

# ==========================================
# STEP 2: DATA QUALITY CHECK
# ==========================================

datasets = {
    "Customers": customers,
    "Orders": orders,
    "Order Items": order_items,
    "Payments": payments,
    "Reviews": reviews,
    "Products": products,
    "Sellers": sellers,
    "Category Translation": category_translation
}

for name, df in datasets.items():
    print("\n" + "=" * 50)
    print(name.upper())
    print("=" * 50)

    print("\nMissing Values:")
    missing = df.isnull().sum()
    print(missing[missing > 0])

    print("\nDuplicate Rows:", df.duplicated().sum())

    # ==========================================
# STEP 3: DATA QUALITY SUMMARY
# ==========================================

for name, df in datasets.items():

    total_missing = df.isnull().sum().sum()
    duplicates = df.duplicated().sum()

    print(
        f"{name:25} | "
        f"Rows: {df.shape[0]:6} | "
        f"Missing: {total_missing:6} | "
        f"Duplicates: {duplicates}"
    )


# ==========================================
# STEP 4: MISSING VALUES BY COLUMN
# ==========================================

for name in ["Orders", "Reviews", "Products"]:

    df = datasets[name]

    print("\n" + "=" * 50)
    print(name.upper())
    print("=" * 50)

    missing = df.isnull().sum()
    missing = missing[missing > 0]

    print(missing)


    # ==========================================
# STEP 5: DATA CLEANING
# ==========================================

# 1. Reviews - missing text means customer left no written comment
reviews["review_comment_title"] = reviews["review_comment_title"].fillna("No Comment")
reviews["review_comment_message"] = reviews["review_comment_message"].fillna("No Comment")

# 2. Products - missing category
products["product_category_name"] = (
    products["product_category_name"].fillna("unknown")
)

# 3. Product numerical columns - fill missing values with median
product_numeric_cols = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm"
]

for col in product_numeric_cols:
    products[col] = products[col].fillna(products[col].median())

# 4. Orders
# Do NOT fill missing delivery/approval dates with fake values.
# Missing dates can represent cancelled/unavailable/undelivered orders.

# ==========================================
# VERIFY CLEANING
# ==========================================

print("\n========== AFTER CLEANING ==========")

print("\nReviews Missing Values:")
print(reviews.isnull().sum()[reviews.isnull().sum() > 0])

print("\nProducts Missing Values:")
print(products.isnull().sum()[products.isnull().sum() > 0])

print("\nOrders Missing Values (intentionally retained):")
print(orders.isnull().sum()[orders.isnull().sum() > 0])

# ==========================================
# STEP 6: FEATURE ENGINEERING
# ==========================================

# Convert order date columns to datetime
date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date"
]

for col in date_columns:
    orders[col] = pd.to_datetime(orders[col], errors="coerce")

# Create useful time features
orders["order_year"] = orders["order_purchase_timestamp"].dt.year
orders["order_month"] = orders["order_purchase_timestamp"].dt.month
orders["order_month_year"] = orders["order_purchase_timestamp"].dt.to_period("M")

# Actual delivery time in days
orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.days

# Difference between actual and estimated delivery
orders["delivery_delay_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_estimated_delivery_date"]
).dt.days

# Delivery performance category
orders["delivery_status"] = orders["delivery_delay_days"].apply(
    lambda x: "Early/On Time"
    if pd.notna(x) and x <= 0
    else ("Late" if pd.notna(x) else "Not Delivered")
)

print("\n========== FEATURE ENGINEERING COMPLETE ==========")

print(
    orders[
        [
            "order_purchase_timestamp",
            "order_month_year",
            "delivery_days",
            "delivery_delay_days",
            "delivery_status"
        ]
    ].head()
)

# ==========================================
# STEP 7: MONTHLY REVENUE & ORDER TREND
# ==========================================

import matplotlib.pyplot as plt

# Delivered orders only
delivered_orders = orders[
    orders["order_status"] == "delivered"
][["order_id", "order_purchase_timestamp"]].copy()

# Merge with order items to get revenue
monthly_data = delivered_orders.merge(
    order_items[["order_id", "price"]],
    on="order_id",
    how="inner"
)

# Create month
monthly_data["month"] = (
    monthly_data["order_purchase_timestamp"]
    .dt.to_period("M")
)

# Monthly KPIs
monthly_summary = (
    monthly_data.groupby("month")
    .agg(
        total_revenue=("price", "sum"),
        total_orders=("order_id", "nunique")
    )
    .reset_index()
)

monthly_summary["month"] = monthly_summary["month"].astype(str)

print("\n========== MONTHLY BUSINESS PERFORMANCE ==========")
print(monthly_summary)

# Revenue chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_summary["month"],
    monthly_summary["total_revenue"],
    marker="o"
)

plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# Orders chart
plt.figure(figsize=(12, 6))

plt.plot(
    monthly_summary["month"],
    monthly_summary["total_orders"],
    marker="o"
)

plt.title("Monthly Order Growth")
plt.xlabel("Month")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

# ==========================================
# STEP 8: TOP 10 PRODUCT CATEGORIES BY REVENUE
# ==========================================

# Merge order items with products
category_data = order_items.merge(
    products[["product_id", "product_category_name"]],
    on="product_id",
    how="left"
)

# Add English category names
category_data = category_data.merge(
    category_translation,
    on="product_category_name",
    how="left"
)

# Use original category if English translation is unavailable
category_data["category"] = (
    category_data["product_category_name_english"]
    .fillna(category_data["product_category_name"])
    .fillna("unknown")
)

# Keep only delivered orders
delivered_ids = orders.loc[
    orders["order_status"] == "delivered",
    ["order_id"]
]

category_data = category_data.merge(
    delivered_ids,
    on="order_id",
    how="inner"
)

# Calculate revenue by category
top_categories = (
    category_data.groupby("category")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .sort_values()
)

print("\n========== TOP 10 CATEGORIES BY REVENUE ==========")
print(top_categories.sort_values(ascending=False))

# Plot
plt.figure(figsize=(12, 7))

top_categories.plot(kind="barh")

plt.title("Top 10 Product Categories by Revenue")
plt.xlabel("Total Revenue")
plt.ylabel("Product Category")
plt.tight_layout()
plt.show()

# ==========================================
# STEP 9: DELIVERY PERFORMANCE
# ==========================================

delivery_analysis = orders[
    orders["delivery_status"].isin(["Early/On Time", "Late"])
]["delivery_status"].value_counts()

print("\n========== DELIVERY PERFORMANCE ==========")
print(delivery_analysis)

print(
    "\nAverage Delivery Days:",
    round(orders["delivery_days"].mean(), 2)
)

plt.figure(figsize=(7, 5))
delivery_analysis.plot(kind="bar")

plt.title("Delivery Performance")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Orders")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()