#!/bin/bash
# Instagram Bot Master Scheduler
# Runs sessions with randomization to mimic human behavior

PROJECT_DIR="/path/to/instabot"  # CHANGE THIS
EMULATOR_NAME="Pixel1"           # CHANGE THIS to your AVD name (e.g., Pixel1)
cd "$PROJECT_DIR" || exit 1

# Activate virtual environment
source .venv/bin/activate

# Configuration
LOCK_FILE="/tmp/instabot.lock"
LOG_DIR="$PROJECT_DIR/logs/scheduler"
mkdir -p "$LOG_DIR"

SESSION_LOG="$LOG_DIR/scheduler_$(date +%Y%m%d).log"

# Function: Log with timestamp
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$SESSION_LOG"
}

# Function: Check if emulator is running
is_emulator_running() {
    adb devices | grep -q "emulator-"
    return $?
}

# Function: Start emulator if not running
start_emulator() {
    if is_emulator_running; then
        log "Emulator already running"
        return 0
    fi

    log "Starting Android emulator: $EMULATOR_NAME"

    # Start emulator in background (headless mode)
    nohup emulator -avd "$EMULATOR_NAME" -no-window -no-audio -no-boot-anim > /dev/null 2>&1 &

    # Wait for emulator to boot (max 120 seconds)
    log "Waiting for emulator to boot..."
    for i in {1..40}; do
        sleep 3
        if adb shell getprop sys.boot_completed 2>/dev/null | grep -q "1"; then
            log "Emulator booted successfully"
            return 0
        fi
    done

    log "ERROR: Emulator failed to boot within timeout"
    return 1
}

# Function: Check if bot is already running (prevent overlaps)
is_bot_running() {
    if [ -f "$LOCK_FILE" ]; then
        PID=$(cat "$LOCK_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0  # Running
        else
            rm -f "$LOCK_FILE"  # Stale lock file
            return 1
        fi
    fi
    return 1
}

# Function: Create lock file
create_lock() {
    echo $$ > "$LOCK_FILE"
}

# Function: Remove lock file
remove_lock() {
    rm -f "$LOCK_FILE"
}

# Main execution
main() {
    log "=== Scheduler triggered ==="

    # Check if already running
    if is_bot_running; then
        log "Bot already running (PID: $(cat $LOCK_FILE)). Skipping this session."
        exit 0
    fi

    # Ensure emulator is running
    if ! start_emulator; then
        log "ERROR: Failed to start emulator"
        exit 1
    fi

    # Determine which session to run based on current time
    HOUR=$(date +%H)

    if [ "$HOUR" -ge 9 ] && [ "$HOUR" -lt 11 ]; then
        SESSION="morning"
        CONFIG="accounts/session_morning.yml"
    elif [ "$HOUR" -ge 12 ] && [ "$HOUR" -lt 14 ]; then
        SESSION="lunch"
        CONFIG="accounts/session_lunch.yml"
    elif [ "$HOUR" -ge 17 ] && [ "$HOUR" -lt 19 ]; then
        SESSION="evening"
        CONFIG="accounts/session_evening.yml"
    else
        SESSION="extra"
        CONFIG="accounts/session_extra.yml"
    fi

    log "Selected session: $SESSION (config: $CONFIG)"

    # Check if config exists
    if [ ! -f "$CONFIG" ]; then
        log "ERROR: Config file not found: $CONFIG"
        exit 1
    fi

    # Create lock file
    create_lock

    # Run the bot
    log "Starting Instagram bot..."
    python3 runner.py "$SESSION" 2>&1 | tee -a "$SESSION_LOG"
    EXIT_CODE=$?

    # Remove lock file
    remove_lock

    if [ $EXIT_CODE -eq 0 ]; then
        log "Session completed successfully"
    else
        log "Session failed with exit code: $EXIT_CODE"
    fi

    log "=== Scheduler finished ==="
}

# Trap to ensure lock file is removed on exit/error
trap remove_lock EXIT INT TERM

# Run main function
main
