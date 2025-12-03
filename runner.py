import argparse
import logging
import os
import subprocess
import sys
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

ROOT = os.path.abspath(os.path.dirname(__file__))
DEVICE = os.getenv("DEVICE", "127.0.0.1:5555")
USERNAME = os.getenv("INSTAGRAM_USER_A") or os.getenv("INSTAGRAM_USER")


def resolve_gramaddict_executable() -> Optional[str]:
    win_path = os.path.join(ROOT, ".venv", "Scripts", "gramaddict.exe")
    if os.path.exists(win_path):
        return win_path
    nix_path = os.path.join(ROOT, ".venv", "bin", "gramaddict")
    if os.path.exists(nix_path):
        return nix_path
    return None


def setup_logging(task_name: str) -> tuple[logging.Logger, str]:
    logs_dir = os.path.join(ROOT, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    log_path = os.path.join(logs_dir, f"gramaddict_{task_name}.log")

    logger = logging.getLogger("gramaddict_runner")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger, log_path


def check_adb(device: str, logger: logging.Logger) -> bool:
    try:
        result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        logger.error("ADB not installed or not in PATH.")
        return False
    except subprocess.CalledProcessError as exc:
        logger.error("ADB command failed: %s", exc)
        if exc.stdout:
            logger.error("adb stdout: %s", exc.stdout.strip())
        if exc.stderr:
            logger.error("adb stderr: %s", exc.stderr.strip())
        return False

    output = (result.stdout or "") + (result.stderr or "")
    if device not in output:
        logger.error("Device %s not found. adb output:\n%s", device, output.strip())
        logger.error("Ensure BlueStacks is running and ADB bridge is enabled.")
        return False

    logger.info("ADB reports device %s is connected.", device)
    return True


def stream_process_output(proc: subprocess.Popen, log_path: str) -> None:
    with open(log_path, "a", encoding="utf-8") as sink:
        for line in proc.stdout or []:
            sys.stdout.write(line)
            sys.stdout.flush()
            sink.write(line)
        sink.flush()


def run_gramaddict(config_path: str, task_name: str, logger: logging.Logger, log_path: str) -> int:
    executable = resolve_gramaddict_executable()
    if not executable:
        logger.error("GramAddict executable not found inside .venv.")
        return 1

    if not os.path.exists(config_path):
        logger.error("Config file not found: %s", config_path)
        return 1

    abs_config = os.path.abspath(config_path)

    cmd = [executable, "run", "--config", abs_config]

    if USERNAME:
        cmd.extend(["--username", USERNAME])
    else:
        logger.warning("INSTAGRAM_USER_A (or INSTAGRAM_USER) not set; relying on config username.")

    if DEVICE:
        cmd.extend(["--device", DEVICE])

    logger.info("Running command: %s", " ".join(cmd))

    env = os.environ.copy()
    existing_pythonpath = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = ROOT if not existing_pythonpath else ROOT + os.pathsep + existing_pythonpath
    env.setdefault("PYTHONUNBUFFERED", "1")
    env.setdefault("GRAMADDICT_LOG_LEVEL", "INFO")

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=env,
    )

    stream_process_output(proc, log_path)

    proc.wait()

    if proc.returncode == 0:
        logger.info("Task finished successfully.")
    else:
        logger.error("Task failed or stopped (exit code %s).", proc.returncode)

    return proc.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="GramAddict task runner")
    parser.add_argument("mode", choices=["growth", "cleanup", "morning", "lunch", "evening", "extra"], help="Select which strategy to run")
    args = parser.parse_args()

    config_map = {
        "growth": os.path.join(ROOT, "accounts", "strategy_growth.yml"),
        "cleanup": os.path.join(ROOT, "accounts", "strategy_cleanup.yml"),
        "morning": os.path.join(ROOT, "accounts", "session_morning.yml"),
        "lunch": os.path.join(ROOT, "accounts", "session_lunch.yml"),
        "evening": os.path.join(ROOT, "accounts", "session_evening.yml"),
        "extra": os.path.join(ROOT, "accounts", "session_extra.yml"),
    }

    config_path = config_map[args.mode]

    logger, log_path = setup_logging(args.mode)
    logger.info("Starting %s task with config %s", args.mode, config_path)

    filters_path = os.path.join(ROOT, "accounts", "filters.yml")
    if not os.path.exists(filters_path):
        logger.warning("filters.yml not found at %s; GramAddict will fall back to defaults.", filters_path)

    if not check_adb(DEVICE, logger):
        return 1

    return run_gramaddict(config_path, args.mode, logger, log_path)


if __name__ == "__main__":
    sys.exit(main())
