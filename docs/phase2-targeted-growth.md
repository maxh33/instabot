# Phase 2 - Targeted Growth Playbook
Now that the hashtag smoke test script is steady, this phase focuses on reaching real people who recently interacted with niche leaders. Follow the steps below before running the new task selector.

## 1. Quality Filters (`accounts/filters.yml`)
Create or update `accounts/filters.yml` so GramAddict quickly rejects low quality profiles.

```yaml
# accounts/filters.yml
skip_business: true
skip_private: true
skip_empty_profile_pic: true
min_posts: 3
min_followers: 50
max_followers: 5000
min_following: 50
max_following: 1500
blacklisted-words: ["store", "shop", "promo", "discount", "nft", "crypto", "sex", "18+"]
# mandatory-words: ["dev", "code", "tech", "engineer", "student"]
```

These defaults are conservative; tune the boundaries once you observe real conversions. Keep `filters.yml` beside your account folders so every strategy run inherits it automatically.

## 2. Competitor Sniper run (`accounts/strategy_growth.yml`)
Create `accounts/strategy_growth.yml` and list the accounts whose audience overlaps your niche. GramAddict will grab the latest post from each handle and walk the likers list.

**IMPORTANT**: GramAddict v3.2.12 uses **FLAT YAML format** (no `jobs:` wrapper, no `time-limit` parameter).

```yaml
# accounts/strategy_growth.yml (FLAT format)
device: fbc9d1f30eb2
allow-untested-ig-version: true
total-sessions: 3

# Target Sources (FLAT format - no jobs wrapper)
blogger-post-likers: [realpython, freecodecamp, thepracticaldev, real.python]

# Daily Limits
total-likes-limit: 100
total-follows-limit: 30
total-interactions-limit: 150

# Human-like Behavior
likes-count: 1-3
likes-percentage: 60-80
follow-percentage: 35
stories-count: 1-3
stories-percentage: 25-40
watch-video-time: 12-25
watch-photo-time: 3-5
carousel-count: 1-3
carousel-percentage: 50-75
interact-percentage: 55
speed-multiplier: 0.85

# Session Controls
interactions-count: 8-15
skipped-list-limit: 8-12
repeat: 180-240
working-hours: [9-22]
```

Replace the handle list with two to four high-signal creators in your niche. Use `total-interactions-limit` to control session duration (not `time-limit`).

## 3. Weekly cleanup (`accounts/strategy_cleanup.yml`)
Schedule a light cleanup pass to remove non-mutuals after they have had time to follow back.

**IMPORTANT**: Use **FLAT format** (no `jobs:` wrapper).

```yaml
# accounts/strategy_cleanup.yml (FLAT format)
device: fbc9d1f30eb2
allow-untested-ig-version: true

# Unfollow Strategy (FLAT format - no jobs wrapper)
unfollow-non-followers: 150
unfollow-delay: 5
unfollow-skip-followed-list: true

# Whitelist Protection
whitelist:
  - my_best_friend
  - my_client_account
```

Run this profile once per week; increase `unfollow-delay` if you notice Instagram slowing the action queue.

## 4. Task selector (`runner.py`)
The repository now includes `runner.py`, a small wrapper that streams GramAddict output, rotates logs per task, and verifies ADB before launching. Key features:
- Select `growth` or `cleanup` mode at runtime (`python runner.py growth`)
- Streams CLI output to both console and `logs/gramaddict_<mode>.log`
- Falls back gracefully if `INSTAGRAM_USER_A` is missing (uses YAML username)
- Warns when `accounts/filters.yml` is absent so you do not forget the quality gate

### Environment variables
Ensure the following keys exist in `.env`:
- `INSTAGRAM_USER_A` (or the more general `INSTAGRAM_USER`)
- `DEVICE` (defaults to `127.0.0.1:5555` if omitted)

### Run commands
- `python runner.py growth`
- `python runner.py cleanup`

### Pre-run checklist
- Connect BlueStacks via `adb connect 127.0.0.1:<port>`
- Update the handle list in `strategy_growth.yml`
- Review the whitelist in `strategy_cleanup.yml`
- Tail the corresponding log under `logs/` if you want to monitor progress live

## 5. Block-proof logic recap
- **Already-liked detection**: GramAddict automatically skips posts you've already liked (built-in, no config needed)
- **Human-like behavior**: Use ranges for randomization (`likes-count: 1-3`), percentage parameters, story watching, video viewing, carousel swiping
- **Speed control**: Use `speed-multiplier: 0.85` to slow down all actions (default is 1.0)
- **Quality gate**: `filters.yml` skips business, private, and low-activity accounts by default
- **Bot detection**: Use follower/following ratios (`min_potency_ratio`, `max_potency_ratio`) and blacklist words
- **Warm traffic**: `blogger-post-likers` targets people who proved their interest minutes ago
- **Risk control**: Daily growth stays under 100 likes / 30 follows; weekly cleanup removes non-mutuals safely
- **Session control**: Use `total-interactions-limit` to control how long sessions run (not `time-limit`)
- **Transparency**: Dedicated logs per task make it easy to review what happened after each run

## 6. Human-like Behavior Parameters (New in Enhanced Version)

GramAddict v3.2.12 has extensive randomization features:

**Action Randomization**:
- `likes-count: 1-3` - Like 1-3 posts per user (randomized)
- `likes-percentage: 60-80` - Like only 60-80% of the time
- `follow-percentage: 35` - Follow 35% of interacted users
- `interact-percentage: 55` - Interact with only 55% of candidates

**Content Engagement**:
- `stories-count: 1-3` - Watch 1-3 stories per user
- `stories-percentage: 25-40` - Watch stories 25-40% of the time
- `watch-video-time: 12-25` - Watch videos for 12-25 seconds
- `watch-photo-time: 3-5` - Watch photos for 3-5 seconds
- `carousel-count: 1-3` - Swipe 1-3 carousel photos
- `carousel-percentage: 50-75` - Swipe carousel 50-75% of the time

**Speed & Behavior**:
- `speed-multiplier: 0.85` - Slow down all actions (0.85 = 15% slower)
- `interactions-count: 8-15` - Interact with 8-15 users per source
- `skipped-list-limit: 8-12` - Move to next source after 8-12 skips

**Note**: `action-delay` and `scroll-delay` parameters do NOT exist in v3.2.12. Delays are built into the interaction logic.
