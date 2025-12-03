#!/usr/bin/env python3
"""
Advanced scheduler with daily randomization
Run this once per day (e.g., at midnight) to schedule that day's sessions
"""
import random
import subprocess
from datetime import datetime, timedelta
import os

PROJECT_DIR = "/path/to/instabot"  # CHANGE THIS
AT_COMMAND = "at"  # Linux 'at' command for one-time scheduling

def schedule_session(session_type, target_hour, target_minute, variance_minutes=30):
    """Schedule a single session with time randomization"""

    # Calculate random offset
    offset = random.randint(-variance_minutes, variance_minutes)
    actual_hour = target_hour
    actual_minute = target_minute + offset

    # Handle minute overflow/underflow
    if actual_minute < 0:
        actual_hour -= 1
        actual_minute += 60
    elif actual_minute >= 60:
        actual_hour += 1
        actual_minute -= 60

    # Validate hour range
    if actual_hour < 8 or actual_hour > 22:
        print(f"Skipping {session_type}: time out of range ({actual_hour}:{actual_minute})")
        return

    # Schedule using 'at' command
    time_str = f"{actual_hour:02d}:{actual_minute:02d}"
    command = f"cd {PROJECT_DIR} && ./scheduler.sh"

    try:
        proc = subprocess.Popen(
            [AT_COMMAND, time_str],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input=command)

        if proc.returncode == 0:
            print(f"✓ {session_type} session scheduled at {time_str}")
        else:
            print(f"✗ Failed to schedule {session_type}: {stderr}")

    except Exception as e:
        print(f"✗ Error scheduling {session_type}: {e}")

def main():
    print(f"=== Daily Session Scheduler - {datetime.now().strftime('%Y-%m-%d')} ===\n")

    # Decide number of sessions today (3-5)
    num_sessions = random.choice([3, 3, 3, 4, 4, 5])  # Weighted toward 3-4
    print(f"Sessions today: {num_sessions}\n")

    # Core sessions (always run)
    schedule_session("morning", 9, 30, variance_minutes=30)
    schedule_session("lunch", 12, 30, variance_minutes=30)
    schedule_session("evening", 18, 0, variance_minutes=30)

    # Extra sessions (for 4-5 session days)
    if num_sessions >= 4:
        extra_times = [(8, 0), (15, 0), (20, 0)]
        extra_session = random.choice(extra_times)
        schedule_session("extra", extra_session[0], extra_session[1], variance_minutes=45)

    if num_sessions == 5:
        # Pick a different extra time
        remaining_times = [t for t in [(8, 0), (15, 0), (20, 0)] if t != extra_session]
        extra_session_2 = random.choice(remaining_times)
        schedule_session("extra2", extra_session_2[0], extra_session_2[1], variance_minutes=45)

    print("\n=== Scheduling complete ===")

if __name__ == "__main__":
    main()
