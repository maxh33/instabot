import os
import sys
import subprocess
import datetime
import logging
from dotenv import load_dotenv

# Safe, committed test runner for a single like from #python
# - Writes `accounts/test_like_safe.yml`
# - Runs the GramAddict CLI with verbose output and logs to `logs/gramaddict_test_like.log`

load_dotenv()

ROOT = os.path.abspath(os.path.dirname(__file__))
os.chdir(ROOT)

CONFIG_PATH = os.path.join("accounts", "test_like_safe.yml")
DEVICE = os.getenv("DEVICE", "127.0.0.1:21503")

# Build YAML content dynamically so we can inject credentials from .env when available.
lines = [
    "# Safe like-only config (committed)",
    "# - Small limits for testing",
    "# - If credentials exist in .env, they will be injected here for this run",
    "# - follow-percentage set to 0 to avoid following",
    "debug: true",
    f"device: {DEVICE}",
    "total-sessions: 1",
    "hashtag-likers-top: [python]",
    "likes-count: 1",
    "total-likes-limit: 1",
    "follow-percentage: 0",
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

# Check adb
logging.info("Checking ADB connection...")
try:
    adb_proc = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
    devices_out = (adb_proc.stdout or "") + (adb_proc.stderr or "")
    if DEVICE not in devices_out:
        logging.warning("Device '%s' not listed by adb. adb output:\n%s", DEVICE, devices_out)
        logging.warning("Make sure BlueStacks ADB is enabled and connected (adb connect 127.0.0.1:PORT).")
except FileNotFoundError:
    logging.error("adb not found in PATH. Ensure ADB is installed or BlueStacks ADB is enabled.")
    sys.exit(1)
except subprocess.CalledProcessError as exc:
    logging.error("adb returned non-zero exit: %s", exc)
    try:
        logging.error("adb stdout: %s\nstderr: %s", exc.stdout, exc.stderr)
    except Exception:
        pass
    sys.exit(1)

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
