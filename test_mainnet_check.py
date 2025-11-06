#!/usr/bin/env python3
"""Check mainnet readiness and constraints without placing orders."""

import sys
import pathlib
import os
sys.path.append(str(pathlib.Path(__file__).parent.parent))

from src.trading.hyperliquid_api import HyperliquidAPI
from dotenv import load_dotenv
load_dotenv()

# Set to mainnet for checking
os.environ["HYPERLIQUID_NETWORK"] = "mainnet"

async def check_mainnet_readiness():
    """Check mainnet API connectivity and constraints."""
    hyperliquid = HyperliquidAPI()
    
    print("=== MAINNET READINESS CHECK ===")
    print(f"Network: {hyperliquid.base_url}")
    
    try:
        # Check basic connectivity
        print("\n1. Checking API connectivity...")
        btc_price = await hyperliquid.get_current_price("BTC")
        print(f"✅ BTC price: ${btc_price:.2f}")
        
        # Check metadata
        print("\n2. Checking market metadata...")
        meta_data = await hyperliquid.get_meta_and_ctxs()
        if meta_data:
            meta, asset_ctxs = meta_data[0], meta_data[1]
            universe = meta.get("universe", [])
            btc_info = next((u for u in universe if u.get("name") == "BTC"), None)
            if btc_info:
                print(f"✅ BTC metadata: {btc_info}")
            else:
                print("❌ BTC metadata not found")
        
        # Check account state
        print("\n3. Checking account state...")
        user_state = await hyperliquid.get_user_state()
        balance = user_state.get("balance", 0)
        total_value = user_state.get("total_value", 0)
        print(f"✅ Account balance: ${balance:.2f}")
        print(f"✅ Total account value: ${total_value:.2f}")
        
        # Check open orders
        print("\n4. Checking open orders...")
        orders = await hyperliquid.get_open_orders()
        print(f"✅ Open orders: {len(orders)} orders")
        
        # Check minimum order size calculation
        print("\n5. Checking order size calculations...")
        test_amounts = [0.001, 0.0001, 0.00001]
        for amount in test_amounts:
            rounded = hyperliquid.round_size("BTC", amount)
            notional = rounded * btc_price
            status = "✅" if notional >= 10.0 else "❌"
            print(f"{status} {amount:.6f} BTC → {rounded:.8f} BTC (${notional:.2f})")
        
        # Risk checks
        print("\n6. Risk assessment...")
        if balance < 50:
            print("⚠️  Low balance - consider funding account")
        else:
            print(f"✅ Sufficient balance for trading")
            
        if total_value < 100:
            print("⚠️  Small account size - be cautious with position sizing")
        else:
            print(f"✅ Account size suitable for trading")
            
        print("\n=== MAINNET STATUS: READY ===")
        
    except Exception as e:
        print(f"\n❌ MAINNET CHECK FAILED: {e}")
        print("Check your credentials and network connectivity")

if __name__ == "__main__":
    import asyncio
    asyncio.run(check_mainnet_readiness())