import tempfile
import unittest
from pathlib import Path
import pandas as pd
from analysis import analyze, load_and_clean, summarize

class SalesTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.folder = Path(temp.name)

    def write_csv(self, records):
        path = self.folder / "sales.csv"
        pd.DataFrame(records).to_csv(path,index=False)
        return path

    def test_cleaning_and_revenue(self):
        path = self.write_csv([
            {"date":"2026-01-01","region":" East ","product":" Phone ","units_sold":"2","price":"100"},
            {"date":"bad","region":"West","product":"Laptop","units_sold":"3","price":"200"},
            {"date":"2026-01-02","region":"West","product":"Laptop","units_sold":"1","price":"-5"},
            {"date":"2026-01-03","region":"West","product":"Laptop","units_sold":"1","price":"50"},
        ])
        cleaned, rejected = load_and_clean(path)
        self.assertEqual(rejected,2)
        self.assertEqual(len(cleaned),2)
        self.assertAlmostEqual(summarize(cleaned)["total_revenue"],250)
        self.assertEqual(cleaned.iloc[0]["region"],"East")

    def test_missing_column_error(self):
        path = self.write_csv([{"date":"2026-01-01","region":"East"}])
        with self.assertRaisesRegex(ValueError,"Missing required columns"):
            load_and_clean(path)

    def test_output_files(self):
        path = self.write_csv([{"date":"2026-01-01","region":"East","product":"Phone","units_sold":2,"price":100}])
        summary, rejected = analyze(path, self.folder / "out")
        self.assertEqual(summary["total_revenue"],200)
        self.assertEqual(rejected,0)
        for name in ("cleaned_sales.csv","revenue_by_product.csv","revenue_by_region.csv","revenue_by_product.png"):
            self.assertTrue((self.folder / "out" / name).is_file())
