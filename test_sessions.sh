#!/bin/bash
# Quick test script to verify all sessions start correctly
# Each session runs for 60 seconds then auto-stops

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

SESSIONS=("morning" "lunch" "evening" "extra")
TEST_DURATION=60  # seconds

echo "======================================"
echo "Testing All Session Configs"
echo "======================================"
echo ""

# Activate venv
source .venv/bin/activate

for SESSION in "${SESSIONS[@]}"; do
    echo -e "${YELLOW}Testing $SESSION session...${NC}"
    echo "Starting session for ${TEST_DURATION}s..."

    # Run session in background with timeout
    timeout ${TEST_DURATION}s python runner.py $SESSION > "logs/test_${SESSION}.log" 2>&1 &
    PID=$!

    # Wait for it to finish
    wait $PID 2>/dev/null || true

    # Check if session started successfully
    if grep -q "Ready for botting" "logs/test_${SESSION}.log"; then
        echo -e "${GREEN}✓ $SESSION session started successfully${NC}"

        # Check for interactions
        if grep -q "Handle\|Interact\|Like" "logs/test_${SESSION}.log"; then
            echo -e "${GREEN}  ✓ Bot is interacting${NC}"
        fi
    else
        echo -e "${RED}✗ $SESSION session failed to start${NC}"
        echo "Check logs/test_${SESSION}.log for details"
    fi

    echo ""
    sleep 2
done

echo "======================================"
echo "Test Summary"
echo "======================================"
echo ""

# Check each log for errors
ERRORS_FOUND=0
for SESSION in "${SESSIONS[@]}"; do
    if [ -f "logs/test_${SESSION}.log" ]; then
        if grep -q "ERROR\|Traceback\|Exception" "logs/test_${SESSION}.log"; then
            echo -e "${RED}✗ $SESSION: Errors found${NC}"
            ERRORS_FOUND=1
        else
            echo -e "${GREEN}✓ $SESSION: No errors${NC}"
        fi
    fi
done

echo ""
if [ $ERRORS_FOUND -eq 0 ]; then
    echo -e "${GREEN}All sessions passed! Ready for cron setup.${NC}"
    echo ""
    echo "Next step: Run ./install_cron_linux.sh"
else
    echo -e "${RED}Some sessions had errors. Review logs in logs/ directory.${NC}"
fi
echo ""
