#Libs
import yfinance as yf
from pathlib import Path

# Project settings "yfinance"
TICKER = "PETR4.SA"
PERIOD = "1y"

# Folder where the project is located
PROJECT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_DIR / "data"
OUTPUT_DIR.mkdir(exist_ok=True)

# Download historical quotes
print(f"Searching for data from {TICKER}...")

action = yf.Ticker(TICKER)
data = action.history(period=PERIOD, auto_adjust=True)

if data.empty:
    raise RuntimeError(
        "No data was returned. Check your internet connection "
        "and the action code."
    )

# Remove time zone information from the index
data.index = data.index.tz_localize(None)

# Save the data in Excel
arq_excel = OUTPUT_DIR / "petr4_hist.xlsx"
data.to_excel(arq_excel, engine="xlsxwriter")

# Terminal Logs
print(f"Data collected: {len(data)} records")
print(f"File saved to: {arq_excel}")
print("\nLatest quotes:")
print(data[["Close", "Volume"]].tail())
