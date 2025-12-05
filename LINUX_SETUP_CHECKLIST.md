# Linux Setup Checklist - Ready for Production

Your Linux machine (Pop!_OS) is now ready for automated Instagram growth. Follow this checklist to complete the setup.

## ✅ What's Already Done

- ✅ Python 3.11 installed and working
- ✅ Virtual environment created with Python 3.11
- ✅ Dependencies installed (`packaging>=24.0` fix applied)
- ✅ Instagram v300 installed on device fbc9d1f30eb2
- ✅ Device connected via USB (no `adb connect` needed)
- ✅ Bot successfully tested (no more `'Iter' object is not iterable` crash)
- ✅ Session configs updated for Linux + v300 compatibility
- ✅ Templates created for all session types

## 📋 Final Steps on Linux Machine

### 1. Pull Latest Changes from Git

```bash
cd ~/repos/instabot
git pull origin main
```

This gets you:
- Updated `session_morning.yml`, `session_lunch.yml`, `session_evening.yml`, `session_extra.yml`
- New `install_cron_linux.sh` script
- New `setup_account_structure.sh` script
- New session templates in `config-templates/`
- Updated documentation

### 2. Setup Account Structure (Fix filter.json Warning)

```bash
cd ~/repos/instabot
chmod +x setup_account_structure.sh
./setup_account_structure.sh
```

Enter username when prompted: `maxhaider.dev`

This creates: `accounts/maxhaider.dev/filter.json`

### 3. Test All Session Configs

```bash
source .venv/bin/activate

# Test each session (Ctrl+C after it starts successfully)
python runner.py morning   # Should start targeting Python/Django hashtags
python runner.py lunch     # Should start targeting Linux/Terraform hashtags
python runner.py evening   # Should start targeting Data/Cloud hashtags
python runner.py extra     # Should start targeting General tech hashtags
```

**Expected output for each:**
```
INFO | Device screen ON and unlocked.
INFO | Open Instagram app.
INFO | Ready for botting!🤫
INFO | Instagram version: 300.0.0.29.110
INFO | Logged in as maxhaider.dev
INFO | Interactions count: 4-8
```

### 4. Install Cron Jobs

```bash
cd ~/repos/instabot
chmod +x install_cron_linux.sh

# Review the script (optional)
nano install_cron_linux.sh

# Install cron jobs
./install_cron_linux.sh
```

**Installed schedule:**
- 9:30am daily - Morning session
- 1:45pm daily - Lunch session
- 6:15pm daily - Evening session
- 3:30pm Mon/Wed/Fri - Extra session
- 11:00pm Sunday - Cleanup

### 5. Verify Cron Installation

```bash
# List cron jobs
crontab -l

# You should see:
# - Instagram Bot section
# - 5 cron entries (morning, lunch, evening, extra, cleanup)
```

### 6. Monitor First Automated Run

Wait for the next scheduled time, then:

```bash
# Watch cron log
tail -f ~/repos/instabot/logs/cron.log

# Watch session log (in another terminal)
tail -f ~/repos/instabot/logs/gramaddict_morning.log
```

**First run times:**
- If setup before 9:30am → Morning session runs at 9:30am
- If setup after 9:30am → Wait for Lunch session at 1:45pm

---

## 📊 Expected Daily Activity

**Most days (Tue/Thu/Sat/Sun):**
- 3 sessions
- 110-120 interactions
- 65-75 likes
- 22-25 follows
- Total time: ~2-2.5 hours

**Extra days (Mon/Wed/Fri):**
- 4 sessions
- 135-150 interactions
- 80-90 likes
- 27-30 follows
- Total time: ~2.5-3 hours

**Weekly:**
- 1 cleanup session (Sunday 11pm)
- Unfollows non-mutuals
- Keeps followers/mutuals

---

## 🔍 Daily Monitoring

### Morning Check (9:00am)

```bash
# Check device connection
adb devices
# Should show: fbc9d1f30eb2    device

# Check cron log for overnight issues
tail -20 ~/repos/instabot/logs/cron.log
```

### Evening Check (10:00pm)

```bash
# Check today's sessions
grep "$(date +%Y-%m-%d)" ~/repos/instabot/logs/cron.log

# Check for errors
grep -i "error\|blocked" ~/repos/instabot/logs/gramaddict_*.log | tail -10

# View latest session log
ls -lt ~/repos/instabot/logs/gramaddict_*.log | head -1
```

### Weekly Review (Sunday)

```bash
# Review entire week
grep -i "error\|warning\|blocked" ~/repos/instabot/logs/gramaddict_*.log | wc -l

# Check disk space
df -h ~/repos/instabot

# Clean old logs (keep last 30 days)
find ~/repos/instabot/logs -name "*.log" -mtime +30 -delete
```

---

## 🚨 What to Watch For

### Red Flags

⚠️ **Action Blocked** - Instagram detected automation
```
ERROR | Action blocked by Instagram
```
**Solution**: Stop bot for 48 hours, then restart with 2 sessions/day

⚠️ **Login Challenge** - Instagram wants verification
```
ERROR | Login challenge required
```
**Solution**: Manually login on device, complete challenge

⚠️ **Device Not Found** - USB connection lost
```
ERROR | Device fbc9d1f30eb2 not found
```
**Solution**: Check USB cable, run `adb devices`, reconnect if needed

### Green Flags

✅ **High rejection rate (60-80%)** - Normal!
```
INFO | Skipped: private account
INFO | Skipped: already liked
INFO | Skipped: empty account
```
**Explanation**: Filters are working correctly

✅ **2-3 successful interactions out of 8 attempts** - Expected!
```
INFO | Successful interactions: 2 out of 8
```
**Explanation**: This is normal human-like success rate

---

## 🛠️ Troubleshooting Commands

### Device Connection Issues

```bash
# Restart ADB
adb kill-server
adb start-server
adb devices

# Check device authorization
# Look at device screen for "Allow USB Debugging?" prompt
```

### Bot Not Running

```bash
# Check cron is active
systemctl status cron

# Test command manually
cd ~/repos/instabot && .venv/bin/python runner.py morning

# Check Python version
~/repos/instabot/.venv/bin/python --version
# Should show: Python 3.11.x
```

### Instagram Not Opening

```bash
# Check Instagram installed
adb -s fbc9d1f30eb2 shell pm list packages | grep instagram

# Launch manually
adb -s fbc9d1f30eb2 shell am start -n com.instagram.android/.activity.MainTabActivity

# Verify version
adb -s fbc9d1f30eb2 shell dumpsys package com.instagram.android | grep versionName
# Should show: versionName=300.0.0.29.110
```

---

## 📚 Documentation Reference

| Document | Purpose |
|----------|---------|
| [LINUX_QUICK_REFERENCE.md](docs/LINUX_QUICK_REFERENCE.md) | Daily command cheatsheet |
| [LINUX_USB_DEVICE_SETUP.md](docs/LINUX_USB_DEVICE_SETUP.md) | Complete setup guide |
| [CLAUDE.md](CLAUDE.md) | Project architecture |
| [README.md](README.md) | General overview |

---

## 🎯 Production Readiness Checklist

Before going live, verify:

- [ ] Device connected: `adb devices` shows fbc9d1f30eb2
- [ ] Python 3.11: `.venv/bin/python --version` shows 3.11.x
- [ ] Instagram v300 installed and logged in
- [ ] Account structure: `accounts/maxhaider.dev/filter.json` exists
- [ ] All session configs tested successfully
- [ ] Cron jobs installed: `crontab -l` shows 5 entries
- [ ] Cron service running: `systemctl status cron`
- [ ] Logs directory exists: `~/repos/instabot/logs/`
- [ ] Device stays awake (Developer Options → Stay awake)
- [ ] USB cable is good quality (prevents disconnections)

---

## 🚀 You're Ready!

Your Linux automation is now complete! The bot will:

✅ Run 3-4 sessions daily at varying times
✅ Target Backend/DevOps/Infrastructure niche
✅ Mix hashtags and blogger post likers for variety
✅ Unfollow non-mutuals weekly
✅ Log everything for monitoring
✅ Use human-like behavior patterns

**First automated session**: Next scheduled cron time
**Monitoring**: Check logs daily for first week
**Safety**: Bot respects Instagram limits (150-200 interactions/day)

Good luck with your Instagram growth! 🤖✨
