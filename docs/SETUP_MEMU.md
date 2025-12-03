# MEmu Setup Guide for GramAddict

Official GramAddict recommendation for Windows emulator.

## Installation Steps

1. **Download MEmu**
   - Visit: https://www.memuplay.com/
   - Download latest version (MEmu 9.x recommended)
   - Install with default settings

2. **Configure MEmu for Automation**
   - Open MEmu Multi-Instance Manager
   - Create new Android instance:
     - **Android Version**: Android 7.1 (Nougat) or Android 9 (Pie)
     - **CPU cores**: 2-4 (depending on your system)
     - **RAM**: 2048-4096 MB
     - **Resolution**: 720x1280 or 1080x1920

3. **Enable ADB in MEmu**
   - Start the MEmu instance
   - Click Settings (gear icon) in MEmu sidebar
   - Go to "General" tab
   - Enable "ADB debugging" checkbox
   - Note the ADB port (usually 21503 for first instance)

4. **Connect via ADB**
   ```bash
   # Kill any existing ADB server
   adb kill-server
   adb start-server

   # Connect to MEmu (default port 21503)
   adb connect 127.0.0.1:21503

   # Verify connection
   adb devices
   # Should show: 127.0.0.1:21503   device
   ```

5. **Update .env File**
   ```
   INSTAGRAM_USER_A=your_username
   INSTAGRAM_PASS_A=your_password
   DEVICE_ID_A=127.0.0.1:21503
   ```

6. **Install Instagram on MEmu**
   - Open Play Store in MEmu
   - Sign in with Google account
   - Install Instagram
   - Log in with your Instagram credentials

7. **Run GramAddict Test**
   ```bash
   python test_like_hashtag.py
   ```

## MEmu Multi-Instance Ports

If running multiple MEmu instances for multi-account automation:
- Instance 1: `127.0.0.1:21503`
- Instance 2: `127.0.0.1:21513`
- Instance 3: `127.0.0.1:21523`
- Pattern: increment by 10 for each instance

## Troubleshooting

**Issue**: ADB connection refused
- **Fix**: Restart MEmu, enable ADB debugging again

**Issue**: UIAutomator2 installation fails
- **Fix**: Use Android 7.1 (Nougat) instead of newer versions
- Better UIAutomator2 compatibility with older Android

**Issue**: Instagram crashes on open
- **Fix**: Increase RAM allocation to 3072-4096 MB in MEmu settings

## Why MEmu?

- Official GramAddict documentation recommendation
- Better UIAutomator2 stability than BlueStacks
- Supports both Intel and AMD CPUs
- No active interference with automation services
- Community-validated for Instagram automation (2024)

## Sources
- [GramAddict Docs](https://docs.gramaddict.org/)
- [UIAutomator2 Emulator Support](https://github.com/hansalemaos/cyandroemu)
