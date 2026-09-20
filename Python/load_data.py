import os
import psycopg2
from pathlib import Path


# Project folders
project_folder = Path(__file__).resolve().parent.parent
cleaned_folder = project_folder / "Data" / "Cleaned"

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="sales_analytics",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD")
)

cursor = conn.cursor()

# Load accounts
with open(cleaned_folder / "accounts_cleaned.csv", "r", encoding="utf-8") as file:
    cursor.copy_expert(
        "COPY accounts FROM STDIN WITH CSV HEADER NULL '';",
        file
    )

# Load products
with open(cleaned_folder / "products_cleaned.csv", "r", encoding="utf-8") as file:
    cursor.copy_expert(
        "COPY products FROM STDIN WITH CSV HEADER NULL '';",
        file
    )

# Load sales teams
with open(cleaned_folder / "sales_teams_cleaned.csv", "r", encoding="utf-8") as file:
    cursor.copy_expert(
        "COPY sales_teams FROM STDIN WITH CSV HEADER NULL '';",
        file
    )

# Load sales pipeline
with open(cleaned_folder / "sales_pipeline_cleaned.csv", "r", encoding="utf-8") as file:
    cursor.copy_expert(
        "COPY sales_pipeline FROM STDIN WITH CSV HEADER NULL '';",
        file
    )

conn.commit()

cursor.close()
conn.close()

print("All cleaned data loaded successfully.")