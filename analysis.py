"""Clean, summarize and visualize sales records with Pandas."""
import argparse
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

REQUIRED = {"date", "region", "product", "units_sold", "price"}

def load_and_clean(path):
    raw = pd.read_csv(path)
    missing = REQUIRED - set(raw.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")
    df = raw.copy()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    for field in ("units_sold", "price"):
        df[field] = pd.to_numeric(df[field], errors="coerce")
    for field in ("region", "product"):
        df[field] = df[field].astype("string").str.strip()
    cleaned = df.dropna(subset=list(REQUIRED))
    cleaned = cleaned.loc[(cleaned["region"] != "") & (cleaned["product"] != "")]
    cleaned = cleaned.loc[(cleaned["units_sold"] >= 0) & (cleaned["price"] >= 0)].copy()
    cleaned["revenue"] = cleaned["units_sold"] * cleaned["price"]
    return cleaned, len(raw) - len(cleaned)

def summarize(df):
    by_product = df.groupby("product", as_index=False, sort=True)["revenue"].sum().sort_values("revenue", ascending=False)
    by_region = df.groupby("region", as_index=False, sort=True)["revenue"].sum().sort_values("revenue", ascending=False)
    return {"total_revenue": float(df["revenue"].sum()), "records": len(df),
            "by_product": by_product, "by_region": by_region}

def analyze(source, output):
    clean, rejected = load_and_clean(source)
    if clean.empty:
        raise ValueError("No valid rows remain after cleaning")
    summary = summarize(clean)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    clean.to_csv(output / "cleaned_sales.csv", index=False)
    summary["by_product"].to_csv(output / "revenue_by_product.csv", index=False)
    summary["by_region"].to_csv(output / "revenue_by_region.csv", index=False)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(summary["by_product"]["product"], summary["by_product"]["revenue"])
    ax.set(title="Revenue by product", xlabel="Product", ylabel="Revenue (source currency)")
    fig.tight_layout()
    fig.savefig(output / "revenue_by_product.png", dpi=150)
    plt.close(fig)
    return summary, rejected

def main():
    parser = argparse.ArgumentParser(description="Clean and summarize a sales dataset")
    parser.add_argument("--input", default="data/sales_data.csv")
    parser.add_argument("--output", default="output")
    args = parser.parse_args()
    result, rejected = analyze(args.input, args.output)
    print(f"Valid records: {result['records']}; rejected records: {rejected}")
    print(f"Total revenue (source currency): {result['total_revenue']:.2f}")
    print(f"Saved chart and summaries in: {args.output}")

if __name__ == "__main__":
    main()
