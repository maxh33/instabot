Here is the complete plan, setup guide, and strategy for your Instagram growth script using GramAddict and BlueStacks. 🚀

# Instagram Growth Strategy with GramAddict (The Human-Like Bot)

This document outlines the setup, secure authentication, and execution plan for your automated Instagram growth script, prioritizing human behavior simulation and safety.

## 🛠️ Phase 1: Environment Setup & Connection

1. Prerequisite Checklist

- Python: Installed (v3.8+ recommended).
- BlueStacks: Installed, configured with the Instagram app, and logged in manually on each instance.
- ADB (Android Debug Bridge): Included with BlueStacks, but ensure it's available in your system path.
- Terminal/Command Prompt: Ready for execution.

2. Connect BlueStacks to ADB

You need to enable remote control for your Python script.

- BlueStacks Settings: In each BlueStacks instance, go to Settings $\rightarrow$ Advanced and ensure Android Debug Bridge is ON. Note the port (e.g., 5555, 5565).
- Verify Connection: Open your terminal and connect to your instance(s) using their respective ports.

```bash
adb connect 127.0.0.1:5555
adb devices
# Output should list your device(s), e.g., '127.0.0.1:5555 device'
```

3. Project Installation

```bash
# Create project folder and virtual environment
mkdir instagram-grow-bot
cd instagram-grow-bot
python3 -m venv venv
source venv/bin/activate

# Install required Python packages
pip install gramaddict python-dotenv

# Initialize GramAddict configuration files
gramaddict init your_username_A
# Repeat for other accounts: gramaddict init your_username_B
```

## 🔒 Phase 2: Secure Authentication & Launch Script

We're using a custom Python launcher to load credentials securely from an environment file (`.env`), bypassing hardcoded passwords in configuration files.

1. Create the .env File (The Secret Vault)

Create a file named `.env` in the project root. Add this file to your `.gitignore` immediately.

```ini
# .env
INSTAGRAM_USER_A=account_A_username
INSTAGRAM_PASS_A=secure_password_A
DEVICE_ID_A=127.0.0.1:5555

INSTAGRAM_USER_B=account_B_username
INSTAGRAM_PASS_B=secure_password_B
DEVICE_ID_B=127.0.0.1:5565
```

2. Create the Secure Launcher (`launch.py`)

This script handles loading credentials and launching GramAddict, targeting a specific BlueStacks instance.

```python
import os
import sys
from dotenv import load_dotenv
from GramAddict.core.bot import Bot

# Load environment variables from .env
load_dotenv()

def run_bot(user_key, pass_key, device_key, config_file):
    username = os.getenv(user_key)
    password = os.getenv(pass_key)
    device = os.getenv(device_key)

    if not all([username, password, device]):
        print(f"Error: Missing credentials or device ID for {user_key} in .env.")
        return

    # Configuration dictionary to override any hardcoded settings
    config_args = {
        "username": username,
        "password": password,
        "device": device,
        "config": config_file,
    }

    print(f"🚀 Launching secure session for {username} on {device}...")
    
    try:
        # Initialize and run the bot core
        bot = Bot()
        bot.run(config_args)
    except Exception as e:
        print(f"❌ An error occurred with {username}: {e}")
        # Note: 2FA prompts on the emulator will cause errors here
        
# --- Execution for your two accounts ---

# Account A: Daily Growth Strategy
run_bot(
    user_key="INSTAGRAM_USER_A",
    pass_key="INSTAGRAM_PASS_A",
    device_key="DEVICE_ID_A",
    config_file="accounts/account_A_username/daily_growth.yml" 
)

# Account B: Daily Growth Strategy (using the same config template)
# This will run sequentially. For true simultaneous runs, use separate terminals 
# or a proper process manager (like your N8N/Crawl4AI setup).
# run_bot(
#     user_key="INSTAGRAM_USER_B",
#     pass_key="INSTAGRAM_PASS_B",
#     device_key="DEVICE_ID_B",
#     config_file="accounts/account_B_username/daily_growth.yml"
# )
```

## 🎯 Phase 3: Strategy & Configuration Files

1. The Daily Growth Routine (20 Mins, Twice a Day)

Create a custom configuration file named `daily_growth.yml` inside your account folder (`accounts/your_username_A/`).

Requirement — GramAddict Job Configuration

- Like recent posts
- Included in `interact-hashtag-likers-recent` (often likes the source post too, but focuses on the likers).
- Follow likers: `interact-hashtag-likers-recent`
- Target specific competitors: `interact-blogger-followers`
- Human Simulation: `time-limit`, `action-delay` — built-in random delays are active.

File: `accounts/your_username_A/daily_growth.yml`

**IMPORTANT**: GramAddict v3.2.12 uses **FLAT YAML format**:
- ❌ NO `jobs:` wrapper section
- ❌ NO `time-limit` parameter (doesn't exist in v3.2.12)
- ✅ Use `repeat:` to control session duration
- ✅ Use FLAT action parameters (see examples below)

```yaml
# Configuration for your daily growth bot
username: "account_A_username"
device: 127.0.0.1:21533

# GROWTH STRATEGY (FLAT format - no 'jobs:' wrapper!)
hashtag-likers-recent: [your_niche_hashtag_1, your_niche_hashtag_2]
blogger-followers: [competitor_user_1, competitor_user_2]

# INTERACTION BEHAVIOR
likes-count: 1-2              # Like 1-2 posts per user profile
follow-percentage: 50         # Follow 50% of interacted users
stories-percentage: 30-40     # Watch stories 30-40% of the time
watch-video-time: 10-20       # Watch videos for 10-20 seconds

# SAFETY LIMITS (Session will stop when any limit is reached)
total-likes-limit: 50         # Stop after 50 likes
total-follows-limit: 20       # Stop after 20 follows
total-interactions-limit: 100 # Stop after 100 total interactions

# TIMING CONTROLS
repeat: 360-420               # Repeat every 6-7 hours (optional)
working-hours: [9-22]         # Only run between 9am-10pm (optional)
```

2. The Unfollow Cleanup (Once a Week)

Create a separate configuration file named `unfollow_weekly.yml` in the same folder. Run this only once a week (e.g., Sunday morning).

File: `accounts/your_username_A/unfollow_weekly.yml`

```yaml
username: "account_A_username"
device: 127.0.0.1:21533

# FLAT format - no 'jobs:' wrapper
unfollow-non-followers: 150-200   # Unfollow 150-200 non-followers
unfollow-delay: 3                 # Only unfollow if followed 3+ days ago
min-following: 100                # Keep at least 100 followings
```

3. Filter Configuration (No Business Accounts)

Edit the `filters.yml` file to skip users who are unlikely to follow back or are competition.

File: `accounts/your_username_A/filters.yml`

```yaml
# Skip accounts identified as business/creator accounts (looks for "Call", "Email", "Shop" buttons)
skip_business: true
skip_private: true  # Recommended to focus on profiles you can engage with

# Target audience profile size
min_followers: 100
max_followers: 5000
min_following: 50
max_following: 5000
min_posts: 5
```

## 🏃 Phase 4: Execution

Daily Execution

You can now run your daily job using the `launch.py` script and the specific config file.

```bash
# Run the daily growth routine for Account A
python launch.py

# To run the unfollow routine, you would need to modify the 'config_file' path in launch.py
# Or, simply run it directly via the GramAddict CLI:
# python run.py --config accounts/account_A_username/unfollow_weekly.yml --device 127.0.0.1:5555
```

This comprehensive plan covers the environment setup, secure authentication using `.env`, human-like behavior, and your specific growth and cleanup strategies.