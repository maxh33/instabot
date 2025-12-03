import os
import sys
import subprocess
import datetime
import logging
import argparse
from dotenv import load_dotenv
from device_manager import DeviceManager, load_device_from_env

# Enhanced test runner for Instagram bot
# - Supports both USB (physical) and network (MEmu) devices
# - Writes `accounts/test_like_enhanced.yml`
# - Runs GramAddict with human-like behavior and debug logging
#
# Usage:
#   python test_like.py                           # Uses DEVICE from .env
#   python test_like.py --device fbc9d1f30eb2     # Specific USB device
#   python test_like.py --device 127.0.0.1:21533  # MEmu emulator
#   python test_like.py --account A               # Uses DEVICE_A from .env

load_dotenv()

ROOT = os.path.abspath(os.path.dirname(__file__))
os.chdir(ROOT)

# Parse command line arguments
parser = argparse.ArgumentParser(description="Run Instagram bot test session")
parser.add_argument("--device", help="Device ID (USB or network IP:port)", default=None)
parser.add_argument("--account", help="Account suffix for multi-account (_A, _B, etc.)", default="")
args = parser.parse_args()

# Configuration
CONFIG_PATH = os.path.join("accounts", "test_like_enhanced.yml")

# Load device ID: CLI arg > env var > default
if args.device:
    DEVICE = args.device
else:
    DEVICE = load_device_from_env(f"_{args.account}" if args.account else "")
    if not DEVICE:
        print("ERROR: No device specified. Set DEVICE in .env or use --device argument")
        print("Examples:")
        print("  python test_like.py --device fbc9d1f30eb2      # USB device")
        print("  python test_like.py --device 127.0.0.1:21533   # MEmu emulator")
        sys.exit(1)

# Build YAML content dynamically with enhanced human-like behavior
# Uses 15 personalized hashtags for backend/infrastructure niche
lines = [
    "# Enhanced test config - 3-8 minute session with faster, natural behavior",
    "# Personalized for backend/infrastructure niche",
    "debug: true",
    f"device: {DEVICE}",
    "allow-untested-ig-version: true",
    "",
    "# Mix of sources for variety (less robotic)",
    "# Hashtags: Top likers (Instagram v313 doesn't have Recent tab)",
    "hashtag-likers-top: [python, django, fastapi, backend, devops]",
    "# Competitor accounts: Post likers",
    "blogger-post-likers: [realpython, freecodecamp, thepracticaldev]",
    "",
    "# Session limits for ~3-8 minute test",
    "total-likes-limit: 8",
    "total-follows-limit: 3",
    "total-interactions-limit: 12",
    "total-successful-interactions-limit: 8",
    "",
    "# Human-like behavior (faster but natural)",
    "likes-count: 1-2",
    "likes-percentage: 50-70",
    "follow-percentage: 25-40",
    "stories-count: 0-1",
    "stories-percentage: 15-35",
    "watch-video-time: 3-15",
    "watch-photo-time: 1-3",
    "carousel-count: 0-2",
    "carousel-percentage: 30-60",
    "interact-percentage: 40-70",
    "speed-multiplier: 1.5",
    "",
    "# Behavior controls",
    "interactions-count: 3-5",
    "skipped-list-limit: 5-8",
]

# Prefer INSTAGRAM_USER_A / INSTAGRAM_PASS_A from .env, fall back to generic USERNAME/PASSWORD
# Do NOT write credentials into the temporary config automatically. Writing
# `username`/`password` keys here can be interpreted as unknown CLI args by
# configargparse in some versions. If you want to test with real credentials,
# add them to `accounts/test_like_safe.yml` manually or use your usual account
# config under `accounts/<username>/config.yml`.

YAML_CONTENT = "\n".join(lines) + "\n"

# Ensure accounts dir exists
os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
with open(CONFIG_PATH, "w", encoding="utf-8") as f:
    f.write(YAML_CONTENT)

# Setup logging
os.makedirs("logs", exist_ok=True)
log_file = os.path.join("logs", "gramaddict_test_like.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s | %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(log_file, encoding="utf-8"),
    ],
)
logging.info("Wrote safe config to %s", CONFIG_PATH)
# Log the config content with password masked for safety
def _mask_password(yaml_text: str) -> str:
    out_lines = []
    for line in yaml_text.splitlines():
        if line.strip().lower().startswith("password:"):
            out_lines.append("password: ****")
        else:
            out_lines.append(line)
    return "\n".join(out_lines)

masked = _mask_password(YAML_CONTENT)
logging.info("Config content:\n%s", masked)

# Check ADB and device connection (supports USB and network devices)
logging.info("Checking ADB connection...")

# Check if ADB is available
if not DeviceManager.check_adb_available():
    logging.error("adb not found in PATH. Ensure ADB is installed.")
    sys.exit(1)

# Create device manager and ensure connection
dm = DeviceManager(DEVICE)
logging.info(f"Device: {DEVICE} (type: {dm.device_type})")

if not dm.ensure_connected(logging):
    logging.error(f"Failed to connect to device {DEVICE}")

    # List available devices
    devices = DeviceManager.list_connected_devices()
    if devices:
        logging.info("Available devices:")
        for dev_id, dev_type in devices:
            logging.info(f"  - {dev_id} ({dev_type})")
    else:
        logging.info("No devices connected")

    sys.exit(1)

logging.info(f"[OK] Device {DEVICE} is ready")

# Locate GramAddict CLI in the local venv
gramaddict_exe = os.path.join(ROOT, ".venv", "Scripts", "gramaddict.exe")
if not os.path.exists(gramaddict_exe):
    logging.error("gramaddict CLI not found at %s. Activate .venv or adjust path.", gramaddict_exe)
    sys.exit(1)

# Ensure sitecustomize from project root is available to the subprocess
env = os.environ.copy()
env["PYTHONPATH"] = ROOT + os.pathsep + env.get("PYTHONPATH", "")
# Enable more verbose logging from GramAddict to help diagnose why it exits early
env.setdefault("GRAMADDICT_LOG_LEVEL", "DEBUG")
env.setdefault("GRAMADDICT_DEBUG", "1")
env.setdefault("PYTHONUNBUFFERED", "1")

# Use absolute config path and request debug via the proper flag
abs_config = os.path.abspath(CONFIG_PATH)
# NOTE: GramAddict's `-v` is the version flag. Use `--debug` to enable
# debug mode (and environment variables) instead of passing `-vv`.
cmd = [gramaddict_exe, "run", "--config", abs_config]
logging.info("Running: %s", " ".join(cmd))
# Capture help output to diagnose CLI flags
try:
    help_proc = subprocess.run([gramaddict_exe, "--help"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    with open(log_file, "a", encoding="utf-8") as lf:
        lf.write("\n--- gramaddict --help ---\n")
        lf.write(help_proc.stdout or "")
except Exception:
    logging.debug("Failed to capture 'gramaddict --help' output")

try:
    help_proc2 = subprocess.run([gramaddict_exe, "run", "--help"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
    with open(log_file, "a", encoding="utf-8") as lf:
        lf.write("\n--- gramaddict run --help ---\n")
        lf.write(help_proc2.stdout or "")
except Exception:
    logging.debug("Failed to capture 'gramaddict run --help' output")

proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)

# Append run output to log file with timestamp
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
    if proc.stdout:
        tail = "\n".join(proc.stdout.splitlines()[-60:])
        logging.error("--- Last output lines ---\n%s", tail)
    # If GramAddict produced a crash zip, mention it
    crashes_dir = os.path.join(ROOT, "crashes", "latest")
    if os.path.isdir(crashes_dir):
        logging.info("Crash artifacts (if any) available in: %s", crashes_dir)
    sys.exit(proc.returncode)

if __name__ == '__main__':
    pass
