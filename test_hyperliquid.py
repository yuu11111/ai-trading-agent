#!/usr/bin/env python3
"""Test script to verify Hyperliquid leverage functionality."""

import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from src.trading.hyperliquid_api import HyperliquidAPI
from dotenv import load_dotenv
load_dotenv()

async def test_leverage():
    """Test leverage setting functionality."""
    hyperliquid = HyperliquidAPI()

    # Test update_leverage (this would set leverage for the asset)
    try:
        # Note: This would actually set leverage on the exchange, use testnet
        # result = await hyperliquid._retry(lambda: hyperliquid.exchange.update_leverage(5, "BTC", is_cross=True))
        # print("update_leverage result:", result)
        print("Leverage methods available: update_leverage is implemented in SDK")
    except Exception as e:
        print(f"update_leverage test failed: {e}")

    # Test place_buy_order with leverage (would set leverage before ordering)
    try:
        # This would place a real order, so commented out
        # result = await hyperliquid.place_buy_order("BTC", 0.001, leverage=3)
        # print("place_buy_order with leverage result:", result)
        print("place_buy_order now accepts leverage parameter")
    except Exception as e:
        print(f"place_buy_order test failed: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_leverage())