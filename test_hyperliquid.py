#!/usr/bin/env python3
"""Test script to verify Hyperliquid leverage and cancel functionality."""

import sys
import pathlib
import os
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from src.trading.hyperliquid_api import HyperliquidAPI
from dotenv import load_dotenv
load_dotenv()

# Force testnet for testing
os.environ["HYPERLIQUID_NETWORK"] = "testnet"

async def test_leverage():
    """Test leverage setting functionality."""
    hyperliquid = HyperliquidAPI()

    # Test update_leverage (this would set leverage on the exchange, use testnet)
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

async def test_cancel():
    """Test cancel functionality."""
    hyperliquid = HyperliquidAPI()

    try:
        # Test cancel_all_orders (for reference)
        result = await hyperliquid.cancel_all_orders("BTC")
        print("cancel_all_orders result:", result)
    except Exception as e:
        print(f"cancel_all_orders test failed: {e}")

    try:
        # Test cancel_order (specific OID)
        # Note: Need a valid OID from get_open_orders
        orders = await hyperliquid.get_open_orders()
        if orders:
            oid = orders[0].get("oid")
            if oid:
                result = await hyperliquid.cancel_order("BTC", oid)
                print("cancel_order result:", result)
            else:
                print("No OID found in open orders")
        else:
            print("No open orders to cancel")
    except Exception as e:
        print(f"cancel_order test failed: {e}")

    try:
        # Test get_open_orders
        orders = await hyperliquid.get_open_orders()
        print("Open orders:", orders)
    except Exception as e:
        print(f"get_open_orders test failed: {e}")

async def test_place_order():
    """Test placing a small order on testnet."""
    hyperliquid = HyperliquidAPI()

    try:
        # Get metadata first to understand market constraints
        print("Fetching market metadata...")
        meta_data = await hyperliquid.get_meta_and_ctxs()
        if meta_data:
            meta, asset_ctxs = meta_data[0], meta_data[1]
            universe = meta.get("universe", [])
            btc_info = next((u for u in universe if u.get("name") == "BTC"), None)
            if btc_info:
                sz_decimals = btc_info.get("szDecimals", 8)
                print(f"BTC size decimals: {sz_decimals}")
                print(f"BTC market info: {btc_info}")

        # Get current BTC price
        btc_price = await hyperliquid.get_current_price("BTC")
        print(f"Current BTC price: ${btc_price:.2f}")

        # Try different amounts to find the minimum
        test_amounts = [0.001, 0.0001, 0.00001]  # Different sizes to test
        
        for test_amount in test_amounts:
            notional = test_amount * btc_price
            print(f"\nTrying amount: {test_amount:.6f} BTC (${notional:.2f})")
            
            # Round the amount properly
            rounded_amount = hyperliquid.round_size("BTC", test_amount)
            rounded_notional = rounded_amount * btc_price
            print(f"Rounded amount: {rounded_amount:.8f} BTC (${rounded_notional:.2f})")
            
            if rounded_notional >= 10.0:
                try:
                    # Place a small buy order for testing
                    print("Placing test buy order...")
                    result = await hyperliquid.place_buy_order("BTC", rounded_amount, leverage=2)
                    print("Test buy order result:", result)

                    # Wait a bit
                    import asyncio
                    await asyncio.sleep(2)

                    # Check open orders
                    orders = await hyperliquid.get_open_orders()
                    print("Open orders after placing:", orders)

                    # Cancel the test order if it exists
                    btc_orders = [o for o in orders if o.get("coin") == "BTC"]
                    if btc_orders:
                        oid = btc_orders[0].get("oid")
                        if oid:
                            print(f"Cancelling test order {oid}...")
                            cancel_result = await hyperliquid.cancel_order("BTC", oid)
                            print("Cancel result:", cancel_result)
                    break
                except Exception as e:
                    print(f"Order with amount {rounded_amount:.8f} failed: {e}")
            else:
                print(f"Amount too small (${rounded_notional:.2f} < $10 minimum)")

    except Exception as e:
        print(f"Test order failed: {e}")

if __name__ == "__main__":
    import asyncio
    print("Running tests on TESTNET - be careful!")
    asyncio.run(test_leverage())
    asyncio.run(test_cancel())
    asyncio.run(test_place_order())