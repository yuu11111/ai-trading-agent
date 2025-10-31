#!/usr/bin/env python3
"""Test script to verify TAAPI indicator fetching."""

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from src.indicators.taapi_client import TAAPIClient
from dotenv import load_dotenv
load_dotenv()

def test_taapi():
    """Test TAAPI client with sample indicators."""
    taapi = TAAPIClient()

    # Test get_indicators (newly added ATR/OBV/MFI/volume)
    try:
        indicators = taapi.get_indicators("BTC", "5m")
        print("get_indicators result:")
        for key, value in indicators.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"get_indicators failed: {e}")

    # Test fetch_series for historical data
    try:
        ema_series = taapi.fetch_series("ema", "BTC/USDT", "5m", results=5, params={"period": 20})
        print(f"\nfetch_series ema (last 5): {ema_series}")
    except Exception as e:
        print(f"fetch_series ema failed: {e}")

    # Test fetch_value for single value
    try:
        rsi_value = taapi.fetch_value("rsi", "BTC/USDT", "5m", params={"period": 14})
        print(f"\nfetch_value rsi: {rsi_value}")
    except Exception as e:
        print(f"fetch_value rsi failed: {e}")

if __name__ == "__main__":
    test_taapi()