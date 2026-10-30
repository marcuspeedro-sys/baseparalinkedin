# Atlas Consumer Goods | Financial Validation & Variance Analysis v1.0

**Independent synthetic case; FY2025; USD.** No confidential or real employer data.

## Data integrity
- 20 SKUs, 12 months, 240 sales records, 72 operating expense records.
- Each sales row reconciles exactly to units × unit price/cost, within USD 0.01; 0 discrepancies.
- Independently recomputed annual P&L from source CSVs. Formula definitions in `build_atlas.py` inspected. Excel cached formula results were not independently certified.

## FY2025 P&L
| USD | Budget | Actual | Actual less budget |
|---|---:|---:|---:|
| Revenue | 11,468,158.93 | 11,664,111.57 | +195,952.64 |
| COGS | 6,649,623.65 | 7,347,741.24 | +698,117.59 (unfavorable) |
| Gross profit | 4,818,535.28 | 4,316,370.33 | -502,164.95 |
| OPEX | 4,239,601.20 | 4,418,552.04 | +178,950.84 (unfavorable) |
| EBITDA proxy | 578,934.08 | -102,181.71 | -681,115.79 |
| Gross margin | 42.0166% | 37.0056% | -5.0111 percentage points |

EBITDA is a **proxy** because depreciation, amortization, taxes and financing are not separately modeled.

## Exact revenue bridge (USD)
The total volume and mix effects use 240 SKU-month buckets, with `Pbar = budget revenue / budget units`.
- Volume: `(total actual units − total budget units) × Pbar` = +299,199.11.
- Mix (SKU and month composition): `SUM[(Qa − Qb) × (Pb − Pbar)]` = -14,149.31.
- Selling price: `SUM[Qa × (Pa − Pb)]` = -89,097.16.
- Total revenue change = +195,952.64, with **zero bridge residual before rounding**.

## Exact gross-profit and EBITDA bridge (USD)
Sequence at SKU-month level, where Q=units, P=selling unit price, C=unit COGS:
- Quantity effect at budget unit margin: `SUM[(Qa − Qb) × (Pb − Cb)]` = **+120,736.51**.
- Unit selling price effect at actual volume: `SUM[Qa × (Pa − Pb)]` = **−89,097.16**.
- Unit cost effect at actual volume: `−SUM[Qa × (Ca − Cb)]` = **−533,804.30**.
- Gross profit variance = **−502,164.95**, zero residual.
- OPEX impact = **−178,950.84**.
- EBITDA proxy variance = **−681,115.79**, zero residual.

**Important:** The gross-profit quantity effect does not distinguish aggregate volume from SKU/month mix. It differs intentionally from the revenue bridge total-volume effect.

## Gross profit by product category (USD; actual minus budget)
- Lifestyle Accessories: −162,198.17
- Office Supplies: −155,376.01
- Personal Care: −112,790.78
- Home Essentials: −71,799.99
- **Total: −502,164.95**

## Executive interpretation
Revenue exceeded budget, but modeled unit costs caused the largest headwind (−533.8k), and operating expenses reduced results by a further 179.0k. Gross margin fell approximately 5.01 percentage points. EBITDA proxy swung from +578.9k budgeted to −102.2k actual. These are **synthetic modeled effects**, not evidence of real inflation or supplier issues.

## Next investigations
1. Identify SKUs/months contributing most to the unit-cost effect.
2. Decompose OPEX variance by category.
3. Model price, cost and operating-expense improvements needed to recover EBITDA.
4. Verify formulas and report display in Excel before using screenshots externally.

**Provenance:** Synthetic dataset inspired only by retail transaction structure / broad seasonal concepts from Chen, D. (2012), *Online Retail II*, UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/502/online+retail+ii . No original transaction rows or empirical fitted coefficients included.
