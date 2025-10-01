import requests
import pandas as pd
import numpy as np

BASE_URL = "http://127.0.0.1:8000"

# --- 1) Portfolioselection ---
print("=== Portfolioselection Test ===")
payload_selection = {
    "header": ["StockA", "StockB"],
    "data": [
        [0.05, 0.02],
        [0.03, 0.01],
        [0.04, 0.03]
    ],
    "zielrendite": 0.02,
    "is_returns": True
}
res = requests.post(f"{BASE_URL}/prediction/portfolioselection", json=payload_selection)
print("Status:", res.status_code)
print("Response:", res.json())


# --- 2) CAPM ---
print("\n=== CAPM Test ===")
dates = pd.date_range("2023-01-01", periods=3, freq="D").strftime("%Y-%m-%d").tolist()
payload_capm = {
    "header": ["StockA", "StockB"],
    "date": dates,
    "data": [
        [0.05, 0.02],
        [0.03, 0.01],
        [0.04, 0.03]
    ],
    "is_returns": True
}
res = requests.post(f"{BASE_URL}/prediction/capm", json=payload_capm)
print("Status:", res.status_code)
try:
    print("Response:", res.json())
except Exception:
    print("Raw Text:", res.text)


# --- 3) Brownian Motion ---
print("\n=== Brownian Motion Test ===")
dates = pd.date_range("2023-01-01", periods=50, freq="B").strftime("%Y-%m-%d").tolist()  # 50 Börsentage
data = np.random.rand(50, 2).tolist()  # 2 Aktien mit Zufallsdaten
payload_brownian = {
    "header": ["StockA", "StockB"],
    "date": dates,
    "data": data,
    "handelstage": 252,
    "haltedauer": 2.0
}
res = requests.post(f"{BASE_URL}/prediction/brownsche_bewegung", json=payload_brownian)
print("Status:", res.status_code)
try:
    print("Response:", res.json())
except Exception:
    print("Raw Text:", res.text)
