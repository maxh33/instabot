import collections
import collections.abc
# Patch for Python 3.10+ compatibility (must run before GramAddict imports)
if not hasattr(collections, "Iterable"):
    collections.Iterable = collections.abc.Iterable
if not hasattr(collections, "Mapping"):
    collections.Mapping = collections.abc.Mapping
    
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
import datetime
import logging
from dotenv import load_dotenv

load_dotenv()

USERNAME = os.getenv("INSTAGRAM_USER_A")
PASSWORD = os.getenv("INSTAGRAM_PASS_A")
DEVICE = os.getenv("DEVICE_ID_A")

if not all([USERNAME, PASSWORD, DEVICE]):
    print("Error: missing INSTAGRAM_USER_A, INSTAGRAM_PASS_A or DEVICE_ID_A in .env")
    sys.exit(1)

# safer strategy: use Top posts for hashtag (Recent tab often unavailable)
config_strategy = {
    # Do NOT include 'username' here to avoid GramAddict attempting to
    # change accounts at startup (we're already logged into the emulator).
    "device": DEVICE,
    "total-sessions": 1,
    "hashtag-likers-top": ["python"],
    "likes-count": 1,
    "total-likes-limit": 1,
    "follow-percentage": 0,
}

os.makedirs(os.path.join("accounts", "temp"), exist_ok=True)
config_path = os.path.abspath(os.path.join("accounts", "temp", "test_like.yml"))

with open(config_path, "w", encoding="utf-8") as f:
    for key, value in config_strategy.items():
        if isinstance(value, list):
            f.write(f"{key}: [{', '.join(value)}]\n")
        else:
            f.write(f"{key}: {value}\n")

print(f"Wrote temporary config to {config_path}")
print("Checking ADB connection...")

# Setup simple logging for this runner
os.makedirs("logs", exist_ok=True)
log_file = os.path.join("logs", "gramaddict_run.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, encoding="utf-8"),
    ],
)
logging.info("Starting test_like_hashtag runner")


# quick ADB check
try:
    adb_proc = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
    devices_out = adb_proc.stdout + adb_proc.stderr
    if DEVICE not in devices_out:
        logging.warning(f"device '{DEVICE}' not listed by adb. adb output:\n{devices_out}")
        logging.warning("Make sure BlueStacks ADB is enabled and connected (adb connect 127.0.0.1:PORT).")
        # proceed anyway so user can see detailed GramAddict logs if they want
except FileNotFoundError:
    logging.error("adb not found in PATH. Ensure ADB is installed or BlueStacks ADB is enabled.")
    sys.exit(1)
except subprocess.CalledProcessError as exc:
    logging.error(f"adb returned non-zero exit: {exc}")
    # still proceed - write output
    try:
        logging.error(f"adb stdout: {exc.stdout}\nstderr: {exc.stderr}")
    except Exception:
        pass
    sys.exit(1)
except subprocess.CalledProcessError as exc:
    print(f"adb returned non-zero exit: {exc}")
    sys.exit(1)

print("Launching GramAddict (will open Instagram on the emulator/device)...")

# build env and locate gramaddict CLI in .venv
env = os.environ.copy()
project_root = os.path.dirname(os.path.abspath(__file__))
env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")

venv_scripts = os.path.join(project_root, ".venv", "Scripts")
gramaddict_exe = os.path.join(venv_scripts, "gramaddict.exe")
if not os.path.exists(gramaddict_exe):
    print(f"Error: gramaddict.exe not found at {gramaddict_exe}")
    print("Install GramAddict in the venv: .venv\\Scripts\\Activate then pip install gramaddict")
    sys.exit(1)

try:
    # Use global -v (verbose)
    cmd = [gramaddict_exe, "-v", "run", "--config", config_path]
    logging.info("Running: %s", " ".join(cmd))
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    # write combined output (stdout+stderr) already captured by FileHandler via logging
    try:
            with open(log_file, "a", encoding="utf-8") as lf:
                lf.write("\n--- GramAddict output: %s ---\n" % datetime.datetime.now(datetime.timezone.utc).isoformat())
            lf.write(proc.stdout or "")
    except Exception as e:
        logging.error("Failed to write gramaddict output to log file: %s", e)

    if proc.returncode == 0:
        logging.info("Test run finished successfully.")
    else:
        logging.error("GramAddict run failed with exit code %s", proc.returncode)
        # show last 30 lines for quick debugging
        if proc.stdout:
            tail = "\n".join(proc.stdout.splitlines()[-30:])
            logging.error("--- Last output lines ---\n%s", tail)
        sys.exit(proc.returncode)
except Exception as e:
    logging.exception("Unexpected error running GramAddict: %s", e)
    raise
