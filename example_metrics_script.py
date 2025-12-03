"""
Example script for collecting and analyzing Instagram bot metrics
Demonstrates how to use the MetricsAnalyzer class for custom analysis
"""
from metrics_analyzer import MetricsAnalyzer
from datetime import datetime
import json

# Replace with your Instagram username
USERNAME = "maxhaider.dev"


def weekly_report():
    """Generate a weekly performance report"""
    print(f"\n{'='*60}")
    print(f"📊 Weekly Report - @{USERNAME}")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    analyzer = MetricsAnalyzer(USERNAME)

    # Overall stats
    stats = analyzer.get_account_stats()
    print("📈 Total Performance:")
    print(f"  Total interactions: {stats['total_interactions']}")
    print(f"  Currently following: {stats['currently_following']}")
    print(f"  Follow/Unfollow ratio: {stats['users_followed']}/{stats['users_unfollowed']}")
    print(f"  Total engagement: {stats['total_likes_given']} likes, {stats['total_stories_watched']} stories")

    # Last 7 days
    weekly = analyzer.get_session_stats(days=7)
    if "message" not in weekly:
        print(f"\n📅 This Week ({weekly['period_days']} days):")
        print(f"  Sessions completed: {weekly['total_sessions']}")
        print(f"  Interactions: {weekly['total_interactions']} ({weekly['successful_interactions']} successful)")
        print(f"  Success rate: {weekly['success_rate']}%")
        print(f"  Actions: {weekly['total_likes']} likes, {weekly['total_follows']} follows")
        print(f"  Average session: {weekly['avg_session_duration_minutes']} minutes")

    # Filter effectiveness
    filter_stats = analyzer.get_filter_effectiveness()
    if "error" not in filter_stats:
        print(f"\n🔍 Filter Effectiveness:")
        print(f"  Total checked: {filter_stats['total_checked']}")
        print(f"  Filtered out: {filter_stats['private_accounts']} private, {filter_stats['empty_accounts']} empty, {filter_stats['business_accounts']} business")
        print(f"  Rejection rate: {filter_stats['rejection_rate']}%")

        if filter_stats['rejection_rate'] > 80:
            print(f"  ⚠️  Warning: High rejection rate. Consider loosening filters.")
        elif filter_stats['rejection_rate'] < 50:
            print(f"  ⚠️  Warning: Low rejection rate. Consider tightening filters.")

    # Source performance
    print(f"\n🎯 Top 5 Sources:")
    sources = analyzer.get_source_performance()
    sorted_sources = sorted(
        sources.items(),
        key=lambda x: x[1]["successful"],
        reverse=True
    )[:5]

    for rank, (source, data) in enumerate(sorted_sources, 1):
        print(f"  {rank}. {source}")
        print(f"     Success: {data['success_rate']}% ({data['successful']}/{data['total_attempts']})")
        print(f"     Followed: {data['followed']}, Likes: {data['likes_given']}")

    print(f"\n{'='*60}\n")


def growth_tracking():
    """Track follower growth over time"""
    analyzer = MetricsAnalyzer(USERNAME)
    growth = analyzer.get_follower_growth()

    if not growth:
        print("No growth data available yet")
        return

    print(f"\n📈 Follower Growth Tracking\n")
    print(f"{'Date':<12} {'Time':<10} {'Followers':<12} {'Following':<12} {'Posts':<8}")
    print(f"{'-'*58}")

    for record in growth[-10:]:  # Last 10 records
        print(f"{record['date']:<12} {record['time']:<10} {record['followers']:<12} {record['following']:<12} {record['posts']:<8}")

    if len(growth) >= 2:
        first = growth[0]
        last = growth[-1]
        follower_change = last['followers'] - first['followers']
        following_change = last['following'] - first['following']

        print(f"\n{'='*58}")
        print(f"Change: {follower_change:+d} followers, {following_change:+d} following")

        if follower_change > 0:
            print(f"✓ Growing! Average: {follower_change / len(growth):.1f} followers per session")
        elif follower_change < 0:
            print(f"⚠️  Declining by {abs(follower_change)} followers")
        else:
            print(f"→ Stable")


def analyze_followed_accounts():
    """Analyze followed accounts by source"""
    analyzer = MetricsAnalyzer(USERNAME)
    accounts = analyzer.get_followed_accounts(status="following")

    print(f"\n👥 Currently Following: {len(accounts)} accounts\n")

    if not accounts:
        print("Not following anyone yet")
        return

    # Group by source
    by_source = {}
    for acc in accounts:
        source = acc['source']
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(acc)

    print("By Source:")
    for source, source_accounts in sorted(by_source.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n  {source}: {len(source_accounts)} accounts")
        # Show first 3
        for acc in source_accounts[:3]:
            print(f"    - @{acc['username']} (last: {acc['last_interaction']})")
        if len(source_accounts) > 3:
            print(f"    ... and {len(source_accounts) - 3} more")


def export_custom_report():
    """Export custom JSON report with additional calculations"""
    analyzer = MetricsAnalyzer(USERNAME)

    report = {
        "generated_at": datetime.now().isoformat(),
        "username": USERNAME,
        "summary": {
            "account_stats": analyzer.get_account_stats(),
            "week_7_days": analyzer.get_session_stats(days=7),
            "week_30_days": analyzer.get_session_stats(days=30),
        },
        "analysis": {
            "filter_effectiveness": analyzer.get_filter_effectiveness(),
            "source_performance": analyzer.get_source_performance(),
            "follower_growth": analyzer.get_follower_growth(),
        },
        "lists": {
            "following": analyzer.get_followed_accounts(status="following"),
            "unfollowed": analyzer.get_followed_accounts(status="unfollowed"),
        }
    }

    # Calculate additional metrics
    stats_7 = report["summary"]["week_7_days"]
    if "message" not in stats_7 and stats_7["total_interactions"] > 0:
        report["kpis"] = {
            "engagement_rate": round(
                (stats_7["total_likes"] + stats_7["total_watched"]) / stats_7["total_interactions"] * 100, 2
            ),
            "follow_rate": round(
                stats_7["total_follows"] / stats_7["total_interactions"] * 100, 2
            ),
            "efficiency_score": round(
                stats_7["successful_interactions"] / stats_7["total_sessions"] if stats_7["total_sessions"] > 0 else 0, 2
            ),
        }

    # Save to file
    filename = f"metrics/custom_report_{datetime.now():%Y%m%d_%H%M%S}.json"
    import os
    os.makedirs("metrics", exist_ok=True)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"✓ Custom report exported to: {filename}")
    return filename


def main():
    """Run all analysis examples"""
    print("\n🤖 Instagram Bot Metrics Analysis\n")

    try:
        # 1. Weekly summary
        weekly_report()

        # 2. Growth tracking
        growth_tracking()

        # 3. Followed accounts analysis
        analyze_followed_accounts()

        # 4. Export custom report
        export_custom_report()

    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print(f"\nMake sure:")
        print(f"  1. The bot has run at least once")
        print(f"  2. Username '{USERNAME}' is correct")
        print(f"  3. Files exist in accounts/{USERNAME}/")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()
