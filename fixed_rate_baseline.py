import pandas as pd
import numpy as np
from curve_utils import get_rate

df = pd.read_csv("clean_trades.csv", low_memory=False)

df["TradeDate"] = pd.to_datetime(df["TradeDate"], errors="coerce")
df["Maturity_trade"] = pd.to_datetime(df["Maturity_trade"], errors="coerce")
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df["Coupon_trade"] = pd.to_numeric(df["Coupon_trade"], errors="coerce")
df["ReportedYield"] = pd.to_numeric(df["ReportedYield"], errors="coerce")

df["years_to_maturity"] = (df["Maturity_trade"] - df["TradeDate"]).dt.days / 365.25
df = df.dropna(subset=["years_to_maturity", "ReportedYield", "Price", "Coupon_trade"]).copy()
df = df[df["years_to_maturity"] > 0].copy()

df["BenchmarkRate"] = df["years_to_maturity"].apply(get_rate)
df["Discount"] = 100 - df["Price"]

X0 = np.ones(len(df))
X1 = df["Coupon_trade"].values
X2 = df["Discount"].values
X3 = df["years_to_maturity"].values

X = np.vstack([X0, X1, X2, X3]).T
y = (df["ReportedYield"] - df["BenchmarkRate"]).values

beta = np.linalg.pinv(X) @ y
a, b1, b2, b3 = beta

df["PredictedSpread"] = a + b1 * df["Coupon_trade"] + b2 * df["Discount"] + b3 * df["years_to_maturity"]
df["ComputedYield"] = df["BenchmarkRate"] + df["PredictedSpread"]
df["YieldErrorBps"] = (df["ComputedYield"] - df["ReportedYield"]) * 100
df["AbsErrorBps"] = df["YieldErrorBps"].abs()

print("===== FIXED-RATE BASELINE =====")
print("Mean abs error (bps):", df["AbsErrorBps"].mean())
print("Median abs error (bps):", df["AbsErrorBps"].median())

print("\nCoefficients:")
print(f"intercept = {a:.6f}")
print(f"coupon    = {b1:.6f}")
print(f"discount  = {b2:.6f}")
print(f"years     = {b3:.6f}")

df.to_csv("fixed_rate_baseline_results.csv", index=False)
print("\nSaved: fixed_rate_baseline_results.csv")
