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

```yaml
# accounts/strategy_growth.yml
username: ${INSTAGRAM_USER}
time-limit: 25
action-delay: [10, 25]
scroll-delay: [4, 8]

jobs:
  - interact-blogger-post-likers:
      - realpython
      - freecodecamp
      - thepracticaldev
      - system.design.daily

likes-count: 2
follow-percentage: 40
total-likes-limit: 60
total-follows-limit: 20
```

Replace the handle list with two to four high-signal creators in your niche and adjust the limits once you see how long a session lasts on your device.

## 3. Weekly cleanup (`accounts/strategy_cleanup.yml`)
Schedule a light cleanup pass to remove non-mutuals after they have had time to follow back.

```yaml
# accounts/strategy_cleanup.yml
jobs:
  - unfollow-non-followers:
      count: 150
      unfollow_delay: 5
      whitelist:
        - my_best_friend
        - my_client_account
```

Run this profile once per week; increase `unfollow_delay` if you notice Instagram slowing the action queue.

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
- Human pacing: `action-delay` and `scroll-delay` keep the session slow and natural
- Quality gate: `filters.yml` skips business, private, and low-activity accounts by default
- Warm traffic: `interact-blogger-post-likers` targets people who proved their interest minutes ago
- Risk control: Daily growth stays under 60 likes / 20 follows; weekly cleanup removes non-mutuals safely
- Transparency: Dedicated logs per task make it easy to review what happened after each run
