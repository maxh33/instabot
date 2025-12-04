#!/usr/bin/env python3
"""
Dismiss Instagram banners/notifications that break GramAddict.
Run this before running the bot if you see crashes.
"""

import os
import subprocess
import sys
from dotenv import load_dotenv

load_dotenv(override=True)

DEVICE = os.getenv("DEVICE", "127.0.0.1:5555")


def run_adb_command(cmd: list[str]) -> str:
    """Run ADB command and return output."""
    result = subprocess.run(
        ["adb", "-s", DEVICE] + cmd,
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout + result.stderr


def tap_coordinates(x: int, y: int):
    """Tap at specific screen coordinates."""
    print(f"Tapping at ({x}, {y})...")
    run_adb_command(["shell", "input", "tap", str(x), str(y)])


def dismiss_professional_dashboard():
    """Dismiss the 'Professional dashboard' banner by tapping the dismiss button."""
    print("Opening Instagram...")
    run_adb_command(["shell", "am", "start", "-n", "com.instagram.android/com.instagram.mainactivity.MainActivity"])

    # Wait for Instagram to load
    subprocess.run(["python", "-c", "import time; time.sleep(3)"], check=True)

    # Navigate to profile (bottom right corner)
    print("Navigating to profile...")
    tap_coordinates(736, 1420)  # Profile tab at bottom right (adjusted for 1080x1920)

    subprocess.run(["python", "-c", "import time; time.sleep(2)"], check=True)

    # Look for the professional dashboard banner dismiss button (blue dot on the right)
    # From hierarchy: blue dot at approximately bounds="[744,564]" (right side of banner)
    print("Dismissing Professional dashboard banner...")
    tap_coordinates(750, 460)  # Tap the blue dismiss dot

    subprocess.run(["python", "-c", "import time; time.sleep(1)"], check=True)

    print("✓ Banner dismissed! You can now run the bot.")


def main():
    print(f"Target device: {DEVICE}")
    print("=" * 50)

    # Check ADB connection
    result = run_adb_command(["devices"])
    if DEVICE not in result:
        print(f"ERROR: Device {DEVICE} not connected!")
        print("Run 'adb devices' to check connection.")
        return 1

    dismiss_professional_dashboard()
    return 0


if __name__ == "__main__":
    sys.exit(main())
