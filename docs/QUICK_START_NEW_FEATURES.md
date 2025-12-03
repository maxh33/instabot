# Quick Start - New Features

## ✅ Your Setup is Ready!

All new features tested and working:
- ✅ Device Manager (USB device detected)
- ✅ Metrics Analyzer (280 interactions tracked)
- ✅ MEmu Support (ready to use)

---

## 🚀 3 Things You Can Do Right Now

### 1. View Your Metrics

```bash
python metrics_analyzer.py maxhaider.dev
```

**What you'll see**:
- Total interactions and success rate
- Filter effectiveness
- Best performing sources
- 7-day session summary

### 2. Check Your Logs

```powershell
# Watch last 50 lines
Get-Content logs/maxhaider.dev.log -Tail 50

# Find followed accounts
Get-Content logs/maxhaider.dev.log | Select-String -Pattern 'Followed @'

# See filter decisions
Get-Content logs/maxhaider.dev.log | Select-String -Pattern 'Private account|Empty account'
```

### 3. Test MEmu (Optional)

**If you want to add MEmu emulator**:

```bash
# Connect to MEmu
adb connect 127.0.0.1:21503

# Test connection
python device_manager.py

# Run test
python test_like.py --device 127.0.0.1:21503
```

---

## 📊 Current Statistics (from test)

**Your Bot Activity**:
- Total Interactions: **280**
- Sessions (Last 7 Days): **7**
- Sources Tracked: **4**

Run `python metrics_analyzer.py maxhaider.dev` for full breakdown!

---

## 📖 Documentation Reference

| What You Want | Where to Look |
|---------------|---------------|
| MEmu emulator setup | `docs/MEMU_SETUP_EXAMPLE.md` |
| Log access commands | `docs/LOG_ACCESS_GUIDE.md` |
| Metrics analysis | Run `python metrics_analyzer.py maxhaider.dev` |
| Custom metrics | See `example_metrics_script.py` |
| All new features | `docs/NEW_FEATURES_SUMMARY.md` |

---

## 🎯 Recommended Next Steps

### 1. Analyze Performance (5 min)

```bash
# View full report
python metrics_analyzer.py maxhaider.dev

# Export to JSON
python metrics_analyzer.py maxhaider.dev export

# Check source performance
python metrics_analyzer.py maxhaider.dev sources
```

**Use this to**:
- Identify best hashtags/sources
- See filter effectiveness
- Track growth trends

### 2. Optimize Targeting (10 min)

Based on metrics, update your configs:

```yaml
# If #fastapi has 32% success rate but #python only 15%:
hashtag-likers-top: [fastapi, django]  # Remove underperforming
```

### 3. Set Up MEmu (Optional, 20 min)

**Only if you want multi-account**:

1. Follow `docs/MEMU_SETUP_EXAMPLE.md`
2. Install Instagram on MEmu
3. Test: `python test_like.py --device 127.0.0.1:21503`

---

## 💡 Pro Tips

### Metrics Best Practices

1. **Export weekly**:
   ```bash
   python metrics_analyzer.py maxhaider.dev export
   ```

2. **Monitor rejection rate**:
   - Target: 60-75%
   - Too high: Loosen filters
   - Too low: Tighten filters

3. **Track sources**:
   ```bash
   python metrics_analyzer.py maxhaider.dev sources
   ```
   Remove sources with <20% success rate

### Log Monitoring

**After each session**:
```powershell
# Quick check
Get-Content logs/maxhaider.dev.log -Tail 100 | Select-String -Pattern 'TOTAL'
```

**Find issues**:
```powershell
Get-Content logs/maxhaider.dev.log | Select-String -Pattern 'ERROR|CRITICAL'
```

### Device Switching

**Switch between devices**:
```bash
# Physical device
python test_like.py --device fbc9d1f30eb2

# MEmu
python test_like.py --device 127.0.0.1:21503
```

---

## 🔄 Daily Workflow

### Morning Routine (2 min)

```bash
# Check yesterday's metrics
python metrics_analyzer.py maxhaider.dev

# Run test session
python test_like.py
```

### Weekly Review (10 min)

```bash
# Export metrics
python metrics_analyzer.py maxhaider.dev export

# Check source performance
python metrics_analyzer.py maxhaider.dev sources

# Review logs for issues
Get-Content logs/maxhaider.dev.log -Tail 500 | Select-String -Pattern 'ERROR|WARNING'
```

### Monthly Optimization (30 min)

1. **Analyze 30-day metrics**
2. **Update target sources** based on performance
3. **Adjust filters** if rejection rate off-target
4. **Review followed accounts** quality

---

## 🆘 Need Help?

### Device Issues
```bash
# Test device connection
python device_manager.py

# Should show your device(s)
# If not, check ADB connection
```

### Metrics Issues
```bash
# Verify data exists
dir accounts\maxhaider.dev\

# Should see:
# - interacted_users.json
# - sessions.json
```

### Log Issues
```bash
# Verify log file
dir logs\maxhaider.dev.log

# If missing, run a test session first
```

---

## ✅ You're All Set!

Everything is working. Start with:

```bash
# View your metrics
python metrics_analyzer.py maxhaider.dev

# Then check logs
Get-Content logs/maxhaider.dev.log -Tail 100

# Run a new session
python test_like.py
```

Happy automating! 🎉
