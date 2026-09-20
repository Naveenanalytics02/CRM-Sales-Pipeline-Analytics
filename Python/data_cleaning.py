import pandas as pd
from pathlib import Path

# Find the project folder automatically
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "Data"

# Load datasets
accounts = pd.read_csv(DATA_DIR / "accounts.csv")
products = pd.read_csv(DATA_DIR / "products.csv")
sales_pipeline = pd.read_csv(DATA_DIR / "sales_pipeline.csv")
sales_teams = pd.read_csv(DATA_DIR / "sales_teams.csv")

# Display basic information
print("\n========== ACCOUNTS ==========")
print(accounts.head())
print("Shape:", accounts.shape)
print("Columns:", accounts.columns.tolist())

print("\n========== PRODUCTS ==========")
print(products.head())
print("Shape:", products.shape)
print("Columns:", products.columns.tolist())

print("\n========== SALES PIPELINE ==========")
print(sales_pipeline.head())
print("Shape:", sales_pipeline.shape)
print("Columns:", sales_pipeline.columns.tolist())

print("\n========== SALES TEAMS ==========")
print(sales_teams.head())
print("Shape:", sales_teams.shape)
print("Columns:", sales_teams.columns.tolist())

print("\n========== MISSING VALUES ==========")

print("\nACCOUNTS")
print(accounts.isnull().sum())

print("\nPRODUCTS")
print(products.isnull().sum())

print("\nSALES PIPELINE")
print(sales_pipeline.isnull().sum())

print("\nSALES TEAMS")
print(sales_teams.isnull().sum())

print("\n========== UNIQUE VALUES ==========")

print("\nACCOUNTS - SECTOR")
print(accounts['sector'].unique())

print("\nACCOUNTS - OFFICE LOCATION")
print(accounts['office_location'].unique())

print("\nPRODUCTS - PRODUCT")
print(products['product'].unique())

print("\nSALES PIPELINE - PRODUCT")
print(sales_pipeline['product'].unique())

print("\nSALES PIPELINE - DEAL STAGE")
print(sales_pipeline['deal_stage'].unique())

# ==========================================
# DATA CLEANING
# ==========================================

# Fix spelling errors in ACCOUNTS
accounts["sector"] = accounts["sector"].replace({
    "technolgy": "technology"
})

accounts["office_location"] = accounts["office_location"].replace({
    "Philipines": "Philippines"
})

# Fix product name inconsistency in SALES PIPELINE
sales_pipeline["product"] = sales_pipeline["product"].replace({
    "GTXPro": "GTX Pro"
})

print("\n========== AFTER SPELLING CLEANING ==========")

print("\nACCOUNT SECTORS:")
print(accounts["sector"].unique())

print("\nACCOUNT LOCATIONS:")
print(accounts["office_location"].unique())

print("\nSALES PIPELINE PRODUCTS:")
print(sales_pipeline["product"].unique())

print("\n========== DUPLICATE CHECK ==========")

print("\nACCOUNTS DUPLICATES:")
print(accounts.duplicated().sum())

print("\nPRODUCTS DUPLICATES:")
print(products.duplicated().sum())

print("\nSALES PIPELINE DUPLICATES:")
print(sales_pipeline.duplicated().sum())

print("\nSALES TEAMS DUPLICATES:")
print(sales_teams.duplicated().sum())

print("\nDUPLICATE OPPORTUNITY IDs:")
print(sales_pipeline["opportunity_id"].duplicated().sum())

print("\n========== DATE CLEANING ==========")

sales_pipeline["engage_date"] = pd.to_datetime(
    sales_pipeline["engage_date"],
    format="%d-%m-%Y",
    errors="coerce"
)

sales_pipeline["close_date"] = pd.to_datetime(
    sales_pipeline["close_date"],
    format="%d-%m-%Y",
    errors="coerce"
)

print("\nENGAGE DATE DATA TYPE:")
print(sales_pipeline["engage_date"].dtype)

print("\nCLOSE DATE DATA TYPE:")
print(sales_pipeline["close_date"].dtype)

print("\nSAMPLE DATES:")
print(sales_pipeline[["engage_date", "close_date"]].head())

print("\n========== MISSING VALUE ANALYSIS ==========")

print("\nSales Pipeline Missing Values:")
print(sales_pipeline.isnull().sum())

print("\nDeal Stage vs Missing Close Date:")
print(
    sales_pipeline.groupby("deal_stage")["close_date"]
    .apply(lambda x: x.isnull().sum())
)

print("\nDeal Stage vs Missing Close Value:")
print(
    sales_pipeline.groupby("deal_stage")["close_value"]
    .apply(lambda x: x.isnull().sum())
)

print("\n========== HANDLING MISSING VALUES ==========")

# 1. Accounts: missing parent company means the company is independent
accounts["subsidiary_of"] = accounts["subsidiary_of"].fillna("Independent")

# 2. Sales Pipeline: missing account means account is unknown
sales_pipeline["account"] = sales_pipeline["account"].fillna("Unknown")

# 3. Do NOT fill missing dates or close values
# They are legitimately missing for open deals:
# Engaging and Prospecting deals have not closed yet.

print("\nAfter handling missing values:")

print("\nACCOUNTS:")
print(accounts.isnull().sum())

print("\nSALES PIPELINE:")
print(sales_pipeline.isnull().sum())

print("\n========== SAMPLE CLEANED DATA ==========")

print("\nACCOUNTS:")
print(accounts.head())

print("\nSALES PIPELINE:")
print(sales_pipeline.head())

print("\n========== NUMERICAL DATA VALIDATION ==========")

print("\nAccounts - Revenue:")
print("Minimum:", accounts["revenue"].min())
print("Maximum:", accounts["revenue"].max())

print("\nAccounts - Employees:")
print("Minimum:", accounts["employees"].min())
print("Maximum:", accounts["employees"].max())

print("\nAccounts - Year Established:")
print("Minimum:", accounts["year_established"].min())
print("Maximum:", accounts["year_established"].max())

print("\nProducts - Sales Price:")
print("Minimum:", products["sales_price"].min())
print("Maximum:", products["sales_price"].max())

print("\nSales Pipeline - Close Value:")
print("Minimum:", sales_pipeline["close_value"].min())
print("Maximum:", sales_pipeline["close_value"].max())

print("\n========== CATEGORICAL CLEANING ==========")

# Fix inconsistent values in Accounts
accounts["sector"] = accounts["sector"].replace({
    "technolgy": "technology"
})

accounts["office_location"] = accounts["office_location"].replace({
    "Philipines": "Philippines"
})

# Fix inconsistent product name in Sales Pipeline
sales_pipeline["product"] = sales_pipeline["product"].replace({
    "GTXPro": "GTX Pro"
})

print("\nCategorical values cleaned successfully.")

print("\n========== VERIFY CATEGORICAL CLEANING ==========")

print("\nAccount Sectors:")
print(accounts["sector"].unique())

print("\nOffice Locations:")
print(accounts["office_location"].unique())

print("\nProducts in Sales Pipeline:")
print(sales_pipeline["product"].unique())

print("\n========== ZERO CLOSE VALUE CHECK ==========")

zero_value_deals = sales_pipeline[
    sales_pipeline["close_value"] == 0
]

print("\nNumber of zero-value deals:")
print(len(zero_value_deals))

print("\nZero-value deals by stage:")
print(zero_value_deals["deal_stage"].value_counts())

print("\n========== DATE CONSISTENCY CHECK ==========")

invalid_dates = sales_pipeline[
    (sales_pipeline["close_date"].notna()) &
    (sales_pipeline["engage_date"].notna()) &
    (sales_pipeline["close_date"] < sales_pipeline["engage_date"])
]

print("\nDeals where close date is before engage date:")
print(len(invalid_dates))

print("\n========== TABLE RELATIONSHIP CHECK ==========")

# Accounts used in Sales Pipeline but missing from Accounts table
missing_accounts = set(sales_pipeline["account"]) - set(accounts["account"])

# Products used in Sales Pipeline but missing from Products table
missing_products = set(sales_pipeline["product"]) - set(products["product"])

# Sales agents used in Sales Pipeline but missing from Sales Teams table
missing_agents = set(sales_pipeline["sales_agent"]) - set(sales_teams["sales_agent"])

print("\nAccounts missing from Accounts table:")
print(missing_accounts)

print("\nProducts missing from Products table:")
print(missing_products)

print("\nSales agents missing from Sales Teams table:")
print(missing_agents)

print("\n========== FINAL MISSING VALUE CHECK ==========")

print("\nAccounts:")
print(accounts.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nSales Pipeline:")
print(sales_pipeline.isnull().sum())

print("\nSales Teams:")
print(sales_teams.isnull().sum())

import os

# Create Cleaned folder
os.makedirs("Data/Cleaned", exist_ok=True)

# Save cleaned datasets
accounts.to_csv("Data/Cleaned/accounts_cleaned.csv", index=False)
products.to_csv("Data/Cleaned/products_cleaned.csv", index=False)
sales_pipeline.to_csv("Data/Cleaned/sales_pipeline_cleaned.csv", index=False)
sales_teams.to_csv("Data/Cleaned/sales_teams_cleaned.csv", index=False)

print("\n========== CLEANED FILES SAVED ==========")
print("All cleaned datasets saved successfully.")