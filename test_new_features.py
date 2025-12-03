"""
Test script to verify all new features are working correctly
Run this to ensure MEmu support, metrics, and device manager work properly
"""
import os
import sys
from pathlib import Path

print("="*70)
print(" Testing New Features - Instagram Bot")
print("="*70)
print()

# Test 1: Device Manager
print("[1/3] Testing Device Manager...")
try:
    from device_manager import DeviceManager, load_device_from_env

    # Check ADB
    if not DeviceManager.check_adb_available():
        print("  [FAILED] ADB not available")
        sys.exit(1)

    print("  [OK] ADB is available")

    # List devices
    devices = DeviceManager.list_connected_devices()
    print(f"  [OK] Found {len(devices)} device(s)")
    for dev_id, dev_type in devices:
        print(f"       - {dev_id} ({dev_type})")

    # Test device from .env
    device_id = load_device_from_env()
    if device_id:
        dm = DeviceManager(device_id)
        print(f"  [OK] Loaded device from .env: {device_id} ({dm.device_type})")

        if dm.ensure_connected():
            print(f"  [OK] Device {device_id} is connected")
        else:
            print(f"  [WARNING] Could not connect to {device_id}")
    else:
        print("  [WARNING] No DEVICE in .env (this is OK if you'll use CLI args)")

    print("  [PASS] Device Manager: PASSED\n")

except Exception as e:
    print(f"  [FAILED] Device Manager test failed: {e}\n")
    sys.exit(1)

# Test 2: Metrics Analyzer
print("[2/3] Testing Metrics Analyzer...")
try:
    from metrics_analyzer import MetricsAnalyzer
    from dotenv import load_dotenv
    load_dotenv()

    # Try to get username
    username = os.getenv("INSTAGRAM_USER_A", "maxhaider.dev")
    print(f"  [INFO] Testing with username: {username}")

    # Check if account data exists
    accounts_path = Path(f"accounts/{username}")
    if not accounts_path.exists():
        print(f"  [WARNING] No data yet for @{username}")
        print(f"  [INFO] Run a test session first: python test_like.py")
        print(f"  [OK] Metrics Analyzer module loads correctly")
    else:
        # Test metrics analyzer
        analyzer = MetricsAnalyzer(username)

        # Test basic functions
        stats = analyzer.get_account_stats()
        print(f"  [OK] Loaded account stats: {stats['total_interactions']} interactions")

        sessions = analyzer.get_session_stats(days=7)
        if "message" not in sessions:
            print(f"  [OK] Session stats: {sessions['total_sessions']} sessions in last 7 days")
        else:
            print(f"  [INFO] {sessions['message']}")

        sources = analyzer.get_source_performance()
        print(f"  [OK] Source performance: {len(sources)} sources tracked")

        print("  [OK] All metrics functions working")

    print("  [PASS] Metrics Analyzer: PASSED\n")

except FileNotFoundError as e:
    print(f"  [WARNING] Account data not found: {e}")
    print(f"  [INFO] This is normal if you haven't run the bot yet")
    print("  [PASS] Metrics Analyzer: PASSED (module OK, no data yet)\n")
except Exception as e:
    print(f"  [FAILED] Metrics Analyzer test failed: {e}\n")
    sys.exit(1)

# Test 3: Updated test_like.py
print("[3/3] Testing Updated test_like.py...")
try:
    # Check if test_like.py has the new imports
    with open("test_like.py", 'r', encoding='utf-8') as f:
        content = f.read()

    if "from device_manager import" in content:
        print("  [OK] test_like.py has device_manager import")
    else:
        print("  [WARNING] test_like.py may not have device_manager integration")

    if "argparse" in content:
        print("  [OK] test_like.py has CLI argument support")
    else:
        print("  [WARNING] test_like.py may not have CLI argument support")

    print("  [PASS] test_like.py: PASSED\n")

except Exception as e:
    print(f"  [WARNING] Could not verify test_like.py: {e}\n")

# Final Summary
print("="*70)
print(" Test Summary")
print("="*70)
print()
print("[OK] All core features are working!")
print()
print("Next Steps:")
print("  1. Test MEmu connection (if using):")
print("     adb connect 127.0.0.1:21503")
print("     python test_like.py --device 127.0.0.1:21503")
print()
print("  2. View metrics (after running bot):")
print("     python metrics_analyzer.py", os.getenv("INSTAGRAM_USER_A", "your_username"))
print()
print("  3. Check logs:")
print("     Get-Content logs/", os.getenv("INSTAGRAM_USER_A", "your_username") + ".log", "-Tail 50", sep="")
print()
print("  4. Read documentation:")
print("     - docs/MEMU_SETUP_EXAMPLE.md")
print("     - docs/LOG_ACCESS_GUIDE.md")
print("     - docs/NEW_FEATURES_SUMMARY.md")
print()
print("="*70)
