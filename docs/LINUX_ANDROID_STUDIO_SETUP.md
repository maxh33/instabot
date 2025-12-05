# Linux Android Studio Emulator Setup Guide

Complete guide for setting up Instagram bot on Linux with Android Studio emulator and cron scheduling.

## Overview

This guide will help you:
1. Install Android Studio on Linux
2. Create Android 7.1.2 (API 25) emulator
3. Install Instagram v300
4. Deploy the bot with automated scheduling
5. Monitor and maintain the system

**Target Configuration:**
- **OS**: Ubuntu/Debian Linux
- **Emulator**: Android Studio AVD (Android 7.1.2 API 25 x86)
- **Instagram**: v300.0.0.29.110
- **Scheduler**: Cron with randomization
- **Device ID**: emulator-5554

---

## Part 1: Install Android Studio

### 1.1 Download and Install

```bash
# Download Android Studio for Linux
cd ~/Downloads
wget https://redirector.gvt1.com/edgedl/android/studio/ide-zips/2023.3.1.18/android-studio-2023.3.1.18-linux.tar.gz

# Extract to /opt/
sudo tar -xzf android-studio-*.tar.gz -C /opt/

# Create symbolic link (optional)
sudo ln -s /opt/android-studio/bin/studio.sh /usr/local/bin/android-studio
```

### 1.2 Add to PATH

Edit `~/.bashrc` or `~/.zshrc`:

```bash
# Android Studio and SDK paths
export ANDROID_SDK_ROOT=$HOME/Android/Sdk
export PATH=$PATH:/opt/android-studio/bin
export PATH=$PATH:$ANDROID_SDK_ROOT/emulator
export PATH=$PATH:$ANDROID_SDK_ROOT/platform-tools
export PATH=$PATH:$ANDROID_SDK_ROOT/tools/bin
```

Apply changes:

```bash
source ~/.bashrc
```

### 1.3 Install Required Dependencies

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install -y \
    libc6:i386 \
    libncurses5:i386 \
    libstdc++6:i386 \
    lib32z1 \
    libbz2-1.0:i386 \
    libgl1-mesa-dev \
    libglu1-mesa \
    libxrandr2 \
    libxss1 \
    libxcursor1 \
    libxcomposite1 \
    libasound2 \
    libxi6 \
    libxtst6

# Fedora/RHEL
sudo dnf install -y \
    zlib.i686 \
    ncurses-libs.i686 \
    bzip2-libs.i686 \
    mesa-libGL \
    mesa-libGLU
```

---

## Part 2: Install SDK Components

### 2.1 Launch Android Studio

```bash
# First time setup
studio.sh
# or
android-studio
```

Complete the initial setup wizard:
1. Choose "Standard" installation
2. Select theme (Light/Dark)
3. Wait for SDK components to download

### 2.2 Install Required SDK Components

Open SDK Manager: **Tools → SDK Manager**

**SDK Platforms** tab:
- ✅ Android 7.1.2 (Nougat) - API Level 25

**SDK Tools** tab:
- ✅ Android SDK Build-Tools
- ✅ Android Emulator
- ✅ Android SDK Platform-Tools
- ✅ Intel x86 Emulator Accelerator (HAXM) - if using Intel CPU
- ✅ Google Play services

Click "Apply" and wait for downloads.

### 2.3 Install via Command Line (Alternative)

```bash
# List available packages
sdkmanager --list

# Install Android 7.1.2 (API 25) system image
sdkmanager "system-images;android-25;google_apis;x86"

# Install additional tools
sdkmanager "platform-tools" "emulator" "build-tools;30.0.3"

# Accept licenses
sdkmanager --licenses
```

---

## Part 3: Create Android Virtual Device (AVD)

### 3.1 Via Command Line (Recommended)

```bash
# List available system images
avdmanager list

# Create AVD
# IMPORTANT: Use Pixel 1 (not Pixel 2) - Pixel 2 requires API 28+
avdmanager create avd \
  --name Pixel1 \
  --package "system-images;android-25;google_apis_playstore;x86" \
  --device "pixel" \
  --abi "x86"

# Verify creation
avdmanager list avd
```

### 3.2 Via Android Studio GUI

1. Open **Tools → Device Manager**
2. Click "Create Virtual Device"
3. Select **Pixel** (NOT Pixel 2 - that requires API 28+) hardware profile → Next
4. Select **Android 7.1.2 (API 25)** system image → Next
5. Configure AVD:
   - Name: `Pixel1`
   - Startup orientation: Portrait
   - Advanced Settings:
     - RAM: 2048 MB
     - VM heap: 256 MB
     - Internal Storage: 4096 MB
6. Finish

**Note**: Pixel 2 only supports API 28+. For API 25 (Android 7.1.2), use Pixel 1.

### 3.3 Optimize AVD Configuration

Edit `~/.android/avd/Pixel1.avd/config.ini`:

```ini
# Performance settings
hw.ramSize=2048
hw.gpu.enabled=yes
hw.gpu.mode=host
disk.dataPartition.size=4G
vm.heapSize=256

# Disable unnecessary features
hw.audioInput=no
hw.audioOutput=no
hw.camera.back=none
hw.camera.front=none
showDeviceFrame=no
```

---

## Part 4: Install Instagram v300

### 4.1 Start Emulator

```bash
# Start emulator (with GUI for initial setup)
emulator -avd Pixel1

# Or headless mode (for server use)
emulator -avd Pixel1 -no-window -no-audio -no-boot-anim
```

Wait for boot completion (watch for home screen).

### 4.2 Verify Device Connection

```bash
# Check connected devices
adb devices

# Should show:
# List of devices attached
# emulator-5554    device
```

### 4.3 Install Instagram APK

```bash
# Navigate to APK location
cd ~/Downloads  # or wherever you have the APK

# Install Instagram v300
adb install instagram_300_0_0_29_110.apk

# Verify installation
adb shell pm list packages | grep instagram
```

**Expected output:**
```
package:com.instagram.android
```

### 4.4 Login to Instagram

1. Open Instagram on emulator
2. Login with your credentials
3. Complete any 2FA verification
4. **Important**: Keep app logged in
5. Test that app works properly

### 4.5 Keep Emulator Running

For production use, keep emulator running 24/7:

```bash
# Start headless emulator in background
nohup emulator -avd Pixel1 -no-window -no-audio -no-boot-anim > /dev/null 2>&1 &

# Check it's running
adb devices
```

**Pro tip**: Use `screen` or `tmux` to keep emulator running even after logout:

```bash
# Start screen session
screen -S emulator

# Start emulator
emulator -avd Pixel1 -no-window

# Detach: Ctrl+A, then D
# Reattach later: screen -r emulator
```

---

## Part 5: Deploy Instagram Bot

### 5.1 Clone Repository

```bash
# Clone repo
cd ~
git clone <repository-url> instabot
cd instabot
```

### 5.2 Setup Python Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Note: If using uv package manager:
# uv pip install -r requirements.txt
# This automatically handles setuptools dependency for pkg_resources
```

**Python 3.13 Note**: The project uses `packaging>=24.0` which is compatible with Python 3.13 (no distutils dependency). If you encounter `ModuleNotFoundError: No module named 'pkg_resources'`, install setuptools: `pip install setuptools`

### 5.3 Configure Environment

Create `.env` file:

```bash
nano .env
```

Add credentials:

```env
# Instagram Credentials
INSTAGRAM_USER_A=your_username
INSTAGRAM_PASS_A=your_password

# Device Configuration
DEVICE=emulator-5554
```

Save and exit (Ctrl+X, Y, Enter).

### 5.4 Update Scheduler Paths

Edit `scheduler.sh`:

```bash
nano scheduler.sh
```

Update these lines:

```bash
PROJECT_DIR="/home/youruser/instabot"  # CHANGE THIS
EMULATOR_NAME="Pixel1"                 # Verify this matches your AVD name
```

Save and exit.

Edit `install_cron.sh`:

```bash
nano install_cron.sh
```

Update:

```bash
PROJECT_DIR="/home/youruser/instabot"  # CHANGE THIS
```

Save and exit.

### 5.5 Make Scripts Executable

```bash
chmod +x scheduler.sh
chmod +x install_cron.sh
chmod +x randomizer.py
```

---

## Part 6: Test Manual Execution

Before setting up cron, test manually:

### 6.1 Test Emulator Startup

```bash
# Start emulator if not running
emulator -avd Pixel1 -no-window &

# Wait 30 seconds for boot
sleep 30

# Verify device
adb devices
```

### 6.2 Test Bot Execution

```bash
# Activate venv
source .venv/bin/activate

# Test morning session
python3 runner.py morning
```

**Expected behavior:**
- Bot starts and opens Instagram
- Performs ~50 interactions over 45-60 minutes
- Session completes successfully
- Check logs: `tail -f logs/gramaddict_morning.log`

### 6.3 Test Scheduler Script

```bash
# Test scheduler
./scheduler.sh
```

**Expected behavior:**
- Checks if emulator is running (starts if needed)
- Selects session based on current time
- Runs bot session
- Creates log in `logs/scheduler/`

Check scheduler log:

```bash
tail -f logs/scheduler/scheduler_$(date +%Y%m%d).log
```

---

## Part 7: Install Cron Scheduling

### 7.1 Install Cron Jobs

```bash
# Run installation script
./install_cron.sh
```

**Expected output:**
```
Cron jobs installed successfully!
View with: crontab -l
```

### 7.2 Verify Cron Installation

```bash
# View installed cron jobs
crontab -l
```

**Expected output:**
```
# Instagram Bot Scheduler - Randomized Times
# Morning session: 9:30am ±30 min
0 9 * * * /home/youruser/instabot/scheduler.sh >> /home/youruser/instabot/logs/cron.log 2>&1
15 9 * * * /home/youruser/instabot/scheduler.sh >> /home/youruser/instabot/logs/cron.log 2>&1
...
```

### 7.3 Monitor Cron Execution

```bash
# Watch cron log
tail -f logs/cron.log

# Watch scheduler log
tail -f logs/scheduler/scheduler_$(date +%Y%m%d).log

# Watch bot session log
tail -f logs/gramaddict_morning.log  # or lunch/evening/extra
```

---

## Part 8: Optional Advanced Randomization

For even better randomization, use `randomizer.py` with the `at` command.

### 8.1 Install 'at' Command

```bash
# Ubuntu/Debian
sudo apt install at

# Start atd service
sudo systemctl start atd
sudo systemctl enable atd
```

### 8.2 Update randomizer.py Path

```bash
nano randomizer.py
```

Update:

```python
PROJECT_DIR = "/home/youruser/instabot"  # CHANGE THIS
```

### 8.3 Install Daily Randomizer Cron

```bash
# Edit crontab
crontab -e

# Add this line (runs at midnight daily)
0 0 * * * cd /home/youruser/instabot && python3 randomizer.py >> logs/randomizer.log 2>&1
```

This will:
1. Run at midnight each day
2. Decide how many sessions (3-5) for that day
3. Schedule each session with random times using `at` command
4. Provide ±30-45 min variance

---

## Part 9: Monitoring & Maintenance

### 9.1 Daily Monitoring

```bash
# Check if emulator is running
adb devices

# Check if bot is running
ps aux | grep gramaddict

# View today's scheduler log
tail -f logs/scheduler/scheduler_$(date +%Y%m%d).log

# Check metrics
python3 metrics_analyzer.py your_username
```

### 9.2 Weekly Maintenance

```bash
# Review logs for errors
grep -i "error\|warning\|fail" logs/scheduler/*.log

# Check disk space
df -h

# Clean old logs (keep last 30 days)
find logs/scheduler -name "*.log" -mtime +30 -delete

# Review metrics
python3 metrics_analyzer.py your_username sources
```

### 9.3 Troubleshooting

**Emulator won't start:**
```bash
# Check if KVM is enabled (Intel)
lsmod | grep kvm

# Check if emulator process exists
ps aux | grep emulator

# Kill stuck emulator
adb kill-server
killall qemu-system-x86_64

# Restart emulator
emulator -avd Pixel1 -no-window &
```

**Bot not running:**
```bash
# Check lock file
cat /tmp/instabot.lock

# Remove stale lock if needed
rm /tmp/instabot.lock

# Check cron status
systemctl status cron

# View cron logs
grep CRON /var/log/syslog
```

**Instagram not opening:**
```bash
# Verify Instagram is installed
adb shell pm list packages | grep instagram

# Check if app is logged in
adb shell am start -n com.instagram.android/.activity.MainTabActivity

# Reinstall if needed
adb install -r instagram_300_0_0_29_110.apk
```

---

## Part 10: Production Checklist

Before going live, verify:

- [ ] Android Studio installed
- [ ] SDK components downloaded (API 25)
- [ ] AVD created (Pixel1)
- [ ] Emulator starts successfully
- [ ] Instagram v300 installed and logged in
- [ ] Repository cloned
- [ ] Python venv created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured with credentials
- [ ] `scheduler.sh` paths updated
- [ ] `install_cron.sh` paths updated
- [ ] Scripts made executable (`chmod +x`)
- [ ] Manual bot test successful
- [ ] Scheduler test successful
- [ ] Cron jobs installed
- [ ] Logs directory created (`logs/scheduler/`)
- [ ] Monitoring commands tested

---

## Part 11: Performance & Safety

### 11.1 Expected Daily Statistics

**With 3 sessions/day:**
- Total interactions: 150/day
- Total likes: ~110/day
- Total follows: ~37/day
- Total time: ~2h30m-3h/day

**With 4-5 sessions/day (20% of time):**
- Total interactions: 185-220/day
- Total time: ~3h-3h30m/day

### 11.2 Safety Recommendations

**First Week:**
- Run only 3 sessions/day
- Monitor for Instagram warnings
- Check success rate (should be 25-35%)
- Adjust filters if rejection rate too high

**After First Week:**
- Enable 4-5 session days (optional extra sessions)
- Gradually increase limits if needed
- Continue monitoring daily

**Red Flags:**
- Action blocked messages
- Login challenges
- Sudden follower drops
- High rejection rate (>80%)

**If Blocked:**
1. Immediately stop all sessions (`crontab -e` and comment out jobs)
2. Wait 48 hours
3. Restart with 2 sessions/day for 1 week
4. Gradually scale back up

---

## Part 12: Backup & Recovery

### 12.1 Backup Important Data

```bash
# Backup account data
tar -czf backup_$(date +%Y%m%d).tar.gz accounts/ logs/ .env

# Backup AVD
cp -r ~/.android/avd/Pixel1.avd/ ~/avd_backup/
```

### 12.2 Recovery

```bash
# Restore account data
tar -xzf backup_20241203.tar.gz

# Restore AVD
cp -r ~/avd_backup/Pixel1.avd/ ~/.android/avd/
```

---

## Summary

You now have:
- ✅ Android Studio emulator running on Linux
- ✅ Instagram v300 installed and logged in
- ✅ Bot configured with Brazilian peak time scheduling
- ✅ Cron jobs with randomization
- ✅ Automated emulator management
- ✅ Lock file protection against overlaps
- ✅ Comprehensive logging and monitoring

**Next Steps:**
1. Monitor first 3 days closely
2. Check metrics weekly
3. Adjust limits based on account growth
4. Scale up gradually after first week

**Support:**
- Check logs first: `logs/scheduler/`, `logs/gramaddict_*.log`
- Review metrics: `python3 metrics_analyzer.py your_username`
- Test manually: `./scheduler.sh` or `python3 runner.py morning`

Good luck with your Instagram growth! 🚀
