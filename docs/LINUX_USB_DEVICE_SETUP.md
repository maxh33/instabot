# Linux USB Device Setup (Quick Start)

Setup guide for running the Instagram bot on Linux with a physical Android device via USB.

## Overview

**Target Setup:**
- **OS**: Linux (tested on Pop!_OS/Ubuntu)
- **Device**: Mi A3 (fbc9d1f30eb2) via USB
- **Instagram**: v313
- **Python**: 3.13
- **Scheduler**: Cron jobs

---

## Prerequisites

### 1. Install ADB

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install android-tools-adb android-tools-fastboot

# Verify installation
adb version
```

### 2. Setup USB Device

**On Android device:**
1. Enable Developer Options (tap Build Number 7 times)
2. Enable USB Debugging
3. Connect via USB cable
4. Authorize USB debugging when prompted

**Verify connection:**
```bash
# Should show your device
adb devices

# Expected output:
# fbc9d1f30eb2    device
```

**Important**: Physical USB devices don't need `adb connect` (only emulators do).

---

## Installation

### 1. Clone Repository

```bash
cd ~/repos
git clone <repository-url> instabot
cd instabot
```

### 2. Setup Python Environment

**IMPORTANT: Use Python 3.11** (GramAddict v3.2.12 crashes on Python 3.13)

```bash
# Install Python 3.11 (if not already installed)
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# Create virtual environment with Python 3.11
python3.11 -m venv .venv

# Activate
source .venv/bin/activate

# Verify Python version (should be 3.11.x)
python --version

# Install dependencies
pip install -r requirements.txt

# If using uv (faster):
# uv pip install -r requirements.txt
```

**Why Python 3.11?**
- GramAddict v3.2.12 uses `collections.Iterable` (removed in Python 3.13)
- Crash error on 3.13: `'Iter' object is not iterable`
- Python 3.11 is the officially tested version

### 3. Configure Environment

Create `.env` file:

```bash
nano .env
```

Add your credentials:

```env
# Instagram Credentials
INSTAGRAM_USER_A=maxhaider.dev
INSTAGRAM_PASS_A=your_password_here

# Device Configuration (USB device ID)
DEVICE=fbc9d1f30eb2
```

Save and exit (Ctrl+X, Y, Enter).

---

## Account Structure Setup

**Fix the filter.json warning:**

```bash
# Create account-specific directory and copy filters
chmod +x setup_account_structure.sh
./setup_account_structure.sh
```

This creates `accounts/maxhaider.dev/filter.json` and eliminates the warning.

---

## Testing

### Manual Test Run

```bash
# Activate venv
source .venv/bin/activate

# Run 3-minute test
python test_like.py

# Or test session configs
python runner.py morning   # Test morning session
python runner.py lunch     # Test lunch session
python runner.py evening   # Test evening session
python runner.py extra     # Test extra session
python runner.py growth    # Test growth strategy
python runner.py cleanup   # Test cleanup (unfollows)
```

**Expected behavior:**
- Opens Instagram on device
- Performs interactions based on session config
- Check logs: `tail -f logs/gramaddict_*.log`

### Verify Device Access

```bash
# Check device connection
adb devices

# Verify Instagram is installed
adb shell pm list packages | grep instagram

# Test app launch
adb shell am start -n com.instagram.android/.activity.MainTabActivity
```

---

## Cron Setup

### Automated Installation (Recommended)

```bash
# Make script executable
chmod +x install_cron_linux.sh

# Review and customize PROJECT_DIR if needed
nano install_cron_linux.sh

# Install cron jobs
./install_cron_linux.sh
```

**Installed schedule:**
- **Morning**: 9:30am daily (session_morning.yml)
- **Lunch**: 1:45pm daily (session_lunch.yml)
- **Evening**: 6:15pm daily (session_evening.yml)
- **Extra**: 3:30pm Mon/Wed/Fri (session_extra.yml)
- **Cleanup**: 11:00pm Sunday (unfollows non-mutuals)

**Expected activity:**
- 3-4 sessions per day (150-200 interactions)
- 90-120 likes per day
- 30-40 follows per day

### Manual Installation (Alternative)

Edit crontab:

```bash
crontab -e
```

Add schedule:

```bash
# Instagram Bot - Automated Sessions
# Morning session: 9:30am
30 9 * * * cd ~/repos/instabot && .venv/bin/python runner.py morning >> logs/cron.log 2>&1

# Lunch session: 1:45pm
45 13 * * * cd ~/repos/instabot && .venv/bin/python runner.py lunch >> logs/cron.log 2>&1

# Evening session: 6:15pm
15 18 * * * cd ~/repos/instabot && .venv/bin/python runner.py evening >> logs/cron.log 2>&1

# Extra session: 3:30pm (Mon/Wed/Fri only)
30 15 * * 1,3,5 cd ~/repos/instabot && .venv/bin/python runner.py extra >> logs/cron.log 2>&1

# Weekly cleanup: Sunday 11pm
0 23 * * 0 cd ~/repos/instabot && .venv/bin/python runner.py cleanup >> logs/cron.log 2>&1
```

**Important**: Use absolute paths in cron:
- ✅ `~/repos/instabot` or `/home/username/repos/instabot`
- ✅ `.venv/bin/python` (relative to project dir)
- ❌ Don't use `python` alone (cron has limited PATH)

### Verify Cron Jobs

```bash
# List installed jobs
crontab -l

# Check cron service status
systemctl status cron

# Test cron log
tail -f ~/repos/instabot/logs/cron.log
```

### 3. Monitor Execution

```bash
# Watch cron log
tail -f ~/repos/instabot/logs/cron.log

# Watch GramAddict log
tail -f ~/repos/instabot/logs/gramaddict_*.log

# Check last run
ls -lt ~/repos/instabot/logs/
```

---

## USB Device Best Practices

### Keep Device Connected

**Power saving issues:**
1. Disable USB selective suspend on Linux
2. Keep device charged (use USB hub with power)
3. Prevent device sleep (use developer option "Stay awake")

**udev rules (optional - for better USB stability):**

Create `/etc/udev/rules.d/51-android.rules`:

```bash
sudo nano /etc/udev/rules.d/51-android.rules
```

Add:

```
# Xiaomi Mi A3
SUBSYSTEM=="usb", ATTR{idVendor}=="2717", MODE="0666", GROUP="plugdev"
```

Reload:

```bash
sudo udevadm control --reload-rules
sudo udevadm trigger
```

### Handle USB Disconnections

**Check device before running:**

Create wrapper script `safe_run.sh`:

```bash
#!/bin/bash
cd ~/repos/instabot
source .venv/bin/activate

# Check device connection
if ! adb devices | grep -q "fbc9d1f30eb2"; then
    echo "[$(date)] ERROR: Device not connected" >> logs/cron.log
    exit 1
fi

# Run bot
python runner.py "$@"
```

Make executable:

```bash
chmod +x safe_run.sh
```

Update crontab to use wrapper:

```bash
30 9 * * * ~/repos/instabot/safe_run.sh growth >> ~/repos/instabot/logs/cron.log 2>&1
```

---

## Monitoring & Maintenance

### Daily Checks

```bash
# Check device connection
adb devices

# View recent logs
tail -n 50 ~/repos/instabot/logs/gramaddict_*.log

# Check cron execution
grep "$(date +%Y-%m-%d)" ~/repos/instabot/logs/cron.log

# View metrics
cd ~/repos/instabot
source .venv/bin/activate
python metrics_analyzer.py maxhaider.dev
```

### Weekly Review

```bash
# Check for errors
grep -i "error\|fail\|blocked" ~/repos/instabot/logs/gramaddict_*.log | tail -20

# Review metrics
python metrics_analyzer.py maxhaider.dev sources

# Clean old logs (keep last 30 days)
find ~/repos/instabot/logs -name "*.log" -mtime +30 -delete
```

### Troubleshooting

**Device not showing:**
```bash
# Restart ADB server
adb kill-server
adb start-server

# Check connection
adb devices

# Re-authorize on device if needed
```

**Bot not running from cron:**
```bash
# Check cron service
systemctl status cron

# View system cron logs
journalctl -u cron | tail -20

# Test cron command manually
cd ~/repos/instabot && .venv/bin/python runner.py growth

# Check permissions
ls -la ~/repos/instabot/runner.py
ls -la ~/repos/instabot/.venv/bin/python
```

**Instagram not opening:**
```bash
# Test ADB access
adb shell pm list packages | grep instagram

# Launch manually
adb shell am start -n com.instagram.android/.activity.MainTabActivity

# Check if logged in (open Instagram manually if needed)
```

---

## Production Checklist

Before going live:

- [ ] ADB installed and working
- [ ] Device connected (shows in `adb devices`)
- [ ] USB debugging authorized on device
- [ ] Python venv created and activated
- [ ] Dependencies installed (no errors)
- [ ] `.env` file configured
- [ ] Manual test successful (`python test_like.py`)
- [ ] Logs directory exists (`logs/`)
- [ ] Cron jobs installed (`crontab -l`)
- [ ] Device stays awake (developer option)
- [ ] Device stays charged
- [ ] Monitoring commands tested

---

## Key Differences from Windows

| Aspect | Windows | Linux |
|--------|---------|-------|
| **Activate venv** | `.venv\Scripts\activate` | `source .venv/bin/activate` |
| **Python in cron** | Not applicable | Use `.venv/bin/python` |
| **Path separator** | `\` (backslash) | `/` (forward slash) |
| **Cron** | Task Scheduler | `crontab -e` |
| **Logs location** | Relative to project | Use absolute paths |
| **ADB location** | Android SDK or `adb` in PATH | `android-tools-adb` package |

---

## Summary

You now have:
- ✅ Linux environment with USB device support
- ✅ Python 3.13 compatibility (packaging>=24.0)
- ✅ Bot configured for device fbc9d1f30eb2
- ✅ Cron scheduling for automated runs
- ✅ Monitoring and maintenance commands

**Next Steps:**
1. Run first manual test
2. Install cron jobs
3. Monitor first 3 days closely
4. Adjust schedule as needed

Good luck! 🚀
