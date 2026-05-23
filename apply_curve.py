import pandas as pd
from curve_utils import get_rate

df = pd.read_csv("clean_trades.csv", low_memory=False)

df["TradeDate"] = pd.to_datetime(df["TradeDate"], errors="coerce")
df["Maturity_trade"] = pd.to_datetime(df["Maturity_trade"], errors="coerce")
df["ReportedYield"] = pd.to_numeric(df["ReportedYield"], errors="coerce")

df["years_to_maturity"] = (df["Maturity_trade"] - df["TradeDate"]).dt.days / 365.25
df = df.dropna(subset=["years_to_maturity", "ReportedYield"]).copy()
df = df[df["years_to_maturity"] > 0].copy()

df["BenchmarkRate"] = df["years_to_maturity"].apply(get_rate)
df["Spread"] = df["ReportedYield"] - df["BenchmarkRate"]

print(df[["CUSIP", "years_to_maturity", "BenchmarkRate", "ReportedYield", "Spread"]].head(10).to_string(index=False))
print("\nRows:", len(df))
