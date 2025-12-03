#!/bin/bash
# Install randomized cron schedule for Instagram bot

PROJECT_DIR="/path/to/instabot"  # CHANGE THIS

# Function to generate random minute offset (-30 to +30)
random_offset() {
    echo $(( (RANDOM % 61) - 30 ))
}

# Install cron jobs with randomization
# Note: We'll use at/batch for true randomization, or create a daily cron that randomizes

cat << 'EOF' > /tmp/instabot_cron.txt
# Instagram Bot Scheduler - Randomized Times
# Base times with ±30 min randomization handled by scheduler.sh

# Morning session: 9:30am ±30 min = 9:00am-10:00am window
0 9 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1
15 9 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1
30 9 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1
45 9 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1

# Lunch session: 12:30pm ±30 min = 12:00pm-1:00pm window
0 12 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1
15 12 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1
30 12 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1
45 12 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1

# Evening session: 6:00pm ±30 min = 5:30pm-6:30pm window
30 17 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1
45 17 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1
0 18 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1
15 18 * * * /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1

# Extra session randomizer: 8:00am, 3:00pm, or 8:00pm (20% chance)
0 8 * * * [ $((RANDOM % 5)) -eq 0 ] && /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1
0 15 * * * [ $((RANDOM % 5)) -eq 0 ] && /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1
0 20 * * * [ $((RANDOM % 5)) -eq 0 ] && /path/to/instabot/scheduler.sh >> /path/to/instabot/logs/cron.log 2>&1

EOF

# Replace /path/to/instabot with actual path
sed -i "s|/path/to/instabot|$PROJECT_DIR|g" /tmp/instabot_cron.txt

# Install cron jobs
crontab -l > /tmp/current_cron.txt 2>/dev/null || true
cat /tmp/current_cron.txt /tmp/instabot_cron.txt | crontab -

echo "Cron jobs installed successfully!"
echo "View with: crontab -l"
