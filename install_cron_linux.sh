#!/bin/bash
# Install cron jobs for Instagram bot on Linux
# Supports both USB devices and emulators

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="$HOME/repos/instabot"
PYTHON_BIN="$PROJECT_DIR/.venv/bin/python"
LOG_DIR="$PROJECT_DIR/logs"

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Instagram Bot - Cron Installation${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo -e "${RED}ERROR: Project directory not found at $PROJECT_DIR${NC}"
    echo "Please update PROJECT_DIR in this script."
    exit 1
fi

# Check if Python venv exists
if [ ! -f "$PYTHON_BIN" ]; then
    echo -e "${RED}ERROR: Python virtual environment not found${NC}"
    echo "Expected: $PYTHON_BIN"
    echo "Run: python3.11 -m venv .venv"
    exit 1
fi

# Check Python version (should be 3.11)
PYTHON_VERSION=$($PYTHON_BIN --version 2>&1 | cut -d' ' -f2 | cut -d'.' -f1-2)
if [ "$PYTHON_VERSION" != "3.11" ]; then
    echo -e "${YELLOW}WARNING: Python version is $PYTHON_VERSION (recommended: 3.11)${NC}"
    echo "GramAddict v3.2.12 may crash on Python 3.13+"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Backup existing crontab
BACKUP_FILE="$HOME/crontab_backup_$(date +%Y%m%d_%H%M%S).txt"
crontab -l > "$BACKUP_FILE" 2>/dev/null || echo "# New crontab" > "$BACKUP_FILE"
echo -e "${GREEN}✓${NC} Backed up existing crontab to: $BACKUP_FILE"

# Create temporary crontab file
TEMP_CRONTAB=$(mktemp)
crontab -l > "$TEMP_CRONTAB" 2>/dev/null || echo "# New crontab" > "$TEMP_CRONTAB"

# Remove old Instagram bot entries (if any)
sed -i '/Instagram Bot/d' "$TEMP_CRONTAB" 2>/dev/null || true
sed -i '/gramaddict/d' "$TEMP_CRONTAB" 2>/dev/null || true
sed -i '/runner.py/d' "$TEMP_CRONTAB" 2>/dev/null || true

# Add new cron jobs
cat >> "$TEMP_CRONTAB" << EOF

# ========================================
# Instagram Bot - Automated Sessions
# ========================================
# Morning session: 9:30am
30 9 * * * cd $PROJECT_DIR && $PYTHON_BIN runner.py morning >> $LOG_DIR/cron.log 2>&1

# Lunch session: 1:45pm
45 13 * * * cd $PROJECT_DIR && $PYTHON_BIN runner.py lunch >> $LOG_DIR/cron.log 2>&1

# Evening session: 6:15pm
15 18 * * * cd $PROJECT_DIR && $PYTHON_BIN runner.py evening >> $LOG_DIR/cron.log 2>&1

# Extra session (optional): 3:30pm on Mon/Wed/Fri
30 15 * * 1,3,5 cd $PROJECT_DIR && $PYTHON_BIN runner.py extra >> $LOG_DIR/cron.log 2>&1

# Weekly cleanup: Sunday 11pm
0 23 * * 0 cd $PROJECT_DIR && $PYTHON_BIN runner.py cleanup >> $LOG_DIR/cron.log 2>&1

EOF

# Install new crontab
crontab "$TEMP_CRONTAB"
rm "$TEMP_CRONTAB"

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}✓ Cron jobs installed successfully!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Schedule:"
echo "  - Morning:  9:30am daily"
echo "  - Lunch:    1:45pm daily"
echo "  - Evening:  6:15pm daily"
echo "  - Extra:    3:30pm (Mon/Wed/Fri only)"
echo "  - Cleanup:  11:00pm Sunday"
echo ""
echo "Expected activity:"
echo "  - 3 sessions/day (most days)"
echo "  - 4 sessions/day (Mon/Wed/Fri)"
echo "  - ~150-200 interactions/day"
echo "  - ~90-120 likes/day"
echo "  - ~30-40 follows/day"
echo ""
echo "Commands:"
echo "  View jobs:    crontab -l"
echo "  Edit jobs:    crontab -e"
echo "  Remove jobs:  crontab -r"
echo "  View logs:    tail -f $LOG_DIR/cron.log"
echo "  Restore:      crontab $BACKUP_FILE"
echo ""
echo -e "${YELLOW}Note: Make sure your device is connected and Instagram is logged in!${NC}"
echo ""
