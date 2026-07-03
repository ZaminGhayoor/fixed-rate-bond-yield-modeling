import pandas as pd
import numpy as np

curve = pd.read_csv("CLASSIFIED")

curve["years"] = pd.to_numeric(curve["years"], errors="coerce")
curve["yield"] = pd.to_numeric(curve["yield"], errors="coerce")
curve = curve.dropna().sort_values("years")

curve_years = curve["years"].values
curve_rates = curve["yield"].values

def get_rate(years_to_maturity: float) -> float:
    return float(np.interp(years_to_maturity, curve_years, curve_rates))
