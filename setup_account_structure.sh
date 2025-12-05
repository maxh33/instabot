#!/bin/bash
# Setup proper account structure for GramAddict
# Fixes the "can't find accounts/maxhaider.dev/filter.json" warning

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Setting up account structure...${NC}"
echo ""

# Get username from .env or ask user
if [ -f .env ]; then
    USERNAME=$(grep INSTAGRAM_USER_A .env | cut -d'=' -f2 | tr -d '"' | tr -d "'")
fi

if [ -z "$USERNAME" ]; then
    read -p "Enter Instagram username: " USERNAME
fi

# Create account directory
ACCOUNT_DIR="accounts/$USERNAME"
mkdir -p "$ACCOUNT_DIR"
echo -e "${GREEN}✓${NC} Created directory: $ACCOUNT_DIR"

# Copy filters.yml to account-specific filter.json
if [ -f accounts/filters.yml ]; then
    cp accounts/filters.yml "$ACCOUNT_DIR/filter.json"
    echo -e "${GREEN}✓${NC} Copied filters to: $ACCOUNT_DIR/filter.json"
else
    echo -e "${YELLOW}⚠${NC} accounts/filters.yml not found, skipping filter copy"
fi

# Copy session configs (optional - they can stay in accounts/ root)
# This allows you to run sessions directly without specifying full path
# for config in session_morning.yml session_lunch.yml session_evening.yml session_extra.yml; do
#     if [ -f "accounts/$config" ]; then
#         cp "accounts/$config" "$ACCOUNT_DIR/"
#         echo -e "${GREEN}✓${NC} Copied $config to account directory"
#     fi
# done

echo ""
echo -e "${GREEN}✓ Account structure ready!${NC}"
echo ""
echo "Structure:"
echo "  accounts/"
echo "  ├── $USERNAME/"
echo "  │   └── filter.json"
echo "  ├── session_morning.yml"
echo "  ├── session_lunch.yml"
echo "  ├── session_evening.yml"
echo "  └── session_extra.yml"
echo ""
echo "The warning should now be gone when running the bot."
echo ""
