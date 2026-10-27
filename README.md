# Sales & Customer Data Analyzer

A reproducible Python, Pandas and Matplotlib learning project. It cleans a small sample sales CSV, calculates revenue by product and region, and saves analysis outputs to files.

## Quick start

Requires Python 3.10+.

    python -m pip install -r requirements.txt
    python analysis.py --input data/sales_data.csv --output output

Outputs in the selected directory:
- cleaned_sales.csv
- revenue_by_product.csv
- revenue_by_region.csv
- revenue_by_product.png

## Input and data cleaning

Required columns: date, region, product, units_sold and price.

The pipeline trims region and product labels, parses dates and numbers, and excludes rows with missing/invalid fields or negative units/prices. It counts rejected rows and keeps the original CSV unchanged. Valid repeated records remain because the data has no transaction ID.

Revenue is computed as units_sold multiplied by price. The source currency is not specified.

**Dataset limitation:** The included CSV has only 10 illustrative rows, not real business data. Don't infer actual company trends or market outcomes from this sample.

## Architecture

1. load_and_clean: validates and parses the source CSV.
2. summarize: computes total and grouped revenue.
3. analyze: saves reusable CSV reports and a PNG chart.
4. main: command-line entrypoint with configurable paths.

## Tests

    python -m unittest discover -s tests -v

Tests cover dirty data, missing columns and generated output files.

## Next steps

Improve the project with a more realistic dataset, unique transaction IDs, time-series analysis, refunds, currency metadata and interactive dashboards.
