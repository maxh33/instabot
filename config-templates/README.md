# Config Templates

This directory contains template configuration files for the Instagram bot.

## Available Templates

### Session Configs (Time-based automation)

- **session_morning.yml.example** - Morning session (9-11am), Python/Backend focus
- **session_lunch.yml.example** - Lunch session (12-2pm), Infrastructure/DevOps focus
- **session_evening.yml.example** - Evening session (5-7pm), Data/Cloud focus
- **session_extra.yml.example** - Extra session (flexible), General tech content

### Strategy Configs (Goal-based automation)

- **strategy_growth.yml.example** - Daily growth (follow/like competitors)
- **strategy_cleanup.yml.example** - Weekly cleanup (unfollow non-mutuals)

### Filter Config

- **filters.yml.example** - Quality filters for all sessions

---

## Setup Instructions

### 1. Copy templates to accounts directory

**Windows:**
```bash
mkdir accounts

# Session configs
copy config-templates\session_morning.yml.example accounts\session_morning.yml
copy config-templates\session_lunch.yml.example accounts\session_lunch.yml
copy config-templates\session_evening.yml.example accounts\session_evening.yml
copy config-templates\session_extra.yml.example accounts\session_extra.yml

# Strategy configs
copy config-templates\strategy_growth.yml.example accounts\strategy_growth.yml
copy config-templates\strategy_cleanup.yml.example accounts\strategy_cleanup.yml

# Filters
copy config-templates\filters.yml.example accounts\filters.yml
```

**Linux/Mac:**
```bash
mkdir -p accounts

# Session configs
cp config-templates/session_morning.yml.example accounts/session_morning.yml
cp config-templates/session_lunch.yml.example accounts/session_lunch.yml
cp config-templates/session_evening.yml.example accounts/session_evening.yml
cp config-templates/session_extra.yml.example accounts/session_extra.yml

# Strategy configs
cp config-templates/strategy_growth.yml.example accounts/strategy_growth.yml
cp config-templates/strategy_cleanup.yml.example accounts/strategy_cleanup.yml

# Filters
cp config-templates/filters.yml.example accounts/filters.yml
```

### 2. Find your device ID

```bash
# For USB devices (physical phone)
adb devices
# Example output: fbc9d1f30eb2    device

# For emulators (MEmu)
adb connect 127.0.0.1:21533
adb devices
# Example output: 127.0.0.1:21533    device
```

### 3. Update username and device ID

Edit each config file and replace placeholders:
- `YOUR_USERNAME_HERE` → your Instagram username
- `YOUR_DEVICE_ID_HERE` → your device ID

**Quick edit (Linux/Mac):**
```bash
# Replace in all files at once
sed -i 's/YOUR_USERNAME_HERE/maxhaider.dev/g' accounts/*.yml
sed -i 's/YOUR_DEVICE_ID_HERE/fbc9d1f30eb2/g' accounts/*.yml
```

**Quick edit (Windows PowerShell):**
```powershell
Get-ChildItem accounts\*.yml | ForEach-Object {
    (Get-Content $_.FullName) -replace 'YOUR_USERNAME_HERE', 'maxhaider.dev' |
    Set-Content $_.FullName
}
```

### 4. Set up environment variables (optional)

Create `.env` file in project root:
```env
INSTAGRAM_USER_A=your_instagram_username
INSTAGRAM_PASS_A=your_instagram_password
DEVICE=your_device_id
```

**Note**: Username and device in YAML configs override `.env` values.

### 5. Customize for your niche

**Session Configs** (`session_*.yml`):
- Update `hashtag-likers-top` with hashtags relevant to your niche
- Update `blogger-post-likers` with competitor/influencer accounts
- Each session should have different sources for variety

**Example niches:**
- **Backend/DevOps**: python, django, kubernetes, terraform, aws, docker
- **Frontend**: react, nextjs, typescript, webdev, javascript, vuejs
- **Data Science**: datascience, machinelearning, ai, analytics, bigdata
- **Mobile**: flutter, reactnative, ios, android, kotlin, swift

**Strategy Configs** (`strategy_*.yml`):
- Update `blogger-post-likers` with competitors in your niche
- Adjust limits based on account age/activity

**Filters** (`filters.yml`):
- Modify `blacklisted-words` to filter unwanted accounts
- Enable `mandatory-words` to target specific keywords
- Adjust follower ranges for your target audience

---

## Session vs Strategy Configs

### Use Session Configs When:
- Setting up cron/scheduled automation
- Want different content sources at different times
- Building daily routine (morning/lunch/evening)

**Example:**
```bash
# Linux cron
30 9 * * * cd ~/repos/instabot && .venv/bin/python runner.py morning
45 13 * * * cd ~/repos/instabot && .venv/bin/python runner.py lunch
15 18 * * * cd ~/repos/instabot && .venv/bin/python runner.py evening
```

### Use Strategy Configs When:
- Manual runs for specific goals
- Testing different approaches
- One-off growth campaigns

**Example:**
```bash
python runner.py growth    # Daily growth
python runner.py cleanup   # Weekly cleanup
```

---

## Running the Bot

### Test configs:
```bash
# Test individual sessions
python runner.py morning
python runner.py lunch
python runner.py evening
python runner.py extra

# Test strategies
python runner.py growth
python runner.py cleanup
```

### Automate with cron (Linux/Mac):
```bash
# Run morning session at 9:30am daily
30 9 * * * cd ~/repos/instabot && .venv/bin/python runner.py morning >> logs/cron.log 2>&1
```

### Automate with Task Scheduler (Windows):
See `docs/` for Windows Task Scheduler setup.

---

## File Structure After Setup

```
instabot/
├── accounts/
│   ├── maxhaider.dev/         # Account-specific (created by bot)
│   │   └── filter.json        # Account filters
│   ├── session_morning.yml    # Morning session config
│   ├── session_lunch.yml      # Lunch session config
│   ├── session_evening.yml    # Evening session config
│   ├── session_extra.yml      # Extra session config
│   ├── strategy_growth.yml    # Growth strategy
│   ├── strategy_cleanup.yml   # Cleanup strategy
│   └── filters.yml            # Base filters
├── config-templates/          # Templates (this directory)
├── logs/                      # Session logs (gitignored)
└── .env                       # Credentials (gitignored)
```

---

## Security Note

⚠️ **Never commit actual config files** in `accounts/` directory to git. They may contain sensitive device IDs and settings.

The `.gitignore` file protects:
- `accounts/` directory
- `.env` file
- `logs/` directory
- `crashes/` directory

Only these template files (with `.example` extension) should be committed to version control.

---

## Expected Daily Activity

**With 3 session days (Tue/Thu/Sat/Sun):**
- Morning + Lunch + Evening
- ~110-120 interactions
- ~65-75 likes
- ~22-25 follows

**With 4 session days (Mon/Wed/Fri):**
- Morning + Lunch + Extra + Evening
- ~135-150 interactions
- ~80-90 likes
- ~27-30 follows

**Weekly cleanup (Sunday):**
- Unfollows non-mutuals
- Keeps followers and mutuals
- ~5-10 minutes

---

## Customization Tips

### Start Conservative
- Begin with 3 sessions/day
- Monitor for 1 week
- Gradually increase if no issues

### Vary Your Sources
- Different hashtags per session
- Mix hashtags + blogger-post-likers
- Rotate targets weekly

### Adjust for Account Age
**New accounts (< 3 months):**
- Reduce limits by 30-40%
- 2 sessions/day max
- Avoid aggressive following

**Established accounts (> 6 months):**
- Can use template limits as-is
- 3-4 sessions/day safe
- Higher follow percentages OK

---

## Support

- **Full Setup Guide**: `docs/LINUX_USB_DEVICE_SETUP.md` or `docs/SETUP_MEMU.md`
- **Quick Reference**: `docs/LINUX_QUICK_REFERENCE.md`
- **Project Overview**: `README.md`
- **Architecture**: `CLAUDE.md`
