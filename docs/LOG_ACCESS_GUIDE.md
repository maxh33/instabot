# Log Access & Metrics Guide

Complete guide to accessing logs, viewing interaction history, and collecting metrics for your Instagram bot.

## 📁 Log File Locations

### Main Session Logs
**Location**: `logs/maxhaider.dev.log` (replace with your username)
- **Size**: ~40-50KB per session
- **Format**: Timestamped text with DEBUG/INFO/WARNING levels
- **Content**: Real-time session activity, interactions, filter decisions

**Rotated Backups**: `logs/maxhaider.dev.log.1`, `logs/maxhaider.dev.log.2`, etc.

### Task Runner Logs
Different log files for different run modes:
- **Test runs**: `logs/gramaddict_test_like.log`
- **Growth strategy**: `logs/gramaddict_growth.log`
- **Cleanup strategy**: `logs/gramaddict_cleanup.log`

### Structured Data Files
**Location**: `accounts/maxhaider.dev/` (replace with your username)

**Key files**:
1. **`interacted_users.json`** (~100-200KB)
   - Complete interaction history
   - Per-user action details
   - Following status tracking

2. **`sessions.json`** (~20-30KB)
   - Session-level statistics
   - Configuration snapshots
   - Timing and duration data

## 📊 What's in the Logs

### Session Summary (End of Log)
```
-------- FINISH: 19:55:00 - 2025/12/02 --------
TOTAL
Completed sessions: 1
Total duration: 0:07:26
Total interactions: (8) 8 for #fastapi
Successful interactions: (3) 3 for #fastapi
Total followed: (1) 1 for #fastapi
Total likes: 3
Total comments: 0
Total PM sent: 0
Total watched: 0
Total unfollowed: 0
```

### Account Info (Session Start)
```
Hello, @maxhaider.dev! You have 5 followers and 3 followings so far.
```

### Per-Interaction Details
```
@simplify.content: interact
Followed @simplify.content
Session progress: 2 likes, 0 watched, 0 commented, 0 PM sent, 1 followed
```

### Filter Decisions
```
@gideon.akinlade.14: interact
Empty account.
follow_private_or_empty is disabled in filters. Skip.
```

## 🔍 Viewing Logs

### Windows PowerShell Commands

**Watch Live (Real-time Updates)**:
```powershell
Get-Content logs/maxhaider.dev.log -Wait -Tail 50
```

**Last Session Summary**:
```powershell
Get-Content logs/maxhaider.dev.log -Tail 100 | Select-String -Pattern 'TOTAL|Session finished|Completed sessions'
```

**Search for Followed Accounts**:
```powershell
Get-Content logs/maxhaider.dev.log | Select-String -Pattern 'Followed @'
```

**Filter Rejections**:
```powershell
Get-Content logs/maxhaider.dev.log | Select-String -Pattern 'Private account|Empty account|Business account'
```

**Find Specific User Interactions**:
```powershell
Get-Content logs/maxhaider.dev.log | Select-String -Pattern '@username'
```

### Linux/Mac Commands

**Watch live**:
```bash
tail -f logs/maxhaider.dev.log
```

**Last session**:
```bash
tail -100 logs/maxhaider.dev.log | grep -E "TOTAL|Session finished"
```

**Followed accounts**:
```bash
grep "Followed @" logs/maxhaider.dev.log
```

## 📈 Using the Metrics Analyzer

### Quick Summary
```bash
python metrics_analyzer.py maxhaider.dev
```

**Output Example**:
```
============================================================
📊 Instagram Bot Metrics - @maxhaider.dev
============================================================

📈 Overall Statistics:
  Total interactions: 127
  Users followed: 23
  Currently following: 18
  Users unfollowed: 5
  Likes given: 156
  Stories watched: 12

📅 Last 7 Days:
  Sessions: 8
  Interactions: 67
  Success rate: 28.4%
  Avg duration: 6.2 min

🔍 Filter Effectiveness:
  Accounts checked: 67
  Private accounts: 38
  Empty accounts: 9
  Rejection rate: 70.1%

🎯 Top Sources (by interactions):
  #fastapi
    Attempts: 25, Success: 32.0%, Followed: 6
  #python
    Attempts: 18, Success: 27.8%, Followed: 4
```

### Export Metrics to JSON
```bash
python metrics_analyzer.py maxhaider.dev export
```

Creates: `metrics/maxhaider.dev_metrics.json` with complete data export

### List Currently Following
```bash
python metrics_analyzer.py maxhaider.dev followed
```

Shows accounts you're currently following with source and interaction date.

### Source Performance Analysis
```bash
python metrics_analyzer.py maxhaider.dev sources
```

Shows which hashtags/sources are performing best.

## 📋 Interaction History (JSON Data)

### interacted_users.json Structure

```json
{
  "simplify.content": {
    "last_interaction": "2025-12-02 19:53:32",
    "following_status": "following",
    "session_id": "abc123-def456",
    "job_name": "hashtag-likers-top",
    "target": "#fastapi",
    "liked": 1,
    "watched": 0,
    "commented": 0,
    "followed": true,
    "unfollowed": false,
    "pm_sent": false
  }
}
```

**Fields Explained**:
- `following_status`: `"following"`, `"unfollowed"`, or `"none"`
- `target`: Which source (hashtag/account) led to this user
- `liked`: Number of posts liked from this user
- `followed`: Whether you followed this user

### Extracting Data with Python

```python
import json

# Load data
with open('accounts/maxhaider.dev/interacted_users.json', 'r') as f:
    users = json.load(f)

# Get all followed accounts
following = [
    username for username, data in users.items()
    if data.get('following_status') == 'following'
]

print(f"Currently following {len(following)} accounts")

# Get accounts by source
from collections import defaultdict
by_source = defaultdict(list)

for username, data in users.items():
    if data.get('following_status') == 'following':
        source = data.get('target', 'unknown')
        by_source[source].append(username)

for source, accounts in by_source.items():
    print(f"{source}: {len(accounts)} accounts")
```

## 📊 Metrics to Track

### Performance Metrics
1. **Success Rate**: Successful interactions / Total interactions
   - Target: 25-35% (higher = better filtering)
   - Below 20%: Filters too strict or low-quality sources
   - Above 50%: Filters too lenient, potential bot risk

2. **Filter Rejection Rate**: Rejected / Total checked
   - Target: 60-75% (shows healthy filtering)
   - Above 80%: Consider loosening filters
   - Below 50%: Tighten filters to avoid low-quality accounts

3. **Average Session Duration**
   - Target: 5-10 minutes for test sessions
   - Compare to `total-interactions-limit` setting

4. **Likes per User**: Total likes / Users interacted
   - Shows engagement depth
   - Range: 1-3 is typical with current config

### Growth Metrics
1. **Follower Growth Rate**
   - Track from session logs: `You have X followers`
   - Calculate: (New - Old) / Old * 100

2. **Follow-back Rate**
   - Users who followed you back / Users you followed
   - Requires manual tracking or Instagram insights

3. **Retention Rate**
   - Followers after 7 days / Initial followers
   - Indicates quality of targeting

### Source Performance
1. **Best Performing Sources**
   - Which hashtags/accounts yield highest success rate
   - Track with: `python metrics_analyzer.py <username> sources`

2. **Engagement by Source**
   - Likes/follows generated per source
   - Helps optimize target selection

## 🔄 Automated Metrics Collection

### Create Daily Metrics Export (Windows Task Scheduler)

**Script**: `daily_metrics.bat`
```batch
@echo off
cd /d D:\Programacao\Repositorios\instabot
call .venv\Scripts\activate
python metrics_analyzer.py maxhaider.dev export
```

**Schedule**:
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Instagram Bot Daily Metrics"
4. Trigger: Daily at 11:00 PM
5. Action: Start Program
6. Program: `D:\Programacao\Repositorios\instabot\daily_metrics.bat`

### Create Growth Tracking Spreadsheet

**Export follower counts**:
```python
# growth_tracker.py
from metrics_analyzer import MetricsAnalyzer
import csv
from datetime import datetime

analyzer = MetricsAnalyzer("maxhaider.dev")
growth = analyzer.get_follower_growth()

with open(f'growth_{datetime.now():%Y%m%d}.csv', 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['date', 'time', 'followers', 'following', 'posts'])
    writer.writeheader()
    writer.writerows(growth)

print("✓ Growth data exported to CSV")
```

Run weekly: `python growth_tracker.py`

## 📌 Quick Reference

| Task | Command |
|------|---------|
| Watch live logs | `Get-Content logs/maxhaider.dev.log -Wait -Tail 50` |
| View last session | `Get-Content logs/maxhaider.dev.log -Tail 100` |
| Show metrics | `python metrics_analyzer.py maxhaider.dev` |
| Export metrics | `python metrics_analyzer.py maxhaider.dev export` |
| List following | `python metrics_analyzer.py maxhaider.dev followed` |
| Source performance | `python metrics_analyzer.py maxhaider.dev sources` |
| Find user interactions | `Get-Content logs/maxhaider.dev.log \| Select-String '@username'` |

## 🎯 Best Practices

1. **Check logs after each session** to validate bot behavior
2. **Export metrics weekly** to track trends
3. **Monitor rejection rate** - should stay 60-75%
4. **Review followed accounts** regularly to ensure quality
5. **Track follower growth** to measure effectiveness
6. **Analyze source performance** monthly to optimize targeting

## 💡 Tips

- Use `Select-String -Context 3` to see lines before/after matches
- Pipe to `Out-File results.txt` to save search results
- Use `Measure-Object` to count occurrences
- Combine multiple patterns with `-Pattern 'word1|word2|word3'`

## 🚨 Troubleshooting

**Log file not found**:
- Check username matches your Instagram account
- Verify bot has run at least once
- Look in `logs/` directory for UUID-named files

**Empty metrics**:
- Ensure bot completed at least one session
- Check `accounts/<username>/` directory exists
- Verify JSON files are not corrupted

**Old data in metrics**:
- Metrics analyzer reads from JSON files
- JSON files update after each session
- Restart analyzer to reload data
