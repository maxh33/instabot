# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Instagram automation bot using GramAddict (v3.2.12) running on physical Android device (Mi A3) via USB/ADB. The bot performs growth activities like following hashtag likers, engaging with competitor followers, and periodic unfollowing.

**Device Setup**: Currently using Mi A3 (device ID: fbc9d1f30eb2) connected via USB. MEmu emulator is an alternative option (official GramAddict recommendation). BlueStacks 5 has UIAutomator2 compatibility issues that cause ATX-agent crashes.

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
- `DEVICE`: ADB device ID (e.g., `fbc9d1f30eb2` for USB, `127.0.0.1:21533` for emulator)

**ADB Connection:**

**Physical Device (Current Setup - Mi A3)**:
```bash
# Enable USB debugging on Android device
# Connect via USB cable
# Authorize USB debugging when prompted on device

# Verify connection (no adb connect needed for USB)
adb devices
# Should show: fbc9d1f30eb2    device
```

**MEmu Emulator (Alternative)**:
```bash
# Connect to MEmu instance (default port: 21503, 21513, 21523 for multi-instance)
adb connect 127.0.0.1:21533

# Verify connection
adb devices
```

**Important**: USB devices connect automatically (don't use `adb connect`). Only network devices/emulators need `adb connect`.

## Running the Bot

**Test Run:**
```bash
python test_like.py
```
This creates an enhanced test config at `accounts/test_like_enhanced.yml` and runs a 3-minute test session with:
- Mixed sources (hashtag top likers + competitor post likers)
- Human-like behavior with randomization
- Debug mode enabled
- Session limits: 8 interactions, 6 likes, 2 follows

**Production Run:**
Use the task runner for production strategies:
```bash
# Daily growth strategy
python runner.py growth

# Weekly cleanup
python runner.py cleanup
```

Or run GramAddict CLI directly:
```bash
gramaddict run --config accounts/strategy_growth.yml
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
- `test_like.py`: Enhanced test launcher - generates `test_like_enhanced.yml` with human-like behavior
- `runner.py`: Production task selector for growth/cleanup strategies
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
- `hashtag-likers-recent: [tag1, tag2]` - Interact with recent likers (requires Recent tab)
- `hashtag-likers-top: [tag1, tag2]` - Interact with top likers (use for Instagram v313)
- `blogger-post-likers: [user1, user2]` - Interact with likers of competitor posts
- `blogger-followers: [user1, user2]` - Interact with followers of users
- `blogger-following: [user1, user2]` - Interact with following of users
- `interact-from-file: [users.txt]` - Load target users from file

**Important**: Parameter is `blogger-post-likers` (NOT `interact-blogger-post-likers`)

**Safety Filters** (filters.yml):
- `skip_business: true` - Skip business/creator accounts
- `min_followers` / `max_followers` - Target audience size
- `min_posts` - Ensure account is active

## Python Version Compatibility

**Recommended: Python 3.11** (GramAddict v3.2.12 is tested with this version)

**Windows (Python 3.13.5)**: Works with `packaging>=24.0` and `distutils/` compatibility shim
- The `distutils/` shim forwards imports to `setuptools._distutils`
- `packaging>=24.0` removes distutils dependency

**Linux (Python 3.11 REQUIRED)**: GramAddict v3.2.12 crashes on Python 3.13 with `'Iter' object is not iterable`
- **Solution**: Use Python 3.11 on Linux systems
- Install: `sudo apt install python3.11 python3.11-venv`
- Create venv: `python3.11 -m venv .venv`

**Common Setup Issues**:
- `ModuleNotFoundError: No module named 'pkg_resources'` → Install: `pip install setuptools`
- `'Iter' object is not iterable` (Linux) → Use Python 3.11 instead of 3.13

## Logs and Output

GramAddict writes logs to `logs/` directory (gitignored). Check recent logs for debugging failed sessions or Instagram blocks.

## Multi-Account Support

The project is designed for multiple accounts (INSTAGRAM_USER_A, INSTAGRAM_USER_B, etc.). Each account should have:
- Separate credentials in `.env`
- Separate config directory under `accounts/`
- Separate physical device OR emulator instance with unique ADB identifier

## Current Setup (Production)

**Device**: Mi A3 (fbc9d1f30eb2) - Physical device via USB
**Instagram Version**: v313 (compatible with GramAddict v3.2.12)
**Account**: maxhaider.dev
**Niche**: Backend/DevOps/Infrastructure development

**Test Configuration**: `accounts/test_like_enhanced.yml`
- Duration: ~3-8 minutes per session
- Targets: Mix of hashtag likers (#python, #django, #fastapi, #backend, #devops) + competitor post likers (@realpython, @freecodecamp, @thepracticaldev)
- Behavior: Enhanced randomization (0.75 speed multiplier, wide ranges for watch times)
- Filters: Auto-reject private accounts, empty accounts, already-liked posts

**Production Strategies**:
- `strategy_growth.yml`: Daily growth targeting competitor post likers
- `strategy_cleanup.yml`: Weekly cleanup unfollowing non-mutuals

## Weekly Reporting System

**Automated Telegram Reports**: The bot generates weekly performance reports and delivers them via Telegram using n8n webhook integration.

**Report Contents**:
- Weekly summary (sessions, interactions, likes, follows, success rate)
- Daily breakdown with per-day metrics
- Follower growth tracking
- Top 5 performing sources (hashtags/accounts)
- Filter effectiveness statistics

**Architecture**: Python → n8n Webhook → Telegram
1. Cron triggers `reports/generate_weekly_report.py` every Sunday at 11:30pm
2. Script aggregates 7-day metrics using `metrics_analyzer.py`
3. Sends JSON payload to secure n8n webhook (UUID-protected)
4. n8n formats message and sends via Telegram bot

**Environment Variables**:
- `N8N_WEBHOOK_URL`: n8n webhook endpoint (use hashed URL for security)
- `TELEGRAM_TOKEN`: Telegram bot token (optional, used by n8n)

**Manual Testing**:
```bash
# Dry run (print JSON without sending)
python reports/generate_weekly_report.py --dry-run

# Test with custom period
python reports/generate_weekly_report.py --days 3

# Actual send (production)
python reports/generate_weekly_report.py
```

**Failed Report Recovery**:
If webhook fails, reports are saved to `reports/failed/` for manual retry.

## Automation & Cron Setup

**Linux Cron with Random Delays**: Sessions run with 0-15 minute random delays to prevent Instagram pattern detection.

**Schedule**:
```bash
Morning:  9:30am-9:45am daily
Lunch:    1:45pm-2:00pm daily
Evening:  6:15pm-6:30pm daily
Extra:    3:30pm-3:45pm Mon/Wed/Fri
Cleanup:  11:00pm-11:15pm Sunday
Report:   11:30pm Sunday (weekly)
```

**Installation**:
```bash
chmod +x install_cron_linux.sh
./install_cron_linux.sh
```

The script automatically:
- Backs up existing crontab
- Removes old Instagram bot entries
- Installs new jobs with random delays (`sleep $((RANDOM % 900))`)
- Preserves other cron jobs

**Monitoring**:
```bash
crontab -l                        # View installed jobs
tail -f logs/cron.log             # Session logs
tail -f logs/weekly_report.log    # Report logs
```

## Metrics & Analytics

**Metrics Analyzer**: `metrics_analyzer.py` provides comprehensive analytics:
- Session statistics (success rate, duration, interactions)
- Account statistics (total interactions, current following)
- Source performance (which hashtags/accounts work best)
- Filter effectiveness (rejection rates, private/empty accounts)
- Follower growth tracking

**Usage**:
```bash
# View all metrics for an account
python metrics_analyzer.py maxhaider.dev

# Session stats for last 7 days
python metrics_analyzer.py maxhaider.dev --days 7

# Source performance
python metrics_analyzer.py maxhaider.dev --source-performance
```

## Key Learnings

### Instagram v313 Limitations
- **No Recent Tab**: Use `hashtag-likers-top` instead of `hashtag-likers-recent`
- **UI Changes**: Some elements may differ from tested v300

### Parameter Name Fixes
- ✅ Correct: `blogger-post-likers`
- ❌ Wrong: `interact-blogger-post-likers` (causes immediate exit)

### Human-like Behavior Success
- **Watch times**: Highly randomized (2s photos, 12-18s videos, 23s stories)
- **Action variety**: Stories, carousels, videos, photos all engaged naturally
- **Filter effectiveness**: 75% rejection rate (private/empty accounts) is normal
- **Success rate**: 2-3 successful interactions per 8 attempts is expected
- **Random cron delays**: 0-15 minute variance prevents Instagram pattern detection

### Performance Notes
- Each interaction: 10-60 seconds depending on content type
- 8 interactions typically complete in 3-8 minutes
- Speed multiplier 0.75 provides good human-like pacing
- Wide randomization ranges (e.g., 5-30s) prevent pattern detection
- Weekly reports complete in <10 seconds
