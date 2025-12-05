# Linux Quick Reference - Instagram Bot

Quick command reference for daily operations on Linux (Pop!_OS/Ubuntu).

## Initial Setup (One-Time)

```bash
# 1. Install Python 3.11
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev

# 2. Clone repo
cd ~/repos
git clone <repository-url> instabot
cd instabot

# 3. Create venv
python3.11 -m venv .venv
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Configure credentials
nano .env
# Add: INSTAGRAM_USER_A, INSTAGRAM_PASS_A, DEVICE

# 6. Setup account structure
chmod +x setup_account_structure.sh
./setup_account_structure.sh

# 7. Install cron jobs
chmod +x install_cron_linux.sh
./install_cron_linux.sh
```

---

## Daily Commands

### Check Device Connection

```bash
# List devices
adb devices
# Should show: fbc9d1f30eb2    device

# Restart ADB if device not showing
adb kill-server
adb start-server
adb devices
```

### Manual Session Testing

```bash
cd ~/repos/instabot
source .venv/bin/activate

# Test sessions
python runner.py morning   # 45-60 min, ~40 interactions
python runner.py lunch     # 45-60 min, ~40 interactions
python runner.py evening   # 30-45 min, ~30 interactions
python runner.py extra     # 30-45 min, ~25 interactions

# Test strategies
python runner.py growth    # Growth strategy
python runner.py cleanup   # Unfollow non-mutuals

# Quick test
python test_like.py        # 3-8 min test session
```

### Monitor Logs

```bash
# Watch cron execution log
tail -f ~/repos/instabot/logs/cron.log

# Watch GramAddict session logs
tail -f ~/repos/instabot/logs/gramaddict_morning.log
tail -f ~/repos/instabot/logs/gramaddict_lunch.log
tail -f ~/repos/instabot/logs/gramaddict_evening.log

# Check recent crashes
ls -lt ~/repos/instabot/crashes/

# Search for errors
grep -i "error\|fail\|blocked" ~/repos/instabot/logs/gramaddict_*.log | tail -20
```

### Check Cron Jobs

```bash
# List installed cron jobs
crontab -l

# Edit cron schedule
crontab -e

# Check cron service status
systemctl status cron

# View system cron logs
journalctl -u cron | tail -30
```

---

## Session Schedule

| Time | Session | Duration | Interactions | Days |
|------|---------|----------|--------------|------|
| 9:30am | Morning | 45-60 min | ~40 | Daily |
| 1:45pm | Lunch | 45-60 min | ~40 | Daily |
| 3:30pm | Extra | 30-45 min | ~25 | Mon/Wed/Fri |
| 6:15pm | Evening | 30-45 min | ~30 | Daily |
| 11:00pm | Cleanup | 5-10 min | Unfollows | Sunday |

**Total Activity:**
- **3 sessions/day** (Tue/Thu/Sat/Sun): ~110 interactions, 65 likes, 22 follows
- **4 sessions/day** (Mon/Wed/Fri): ~135 interactions, 80 likes, 27 follows
- **Weekly average**: ~150-200 interactions/day

---

## Troubleshooting

### Device Not Found

```bash
# Check USB connection
adb devices

# Restart ADB
adb kill-server
adb start-server

# Check device authorization
# Look at device screen for "Allow USB Debugging?" prompt
```

### Bot Not Running from Cron

```bash
# Check cron is running
systemctl status cron

# Check Python path
~/repos/instabot/.venv/bin/python --version
# Should show: Python 3.11.x

# Test command manually
cd ~/repos/instabot && .venv/bin/python runner.py morning
```

### Instagram Not Opening

```bash
# Check Instagram installed
adb -s fbc9d1f30eb2 shell pm list packages | grep instagram

# Launch Instagram manually
adb -s fbc9d1f30eb2 shell am start -n com.instagram.android/.activity.MainTabActivity

# Check Instagram version
adb -s fbc9d1f30eb2 shell dumpsys package com.instagram.android | grep versionName
# Should show: versionName=300.0.0.29.110
```

### Python 3.13 Crash (`'Iter' object is not iterable`)

```bash
# Recreate venv with Python 3.11
cd ~/repos/instabot
rm -rf .venv
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Verify version
python --version
# Should show: Python 3.11.x
```

### Filter Warning (`can't find filter.json`)

```bash
cd ~/repos/instabot
./setup_account_structure.sh

# Manually create if needed
mkdir -p accounts/maxhaider.dev
cp accounts/filters.yml accounts/maxhaider.dev/filter.json
```

---

## Configuration Files

### Session Configs

```bash
accounts/
├── maxhaider.dev/
│   └── filter.json          # Account-specific filters
├── session_morning.yml      # Morning session (Python/Django/FastAPI)
├── session_lunch.yml        # Lunch session (Linux/Terraform/CI/CD)
├── session_evening.yml      # Evening session (Data/Cloud/AI)
├── session_extra.yml        # Extra session (General tech)
├── strategy_growth.yml      # Daily growth
├── strategy_cleanup.yml     # Weekly cleanup
└── filters.yml              # Base filters
```

### Update Session Targets

```bash
# Edit session configs
nano ~/repos/instabot/accounts/session_morning.yml

# Update these lines:
# hashtag-likers-top: [your, hashtags, here]
# blogger-post-likers: [competitor1, competitor2, competitor3]
```

### Update Device/Username

```bash
# Update .env file
nano ~/repos/instabot/.env

# Update these lines:
# INSTAGRAM_USER_A=maxhaider.dev
# DEVICE=fbc9d1f30eb2

# Or update session configs directly
nano ~/repos/instabot/accounts/session_morning.yml

# Update:
# username: maxhaider.dev
# device: fbc9d1f30eb2
```

---

## Maintenance

### Weekly Checks

```bash
# 1. Check device connection
adb devices

# 2. Review error logs
grep -i "error\|blocked" ~/repos/instabot/logs/gramaddict_*.log | tail -20

# 3. Check cron execution
grep "$(date +%Y-%m-%d)" ~/repos/instabot/logs/cron.log

# 4. View session metrics (if metrics_analyzer.py exists)
cd ~/repos/instabot
source .venv/bin/activate
python metrics_analyzer.py maxhaider.dev
```

### Clean Old Logs

```bash
# Delete logs older than 30 days
find ~/repos/instabot/logs -name "*.log" -mtime +30 -delete

# Delete old crash dumps
find ~/repos/instabot/crashes -name "*.zip" -mtime +30 -delete
```

### Backup Configuration

```bash
# Backup important files
cd ~/repos
tar -czf instabot_backup_$(date +%Y%m%d).tar.gz \
    instabot/.env \
    instabot/accounts/*.yml \
    instabot/accounts/maxhaider.dev/

# Restore from backup
tar -xzf instabot_backup_20251205.tar.gz
```

---

## Emergency Commands

### Stop All Bot Activity

```bash
# Comment out all cron jobs
crontab -e
# Add '#' at start of each line

# Or temporarily remove crontab
crontab -r

# Restore from backup
crontab ~/crontab_backup_*.txt
```

### Kill Running Session

```bash
# Find process
ps aux | grep gramaddict

# Kill by PID
kill -9 <PID>

# Or kill all Python processes (DANGEROUS - kills everything)
# pkill -9 python
```

### Reset Instagram Session

```bash
# Force stop Instagram
adb -s fbc9d1f30eb2 shell am force-stop com.instagram.android

# Clear app cache (keeps login)
adb -s fbc9d1f30eb2 shell pm clear --cache-only com.instagram.android

# Launch Instagram
adb -s fbc9d1f30eb2 shell am start -n com.instagram.android/.activity.MainTabActivity
```

---

## Performance Tips

### Keep Device Awake

```bash
# Enable "Stay awake" in Developer Options on device
# This prevents screen timeout when charging

# Or via ADB (temporary)
adb -s fbc9d1f30eb2 shell svc power stayon true
```

### Optimize Session Times

```bash
# Randomize cron times slightly
# Instead of: 30 9 * * *
# Use: 25-35 9 * * * (requires cron with random support)

# Or manually vary times by ±15 minutes each week
crontab -e
```

### Monitor Resource Usage

```bash
# Check disk space
df -h ~/repos/instabot

# Check memory
free -h

# Check CPU usage during session
htop
# Look for Python processes
```

---

## Key Files Reference

| File | Purpose | Location |
|------|---------|----------|
| `.env` | Credentials & device ID | `~/repos/instabot/.env` |
| Session configs | Bot behavior | `~/repos/instabot/accounts/session_*.yml` |
| Filters | Target filtering | `~/repos/instabot/accounts/maxhaider.dev/filter.json` |
| Cron log | Cron execution | `~/repos/instabot/logs/cron.log` |
| Session logs | Bot activity | `~/repos/instabot/logs/gramaddict_*.log` |
| Crashes | Error dumps | `~/repos/instabot/crashes/*.zip` |
| Cron schedule | Automation | `crontab -l` |

---

## Support Resources

- **Documentation**: `~/repos/instabot/docs/`
- **Config templates**: `~/repos/instabot/config-templates/`
- **GramAddict docs**: https://github.com/GramAddict/bot
- **Project README**: `~/repos/instabot/README.md`
- **Claude.md**: `~/repos/instabot/CLAUDE.md`

---

## Quick Status Check

```bash
#!/bin/bash
# Save as: ~/repos/instabot/status.sh
# Usage: ./status.sh

echo "=== Instagram Bot Status ==="
echo ""
echo "Device Connection:"
adb devices | grep -v "List of devices"
echo ""
echo "Python Version:"
~/repos/instabot/.venv/bin/python --version
echo ""
echo "Instagram Version:"
adb -s fbc9d1f30eb2 shell dumpsys package com.instagram.android | grep versionName | head -1
echo ""
echo "Recent Cron Runs:"
tail -5 ~/repos/instabot/logs/cron.log
echo ""
echo "Cron Schedule:"
crontab -l | grep -v "^#" | grep -v "^$"
echo ""
```

Make executable: `chmod +x ~/repos/instabot/status.sh`

---

**Happy botting! 🤖🚀**
