# Atlas Consumer Goods | FP&A Data Pack v1.0

**Independent, 100% synthetic FP&A portfolio case.** Atlas Consumer Goods is fictional. This project does not contain employer data, confidential financial information, or original UCI transaction records.

## Project goal
Investigate why a fictional retail distributor can outperform its revenue budget but miss profitability targets. The case supports budget-to-actual variance analysis, price-volume-mix analysis, cost management, management reporting, and scenario planning.

## Dataset files
- `Atlas_Consumer_Goods_FP&A_Dataset_v1.xlsx` — Excel workbook: README, Products, Sales_Data, OPEX_Data, Monthly_PnL, Executive_Summary, Assumptions, Data_Dictionary.
- `atlas_products.csv` — 20 fictional SKUs.
- `atlas_sales_monthly.csv` — 240 month-by-SKU budget/actual records for FY2025.
- `atlas_opex_monthly.csv` — 72 monthly expense-category records.
- `build_atlas.py` — reproducible local data generator (seed `20261029`).

**Upload status:** The dataset files above are pending upload. Only this documentation has been committed so far; do not treat the repository as a complete dataset until all files appear.

## Financial model
- Revenue = quantity × selling price
- COGS = quantity × unit cost
- Gross profit = revenue − COGS
- EBITDA proxy = gross profit − operating expenses (D&A, interest and taxes are not separately modeled)
- Variance = actual − budget; positive expense variances are unfavorable

## Data provenance
Inspired only by the **transactional structure and broad seasonal concepts** of Chen, D. (2012), *Online Retail II*, UCI Machine Learning Repository: https://archive.ics.uci.edu/dataset/502/online+retail+ii (https://doi.org/10.24432/C5CG6D). No UCI original records or statistically fitted parameters were imported.

All SKUs, prices, quantities, costs, operating expenses, and seasonality coefficients were generated for demonstration. The project is not an empirical account of any real business.

## Responsible reuse
This repository is intended for portfolio demonstrations, dashboards, financial analysis, and educational LinkedIn content in Portuguese and English. Always disclose that the figures are simulated.

## Reproducibility
The generator uses fixed random seed `20261029`. CSV creation uses Python's standard library; workbook generation requires `artifact_tool`.
