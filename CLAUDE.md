# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Instagram automation bot using GramAddict (v3.2.12) running on MEmu Android emulator via ADB. The bot performs growth activities like following hashtag likers, engaging with competitor followers, and periodic unfollowing.

**Emulator Recommendation**: MEmu (official GramAddict recommendation) - BlueStacks 5 has UIAutomator2 compatibility issues that cause ATX-agent crashes.

## Environment Setup

**Virtual Environment:**
```bash
# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Required Environment Variables (.env):**
- `INSTAGRAM_USER_A`: Instagram username
- `INSTAGRAM_PASS_A`: Instagram password
- `DEVICE_ID_A`: ADB device ID (e.g., `127.0.0.1:5555`)

**ADB Connection:**
```bash
# Connect to MEmu instance (default port: 21503, 21513, 21523 for multi-instance)
adb connect 127.0.0.1:21533

# Verify connection
adb devices
```

## Running the Bot

**Test Run:**
```bash
python test_like_hashtag.py
```
This creates a temporary config at `accounts/temp/test_like.yml` and runs a minimal test (likes 1 post from #python hashtag).

**Production Run:**
Create YAML config files in `accounts/<username>/` directory following the pattern in plan.md, then use GramAddict CLI:
```bash
gramaddict run --config accounts/<username>/daily_growth.yml --device 127.0.0.1:5555
```

## Architecture

**Credential Management:**
- Never hardcode credentials in config files
- All sensitive data loads from `.env` via `python-dotenv`
- The `.env` file is gitignored

**Configuration Structure:**
- YAML configs define bot behavior (time limits, jobs, filters)
- Stored in `accounts/<username>/` subdirectories
- Common configs: `daily_growth.yml`, `unfollow_weekly.yml`, `filters.yml`
- Test configs use `accounts/temp/` with auto-generated YAML

**Core Scripts:**
- `test_like_hashtag.py`: Test launcher that programmatically generates config and calls `GramAddict.run()`
- `instaScript.py`: Basic credential loader (incomplete launcher stub)
- `distutils/__init__.py`: Compatibility shim for Python 3.12+ where stdlib distutils was removed

**GramAddict Integration:**
The bot uses GramAddict's entry point: `GramAddict.run(config=path, device=id)`. Pass config file path and device ID as kwargs to avoid argparse conflicts with complex usernames.

## Configuration Pattern

**IMPORTANT**: GramAddict v3.2.12 uses **FLAT YAML format** (no `jobs:` wrapper, no `time-limit` parameter).

YAML configs follow this structure:
```yaml
username: "<loaded_from_env>"
device: 127.0.0.1:21533

# Action parameters (FLAT format - no 'jobs:' wrapper)
hashtag-likers-recent: [hashtag1, hashtag2]
blogger-followers: [competitor1, competitor2]

# Interaction behavior
likes-count: 1-2                  # Like 1-2 posts per user
follow-percentage: 50             # Follow 50% of interacted users
total-likes-limit: 50             # Stop after 50 likes
total-follows-limit: 20           # Stop after 20 follows
total-interactions-limit: 100     # Stop after 100 interactions

# Optional: Timing controls
repeat: 120-180                   # Repeat session every 2-3 hours
working-hours: [9-22]             # Only run 9am-10pm
```

**Common Parameters**:
- `hashtag-likers-recent: [tag1, tag2]` - Interact with recent likers of hashtags
- `hashtag-likers-top: [tag1, tag2]` - Interact with top likers of hashtags
- `blogger-followers: [user1, user2]` - Interact with followers of users
- `blogger-following: [user1, user2]` - Interact with following of users
- `interact-from-file: [users.txt]` - Load target users from file

**Safety Filters** (filters.yml):
- `skip_business: true` - Skip business/creator accounts
- `min_followers` / `max_followers` - Target audience size
- `min_posts` - Ensure account is active

## Python Version Compatibility

Project runs on Python 3.13.5. The `distutils/` package provides backward compatibility shim since distutils was removed from stdlib in Python 3.12+. It forwards imports to `setuptools._distutils` to keep packages like `packaging` functional.

## Logs and Output

GramAddict writes logs to `logs/` directory (gitignored). Check recent logs for debugging failed sessions or Instagram blocks.

## Multi-Account Support

The project is designed for multiple accounts (INSTAGRAM_USER_A, INSTAGRAM_USER_B, etc.). Each account should have:
- Separate credentials in `.env`
- Separate config directory under `accounts/`
- Separate MEmu instance with unique ADB port (21503, 21513, 21523, etc.)
