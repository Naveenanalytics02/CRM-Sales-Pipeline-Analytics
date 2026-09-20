import pandas as pd

accounts = pd.read_csv("Data/Cleaned/accounts_cleaned.csv")
products = pd.read_csv("Data/Cleaned/products_cleaned.csv")
sales_pipeline = pd.read_csv("Data/Cleaned/sales_pipeline_cleaned.csv")
sales_teams = pd.read_csv("Data/Cleaned/sales_teams_cleaned.csv")

print("Data loaded successfully.")

print("\nAccounts:", accounts.shape)
print("Products:", products.shape)
print("Sales Pipeline:", sales_pipeline.shape)
print("Sales Teams:", sales_teams.shape)

print("\n========== BASIC STATISTICS ==========")

print("\nSales Pipeline:")
print(sales_pipeline.describe())

print("\nAccounts:")
print(accounts.describe())

print("\nProducts:")
print(products.describe())

print("\n========== DEAL STAGE ANALYSIS ==========")

stage_counts = sales_pipeline["deal_stage"].value_counts()

print(stage_counts)

print("\n========== WIN/LOSS ANALYSIS ==========")

completed_deals = sales_pipeline[
    sales_pipeline["deal_stage"].isin(["Won", "Lost"])
]

won_deals = (completed_deals["deal_stage"] == "Won").sum()
lost_deals = (completed_deals["deal_stage"] == "Lost").sum()

win_rate = won_deals / len(completed_deals) * 100

print("Won deals:", won_deals)
print("Lost deals:", lost_deals)
print("Win rate:", round(win_rate, 2), "%")

print("\n========== REVENUE ANALYSIS ==========")

won_revenue = sales_pipeline.loc[
    sales_pipeline["deal_stage"] == "Won",
    "close_value"
].sum()

average_won_deal = sales_pipeline.loc[
    sales_pipeline["deal_stage"] == "Won",
    "close_value"
].mean()

print("Total won revenue:", won_revenue)
print("Average won deal:", round(average_won_deal, 2))

print("\n========== PRODUCT PERFORMANCE ==========")

product_performance = sales_pipeline[
    sales_pipeline["deal_stage"] == "Won"
].groupby("product").agg(
    won_deals=("opportunity_id", "count"),
    won_revenue=("close_value", "sum"),
    average_deal=("close_value", "mean")
).sort_values("won_revenue", ascending=False)

print(product_performance)

print("\n========== SALES AGENT PERFORMANCE ==========")

agent_performance = sales_pipeline[
    sales_pipeline["deal_stage"].isin(["Won", "Lost"])
].groupby("sales_agent").agg(
    completed_deals=("opportunity_id", "count"),
    won_deals=("deal_stage", lambda x: (x == "Won").sum())
)

agent_performance["win_rate"] = (
    agent_performance["won_deals"]
    / agent_performance["completed_deals"]
    * 100
)

agent_performance = agent_performance.sort_values(
    "win_rate",
    ascending=False
)

print(agent_performance.head(10))

print("\n========== MONTHLY REVENUE TREND ==========")

won_sales = sales_pipeline[
    sales_pipeline["deal_stage"] == "Won"
].copy()

won_sales["close_date"] = pd.to_datetime(won_sales["close_date"])

monthly_revenue = won_sales.groupby(
    won_sales["close_date"].dt.to_period("M")
)["close_value"].sum()

print(monthly_revenue)

print("\n========== REGIONAL PERFORMANCE ==========")

regional_performance = sales_pipeline[
    sales_pipeline["deal_stage"].isin(["Won", "Lost"])
].merge(
    sales_teams[["sales_agent", "regional_office"]],
    on="sales_agent",
    how="left"
)

regional_performance = regional_performance.groupby(
    "regional_office"
).agg(
    completed_deals=("opportunity_id", "count"),
    won_deals=("deal_stage", lambda x: (x == "Won").sum()),
    won_revenue=("close_value", "sum")
)

regional_performance["win_rate"] = (
    regional_performance["won_deals"]
    / regional_performance["completed_deals"]
    * 100
)

print(
    regional_performance.sort_values(
        "win_rate",
        ascending=False
    )
)

print("\n========== ACCOUNT PERFORMANCE ==========")

account_performance = sales_pipeline[
    (sales_pipeline["deal_stage"] == "Won") &
    (sales_pipeline["account"] != "Unknown")
].groupby("account").agg(
    won_deals=("opportunity_id", "count"),
    won_revenue=("close_value", "sum"),
    average_deal=("close_value", "mean")
).sort_values("won_revenue", ascending=False)

print(account_performance.head(10))

print("\n========== SECTOR PERFORMANCE ==========")

sector_performance = sales_pipeline[
    (sales_pipeline["deal_stage"].isin(["Won", "Lost"])) &
    (sales_pipeline["account"] != "Unknown")
].merge(
    accounts[["account", "sector"]],
    on="account",
    how="left"
)

sector_performance = sector_performance.groupby(
    "sector"
).agg(
    completed_deals=("opportunity_id", "count"),
    won_deals=("deal_stage", lambda x: (x == "Won").sum()),
    won_revenue=("close_value", "sum")
)

sector_performance["win_rate"] = (
    sector_performance["won_deals"]
    / sector_performance["completed_deals"]
    * 100
)

print(
    sector_performance.sort_values(
        "won_revenue",
        ascending=False
    )
)

print("\n========== DEAL CYCLE TIME ==========")

won_sales = sales_pipeline[
    (sales_pipeline["deal_stage"] == "Won") &
    (sales_pipeline["engage_date"].notna()) &
    (sales_pipeline["close_date"].notna())
].copy()

won_sales["engage_date"] = pd.to_datetime(won_sales["engage_date"])
won_sales["close_date"] = pd.to_datetime(won_sales["close_date"])

won_sales["days_to_close"] = (
    won_sales["close_date"] - won_sales["engage_date"]
).dt.days

print("Average days to close:", round(won_sales["days_to_close"].mean(), 2))
print("Fastest deal:", won_sales["days_to_close"].min(), "days")
print("Longest deal:", won_sales["days_to_close"].max(), "days")

import matplotlib.pyplot as plt

print("\n========== DEAL STAGE CHART ==========")

stage_counts = sales_pipeline["deal_stage"].value_counts()

stage_counts.plot(kind="bar")

plt.title("Deal Stage Distribution")
plt.xlabel("Deal Stage")
plt.ylabel("Number of Opportunities")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

print("\n========== MONTHLY REVENUE CHART ==========")

monthly_revenue.plot(kind="line", marker="o")

plt.title("Monthly Won Revenue")
plt.xlabel("Month")
plt.ylabel("Won Revenue ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n========== PRODUCT REVENUE CHART ==========")

product_revenue = sales_pipeline[
    sales_pipeline["deal_stage"] == "Won"
].groupby("product")["close_value"].sum().sort_values(
    ascending=False
)

product_revenue.plot(kind="bar")

plt.title("Won Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Won Revenue ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("\n========== SALES AGENT WIN RATE CHART ==========")

top_agents = agent_performance.head(10)["win_rate"].sort_values()

top_agents.plot(kind="barh")

plt.title("Top 10 Sales Agents by Win Rate")
plt.xlabel("Win Rate (%)")
plt.ylabel("Sales Agent")
plt.tight_layout()
plt.show()

print("\n========== REGIONAL REVENUE CHART ==========")

regional_revenue = regional_performance["won_revenue"].sort_values(
    ascending=False
)

regional_revenue.plot(kind="bar")

plt.title("Won Revenue by Region")
plt.xlabel("Regional Office")
plt.ylabel("Won Revenue ($)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()