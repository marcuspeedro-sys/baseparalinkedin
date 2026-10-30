# Atlas Consumer Goods | FP&A Data Pack v1.0

**Status:** 100% synthetic portfolio case; Atlas Consumer Goods does not exist. No employer data and no original UCI transaction records are included.

## Contents
- `Atlas_Consumer_Goods_FP&A_Dataset_v1.xlsx`: Excel workbook containing README, Products, Sales_Data, OPEX_Data, Monthly_PnL, Executive_Summary, Assumptions and Data_Dictionary.
- `atlas_products.csv`: product master (20 fictional SKUs).
- `atlas_sales_monthly.csv`: 240 month-by-SKU records for FY2025 (budget and actual).
- `atlas_opex_monthly.csv`: 72 month-by-expense-category records (budget and actual).
- `build_atlas.py`: fully reproducible generator. Requires `artifact_tool`; CSV generation uses Python standard library.

## Data model
- `Revenue = quantity × selling price` (budget and actual separately)
- `COGS = quantity × unit cost`
- `Gross profit = revenue − COGS`
- `EBITDA (proxy) = gross profit − operating expenses` (no separate D&A, tax or financing flows)
- `Variance = actual − budget` for source categories. Positive expenses are unfavorable.

## Provenance and appropriate attribution
Reference for retail transactional **structure and broad seasonal concepts only**: Chen, D. (2012). *Online Retail II*. UCI Machine Learning Repository. https://archive.ics.uci.edu/dataset/502/online+retail+ii ; DOI: https://doi.org/10.24432/C5CG6D (CC BY 4.0 for original dataset). **No UCI records or estimated statistical parameters were imported**, and the values here are not empirical replicas. Products, periods, costs, price responses, and seasonality coefficients were constructed for a teaching example.

## Usage and integrity
Use as fictional case data for financial analysis, educational LinkedIn posts, dashboards and project demonstrations. Preserve the synthetic-data disclosure when sharing conclusions; do not attribute the generated revenue or costs to a real company. Financial records are keyed by `Month` and `SKU`; expenses by `Month` and `Expense Category`.

The Excel workbook contains formula-driven P&L and consistency checks. The included deterministic generator uses random seed `20261029` so the dataset can be regenerated.
