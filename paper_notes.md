# Fixed-Rate Bond Yield Modeling Notes

## Research-Style Explanation
The fixed-rate side starts from the observation that yield should not be modeled directly as a pure function of coupon and price. Instead, the correct structure is:

Yield = Benchmark + Spread

### Why this matters
Two bonds with identical coupons but different maturities should not have the same benchmark. Benchmark assignment must depend on term structure.

### Workflow
1. Build / load Treasury curve for the trade date.
2. Interpolate benchmark rate by maturity.
3. Define spread as reported yield minus benchmark.
4. Model spread instead of raw yield.

### Key message for interviews
The project is not just a regression. It is a fixed-income decomposition:
- Treasury term structure first,
- spread second,
- pricing features third.
