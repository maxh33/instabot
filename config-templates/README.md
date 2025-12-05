# Config Templates

This directory contains template configuration files for the Instagram bot.

## Setup Instructions

### 1. Copy templates to accounts directory

```bash
# Create accounts directory if it doesn't exist
mkdir accounts

# Copy template files (remove .example extension)
cp config-templates/filters.yml.example accounts/filters.yml
cp config-templates/strategy_growth.yml.example accounts/strategy_growth.yml
cp config-templates/strategy_cleanup.yml.example accounts/strategy_cleanup.yml
```

### 2. Configure your device ID

Find your device ID:
```bash
# For USB devices (physical phone)
adb devices
# Example output: fbc9d1f30eb2    device

# For emulators (MEmu)
adb connect 127.0.0.1:21533
adb devices
# Example output: 127.0.0.1:21533    device
```

Edit the copied files and replace `YOUR_DEVICE_ID_HERE` with your actual device ID.

### 3. Set up environment variables

Create a `.env` file in the project root:
```bash
INSTAGRAM_USER_A=your_instagram_username
INSTAGRAM_PASS_A=your_instagram_password
DEVICE=your_device_id
```

### 4. Customize for your niche

**Growth Strategy** (`accounts/strategy_growth.yml`):
- Update `blogger-post-likers` with competitor accounts in your niche
- Adjust interaction limits based on your account age/activity

**Filters** (`accounts/filters.yml`):
- Modify `blacklisted-words` to filter out unwanted accounts
- Enable `mandatory-words` if you want to target specific keywords in bios

**Cleanup Strategy** (`accounts/strategy_cleanup.yml`):
- Add important accounts to the `whitelist` to protect them from unfollowing

## File Descriptions

- **filters.yml.example** - Global filters for skipping unwanted accounts
- **strategy_growth.yml.example** - Daily growth automation (follow/like)
- **strategy_cleanup.yml.example** - Weekly cleanup (unfollow non-followers)

## Security Note

⚠️ **Never commit the actual config files** in `accounts/` directory to git. They contain your device ID and potentially sensitive settings. The `.gitignore` file is configured to ignore the entire `accounts/` directory.

Only these template files (with `.example` extension) should be committed to version control.