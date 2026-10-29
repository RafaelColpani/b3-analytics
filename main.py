
# Libraries
from pathlib import Path

import yfinance as yf

# Project settings
TICKERS = ["PETR4.SA", "VALE3.SA"]
PERIOD = "1y"

# Project directory
PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Download historical quotes
print(f"Searching for data from {', '.join(TICKERS)}...")

data = yf.download(
    tickers=TICKERS,
    period=PERIOD,
    interval="1d",
    auto_adjust=True,
    progress=False
)

if data.empty:
    raise RuntimeError(
        "No data was returned. Check your internet connection "
        "and ticker symbols."
    )

# Extract adjusted closing prices
prices = data["Close"].copy()

# Use shorter column names
prices = prices.rename(columns={
    "PETR4.SA": "PETR4",
    "VALE3.SA": "VALE3"
})

# Remove timezone information
prices.index = prices.index.tz_localize(None)
prices.index.name = "Date"

# Sort by date
prices = prices.sort_index()

# Save data to Excel
excel_path = OUTPUT_DIR / "vale3_hist.xlsx"

with __import__("pandas").ExcelWriter(
    excel_path,
    engine="xlsxwriter",
    datetime_format="yyyy-mm-dd"
) as writer:
    prices.to_excel(writer, sheet_name="Prices")

# Terminal logs
print(f"Data collected: {len(prices)} records")
print(f"File saved to: {excel_path}")
print("\nLatest quotes:")
print(prices.tail())
