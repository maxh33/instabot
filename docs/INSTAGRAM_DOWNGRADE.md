# Downgrade Instagram on MEmu

GramAddict v3.2.12 is tested with Instagram 300.0.0.29.110. Newer versions (like 408.0) have UI changes that cause crashes.

## Method 1: APKMirror (Recommended)

1. **Download Instagram 300.0.0.29.110 APK**
   - Visit: https://www.apkmirror.com/apk/instagram/instagram-instagram/
   - Search for version 300.0.0.29.110
   - Download the APK file to your computer

2. **Uninstall Current Instagram on MEmu**
   - Open MEmu emulator
   - Long-press Instagram app icon
   - Drag to "Uninstall" or click uninstall

3. **Install Old Version via ADB**
   ```bash
   # From your computer (replace with actual APK path)
   adb connect 127.0.0.1:21533
   adb install "path/to/Instagram_300.0.0.29.110.apk"
   ```

4. **Disable Auto-Updates**
   - Open Play Store on MEmu
   - Search for Instagram
   - Tap Instagram → ⋮ (three dots) → Uncheck "Enable auto-update"

5. **Re-run Test**
   ```bash
   python test_like_hashtag.py
   ```

## Method 2: Play Store Version Control

If APKMirror download doesn't work:

1. Search for "Instagram old version APK" sites
2. Look specifically for version 300.0.0.29.110
3. Ensure APK is from reputable source (APKPure, APKMirror, Uptodown)

## Verification

After installing the old version, check in Instagram:
- Settings → About → Version should show **300.0.0.29.110**

## Security Note

Only download APKs from trusted sources:
- ✅ APKMirror.com (most reputable)
- ✅ APKPure.com
- ✅ Uptodown.com
- ❌ Random websites

## Alternative: Update GramAddict

If you prefer to keep Instagram 408.0, check for newer GramAddict versions:
```bash
pip install --upgrade gramaddict
```

Check releases: https://github.com/GramAddict/bot/releases
