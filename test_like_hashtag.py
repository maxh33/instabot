#!/usr/bin/env python3
"""
Simple test launcher that creates a temporary GramAddict config to
search for `#python` and like the first post found (1 like). This is
meant for local testing with BlueStacks + ADB and the credentials in
`.env` (INSTAGRAM_USER_A, INSTAGRAM_PASS_A, DEVICE_ID_A).

Usage (from project root, with .venv activated):
  python test_like_hashtag.py

Notes:
- The script creates `accounts/temp/test_like.yml` and calls GramAddict's
  Bot.run(...) with that config. Adjust params as needed.
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("INSTAGRAM_USER_A")
PASSWORD = os.getenv("INSTAGRAM_PASS_A")
DEVICE = os.getenv("DEVICE_ID_A")

if not all([USERNAME, PASSWORD, DEVICE]):
    print("Error: missing INSTAGRAM_USER_A, INSTAGRAM_PASS_A or DEVICE_ID_A in .env")
    sys.exit(1)

# Minimal config: small time limit, like only one post from hashtag 'python'
# Note: GramAddict uses FLAT config format (no 'jobs:' wrapper)
config = {
    "username": USERNAME,
    "device": DEVICE,                       # ADB device ID
    "time-limit": 2,                        # minutes (short test)
    "hashtag-likers-recent": ["python"],    # interact with #python likers
    "likes-count": 1,
    "total-likes-limit": 1,
    "follow-percentage": 0
}

os.makedirs(os.path.join("accounts", "temp"), exist_ok=True)
config_path = os.path.abspath(os.path.join("accounts", "temp", "test_like.yml"))

with open(config_path, "w", encoding="utf-8") as f:
    # Write YAML config matching EXACT official format from GramAddict repo
    # Note: spaces inside brackets are important! [ item1, item2 ] not [item1,item2]
    f.write(f"username: {USERNAME}\n")
    f.write(f"device: {DEVICE}\n")
    f.write(f"hashtag-likers-recent: [ python ]\n")  # EXACT official format with spaces
    f.write(f"likes-count: 1\n")
    f.write(f"total-likes-limit: 1\n")
    f.write(f"follow-percentage: 0\n")
    f.write(f"total-interactions-limit: 1\n")
    f.write(f"allow-untested-ig-version: true\n")

print(f"Wrote temporary config to {config_path}")
print("Launching GramAddict (this will open Instagram on the emulator/device)...")

try:
    # Call GramAddict using the venv's gramaddict.exe directly to avoid global conflicts
    env = os.environ.copy()
    project_root = os.path.dirname(os.path.abspath(__file__))
    env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")

    # Get venv's Scripts directory - look for .venv in project root
    # sys.executable might point to base Python, so we find venv manually
    venv_scripts = os.path.join(project_root, ".venv", "Scripts")
    gramaddict_exe = os.path.join(venv_scripts, "gramaddict.exe")

    if not os.path.exists(gramaddict_exe):
        print(f"Error: gramaddict.exe not found at {gramaddict_exe}")
        print("Make sure GramAddict is installed in your active venv: pip install gramaddict")
        sys.exit(1)

    # Use simple config file approach (CLI args caused parser errors)
    result = subprocess.run(
        [gramaddict_exe, "run", "--config", config_path],
        check=True,
        capture_output=False,
        env=env
    )
    print("\nTest run finished successfully.")
except subprocess.CalledProcessError as exc:
    print(f"\nGramAddict run failed with exit code {exc.returncode}")
    sys.exit(exc.returncode)
