# MEmu Emulator Setup Guide

Step-by-step guide to set up MEmu Android emulator for Instagram automation alongside your physical device.

## Why Use MEmu?

- **Multi-account support**: Run multiple Instagram accounts simultaneously
- **Official GramAddict recommendation**: Most compatible emulator
- **No physical device needed**: Can run on your computer 24/7
- **Easy automation**: Network ADB connection

## Installation

### 1. Download and Install MEmu

Download from: https://www.memuplay.com/

**Recommended Settings**:
- Android version: 7.1 (best compatibility with Instagram)
- CPU: 2 cores
- RAM: 2048MB (2GB)
- Resolution: 720x1280 (Instagram optimized)

### 2. Enable ADB in MEmu

**Method 1: From MEmu Settings**
1. Open MEmu
2. Click the gear icon (Settings)
3. Go to "Advanced" tab
4. Enable "ADB debugging"
5. Note the ADB port (usually 21503, 21513, or 21523)

**Method 2: From Multi-MEmu Manager**
1. Open Multi-MEmu (for multiple instances)
2. Create new instance or edit existing
3. Enable ADB debugging
4. Assign unique port (21503, 21513, 21523, etc.)

### 3. Connect via ADB

```bash
# Connect to MEmu instance (default port: 21503)
adb connect 127.0.0.1:21503

# Verify connection
adb devices
# Should show: 127.0.0.1:21503    device
```

### 4. Install Instagram

**Option A: Google Play Store**
1. Open Play Store in MEmu
2. Sign in with Google account
3. Search and install Instagram
4. Login to your Instagram account

**Option B: APK Install (Recommended)**
```bash
# Install Instagram v313 (tested version)
adb -s 127.0.0.1:21503 install instagram313.apk

# Launch Instagram
adb -s 127.0.0.1:21503 shell am start -n com.instagram.android/.activity.MainTabActivity
```

## Multi-Instance Setup

### Creating Multiple MEmu Instances

1. **Open Multi-MEmu Manager**
2. **Click "Create" or "Clone"**
   - Clone: Copy existing setup (faster)
   - Create: Fresh instance
3. **Configure Each Instance**:
   - Name: "Instagram_Account_A", "Instagram_Account_B", etc.
   - Android version: 7.1
   - Memory: 2GB each
   - Unique ADB port

**Default Ports**:
- Instance 1: 21503
- Instance 2: 21513
- Instance 3: 21523
- Pattern: 21503 + (instance_number - 1) * 10

### Configure .env for Multiple Accounts

```env
# Physical Device (Account A)
INSTAGRAM_USER_A=account_a_username
INSTAGRAM_PASS_A=account_a_password
DEVICE_A=fbc9d1f30eb2

# MEmu Instance 1 (Account B)
INSTAGRAM_USER_B=account_b_username
INSTAGRAM_PASS_B=account_b_password
DEVICE_B=127.0.0.1:21503

# MEmu Instance 2 (Account C)
INSTAGRAM_USER_C=account_c_username
INSTAGRAM_PASS_C=account_c_password
DEVICE_C=127.0.0.1:21513
```

## Running the Bot with MEmu

### Test Run with MEmu

```bash
# Using device from .env (DEVICE_B)
python test_like.py --account B

# Or specify device directly
python test_like.py --device 127.0.0.1:21503
```

### Production Run with MEmu

**Option 1: Update config files**
Edit `accounts/strategy_growth.yml`:
```yaml
device: 127.0.0.1:21503  # Change to your MEmu port
```

Then run:
```bash
python runner.py growth
```

**Option 2: Use device manager**
```python
# Create separate configs for each device
# accounts/strategy_growth_memu.yml
device: 127.0.0.1:21503

# Run with specific config
gramaddict run --config accounts/strategy_growth_memu.yml
```

## Testing Device Connection

```bash
# Test device manager
python device_manager.py

# Should show:
# === Device Manager Test ===
# ✓ ADB is available
# Connected devices: 2
#   - fbc9d1f30eb2 (usb)
#   - 127.0.0.1:21503 (network)
# Device from .env: fbc9d1f30eb2
#   Type: usb
#   Connected: True
```

## Switching Between Devices

### Quick Device Switch

**Edit .env**:
```env
# Comment out USB, uncomment MEmu
# DEVICE=fbc9d1f30eb2  # Physical device
DEVICE=127.0.0.1:21503  # MEmu emulator
```

Then run normally:
```bash
python test_like.py
```

### Run Both Simultaneously

**Terminal 1 (Physical Device)**:
```bash
python test_like.py --device fbc9d1f30eb2
```

**Terminal 2 (MEmu)**:
```bash
python test_like.py --device 127.0.0.1:21503
```

## Troubleshooting

### MEmu Not Detected

**Problem**: `adb devices` doesn't show MEmu
**Solutions**:
1. Restart MEmu
2. Disable/re-enable ADB in MEmu settings
3. Try `adb kill-server` then `adb start-server`
4. Check Windows Firewall isn't blocking ADB
5. Verify port in Multi-MEmu settings

### Connection Lost

**Problem**: Device shows "offline" or disconnects
**Solution**:
```bash
# Disconnect and reconnect
adb disconnect 127.0.0.1:21503
adb connect 127.0.0.1:21503

# Verify
adb devices
```

### Instagram Crashes in MEmu

**Problem**: Instagram crashes or won't open
**Solutions**:
1. **Lower Graphics Settings**:
   - MEmu Settings → Advanced → Graphics
   - Change to "DirectX" or "OpenGL"
   - Lower to 720x1280 resolution

2. **Increase RAM**:
   - MEmu Settings → Advanced
   - Increase RAM to 3072MB (3GB)

3. **Reinstall Instagram**:
   ```bash
   adb -s 127.0.0.1:21503 uninstall com.instagram.android
   adb -s 127.0.0.1:21503 install instagram313.apk
   ```

### Wrong ADB Port

**Problem**: Can't determine MEmu port
**How to find**:
1. Open Multi-MEmu Manager
2. Right-click instance → "Settings"
3. Go to "Advanced" tab
4. Check "ADB port" field

Or use netstat:
```bash
netstat -ano | findstr "21503"
```

### Multiple ADB Servers

**Problem**: Conflicts between Android Studio and MEmu ADB
**Solution**:
```bash
# Kill all ADB servers
adb kill-server

# Restart with MEmu's ADB path
# Usually: C:\Program Files\Microvirt\MEmu\adb.exe
cd "C:\Program Files\Microvirt\MEmu"
adb.exe start-server
adb.exe devices
```

## Performance Tips

### Optimize MEmu for Bot

1. **Disable Unnecessary Features**:
   - Settings → Display → Disable "Show FPS"
   - Settings → Display → Disable "Enable keyboard"

2. **CPU Priority**:
   - MEmu Settings → Advanced → Engine
   - Select "High priority"

3. **Close Other Apps in MEmu**:
   - Only keep Instagram running
   - Disable Google services if not needed

### Run MEmu in Background

1. **Minimize MEmu**:
   - Click minimize button
   - MEmu continues running in background

2. **Headless Mode** (Advanced):
   ```bash
   # Start MEmu without UI (requires MEmu Pro)
   "C:\Program Files\Microvirt\MEmu\MEmu.exe" -v -i 0
   ```

## Best Practices

### For Multi-Account Setup

1. **One Account per Instance**: Don't switch accounts in same instance
2. **Separate Configs**: Create `strategy_growth_A.yml`, `strategy_growth_B.yml`
3. **Stagger Sessions**: Don't run all bots at same time
4. **Monitor Resources**: Each instance uses ~2GB RAM

### Device Organization

```
Physical Device (USB)
├── Account A (main)
└── DEVICE=fbc9d1f30eb2

MEmu Instance 1 (Port 21503)
├── Account B (growth)
└── DEVICE=127.0.0.1:21503

MEmu Instance 2 (Port 21513)
├── Account C (testing)
└── DEVICE=127.0.0.1:21513
```

### Safety

1. **Different IPs**: Use VPN/proxy for different accounts on same machine
2. **Different Times**: Run sessions at different times
3. **Realistic Limits**: Lower limits for emulator accounts
4. **Unique Devices**: Use different Android versions/resolutions if possible

## Quick Reference

| Task | Command |
|------|---------|
| Connect MEmu | `adb connect 127.0.0.1:21503` |
| Disconnect MEmu | `adb disconnect 127.0.0.1:21503` |
| List devices | `adb devices` |
| Test device manager | `python device_manager.py` |
| Run on MEmu | `python test_like.py --device 127.0.0.1:21503` |
| Install Instagram | `adb -s 127.0.0.1:21503 install instagram313.apk` |
| Launch Instagram | `adb -s 127.0.0.1:21503 shell am start -n com.instagram.android/.activity.MainTabActivity` |

## Resources

- [MEmu Official Site](https://www.memuplay.com/)
- [GramAddict Documentation](https://docs.gramaddict.org/)
- [Android ADB Guide](https://developer.android.com/studio/command-line/adb)
