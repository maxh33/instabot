"""
Metrics Analyzer for Instagram Bot
Analyzes logs and JSON data to provide insights and metrics
"""
import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
from collections import defaultdict


class MetricsAnalyzer:
    """Analyze Instagram bot metrics from logs and JSON data"""

    def __init__(self, username: str):
        self.username = username
        self.base_path = Path(__file__).parent
        self.accounts_path = self.base_path / "accounts" / username
        self.logs_path = self.base_path / "logs"

        # Data storage
        self.interacted_users = {}
        self.sessions = []

        # Load data
        self.load_data()

    def load_data(self):
        """Load interaction and session data from JSON files"""
        # Load interacted users
        users_file = self.accounts_path / "interacted_users.json"
        if users_file.exists():
            with open(users_file, 'r', encoding='utf-8') as f:
                self.interacted_users = json.load(f)

        # Load sessions
        sessions_file = self.accounts_path / "sessions.json"
        if sessions_file.exists():
            with open(sessions_file, 'r', encoding='utf-8') as f:
                self.sessions = json.load(f)

    def get_account_stats(self) -> dict:
        """Get overall account statistics"""
        stats = {
            "total_interactions": len(self.interacted_users),
            "total_sessions": len(self.sessions),
            "users_followed": 0,
            "users_unfollowed": 0,
            "currently_following": 0,
            "total_likes_given": 0,
            "total_stories_watched": 0,
            "total_comments_sent": 0,
            "total_pms_sent": 0,
        }

        for username, data in self.interacted_users.items():
            if data.get("followed"):
                stats["users_followed"] += 1
            if data.get("unfollowed"):
                stats["users_unfollowed"] += 1
            if data.get("following_status") == "following":
                stats["currently_following"] += 1

            stats["total_likes_given"] += data.get("liked", 0)
            stats["total_stories_watched"] += data.get("watched", 0)
            stats["total_comments_sent"] += data.get("commented", 0)
            stats["total_pms_sent"] += 1 if data.get("pm_sent") else 0

        return stats

    def get_session_stats(self, days: int = 7) -> dict:
        """Get session statistics for last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent_sessions = []

        for session in self.sessions:
            start_time_str = session.get("start_time", "")
            if start_time_str:
                try:
                    start_time = datetime.fromisoformat(start_time_str.replace(" ", "T"))
                    if start_time >= cutoff_date:
                        recent_sessions.append(session)
                except ValueError:
                    continue

        if not recent_sessions:
            return {"message": f"No sessions in last {days} days"}

        stats = {
            "period_days": days,
            "total_sessions": len(recent_sessions),
            "total_interactions": sum(s.get("total_interactions", 0) for s in recent_sessions),
            "successful_interactions": sum(s.get("successful_interactions", 0) for s in recent_sessions),
            "total_likes": sum(s.get("total_likes", 0) for s in recent_sessions),
            "total_follows": sum(s.get("total_followed", 0) for s in recent_sessions),
            "total_unfollows": sum(s.get("total_unfollowed", 0) for s in recent_sessions),
            "total_watched": sum(s.get("total_watched", 0) for s in recent_sessions),
            "avg_session_duration_minutes": 0,
            "success_rate": 0,
        }

        # Calculate average session duration
        durations = []
        for session in recent_sessions:
            start = session.get("start_time")
            finish = session.get("finish_time")
            if start and finish:
                try:
                    start_dt = datetime.fromisoformat(start.replace(" ", "T"))
                    finish_dt = datetime.fromisoformat(finish.replace(" ", "T"))
                    duration = (finish_dt - start_dt).total_seconds() / 60
                    durations.append(duration)
                except ValueError:
                    continue

        if durations:
            stats["avg_session_duration_minutes"] = round(sum(durations) / len(durations), 2)

        # Calculate success rate
        if stats["total_interactions"] > 0:
            stats["success_rate"] = round(
                (stats["successful_interactions"] / stats["total_interactions"]) * 100, 1
            )

        return stats

    def get_followed_accounts(self, status: str = "following") -> list[dict]:
        """
        Get list of followed accounts

        Args:
            status: "following", "unfollowed", or "all"
        """
        accounts = []

        for username, data in self.interacted_users.items():
            if status == "all":
                if data.get("followed"):
                    accounts.append({
                        "username": username,
                        "following_status": data.get("following_status", "unknown"),
                        "last_interaction": data.get("last_interaction"),
                        "source": data.get("target", "unknown"),
                    })
            elif data.get("following_status") == status:
                accounts.append({
                    "username": username,
                    "last_interaction": data.get("last_interaction"),
                    "source": data.get("target", "unknown"),
                    "liked_posts": data.get("liked", 0),
                })

        # Sort by last interaction (most recent first)
        accounts.sort(key=lambda x: x.get("last_interaction", ""), reverse=True)
        return accounts

    def get_source_performance(self) -> dict:
        """Analyze performance by source (hashtags, bloggers, etc.)"""
        sources = defaultdict(lambda: {
            "total_attempts": 0,
            "successful": 0,
            "followed": 0,
            "likes_given": 0,
        })

        for username, data in self.interacted_users.items():
            source = data.get("target", "unknown")
            sources[source]["total_attempts"] += 1

            if data.get("liked", 0) > 0 or data.get("followed"):
                sources[source]["successful"] += 1

            if data.get("followed"):
                sources[source]["followed"] += 1

            sources[source]["likes_given"] += data.get("liked", 0)

        # Calculate success rates
        for source, stats in sources.items():
            if stats["total_attempts"] > 0:
                stats["success_rate"] = round(
                    (stats["successful"] / stats["total_attempts"]) * 100, 1
                )
            else:
                stats["success_rate"] = 0

        return dict(sources)

    def get_filter_effectiveness(self) -> dict:
        """Analyze filter effectiveness from recent logs"""
        log_file = self.logs_path / f"{self.username}.log"
        if not log_file.exists():
            return {"error": "Log file not found"}

        stats = {
            "total_checked": 0,
            "private_accounts": 0,
            "empty_accounts": 0,
            "business_accounts": 0,
            "successful_interactions": 0,
            "rejection_rate": 0,
        }

        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                content = f.read()

                # Count interactions
                stats["total_checked"] = len(re.findall(r'@\w+: interact', content))
                stats["private_accounts"] = len(re.findall(r'Private account\.', content))
                stats["empty_accounts"] = len(re.findall(r'Empty account\.', content))
                stats["business_accounts"] = len(re.findall(r'Business account\.', content))
                stats["successful_interactions"] = len(re.findall(r'successful interaction', content))

                # Calculate rejection rate
                total_rejections = (
                    stats["private_accounts"] +
                    stats["empty_accounts"] +
                    stats["business_accounts"]
                )

                if stats["total_checked"] > 0:
                    stats["rejection_rate"] = round(
                        (total_rejections / stats["total_checked"]) * 100, 1
                    )

        except Exception as e:
            return {"error": str(e)}

        return stats

    def get_follower_growth(self) -> list[dict]:
        """Get follower/following counts from session data"""
        growth = []

        for session in self.sessions:
            start_time = session.get("start_time")
            profile_data = session.get("profile_data", {})

            if start_time and profile_data:
                growth.append({
                    "date": start_time.split()[0],  # Extract date
                    "time": start_time.split()[1] if len(start_time.split()) > 1 else "",
                    "followers": profile_data.get("followers", 0),
                    "following": profile_data.get("following", 0),
                    "posts": profile_data.get("posts", 0),
                })

        return growth

    def export_metrics_to_json(self, output_file: Optional[str] = None):
        """Export all metrics to JSON file"""
        if output_file is None:
            output_file = self.base_path / "metrics" / f"{self.username}_metrics.json"
        else:
            output_file = Path(output_file)

        output_file.parent.mkdir(exist_ok=True)

        metrics = {
            "username": self.username,
            "generated_at": datetime.now().isoformat(),
            "account_stats": self.get_account_stats(),
            "recent_sessions": self.get_session_stats(days=7),
            "followed_accounts": self.get_followed_accounts(status="following"),
            "source_performance": self.get_source_performance(),
            "filter_effectiveness": self.get_filter_effectiveness(),
            "follower_growth": self.get_follower_growth(),
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2, ensure_ascii=False)

        return output_file

    def print_summary(self):
        """Print a formatted summary to console"""
        print(f"\n{'='*60}")
        print(f"📊 Instagram Bot Metrics - @{self.username}")
        print(f"{'='*60}\n")

        # Account stats
        stats = self.get_account_stats()
        print("📈 Overall Statistics:")
        print(f"  Total interactions: {stats['total_interactions']}")
        print(f"  Users followed: {stats['users_followed']}")
        print(f"  Currently following: {stats['currently_following']}")
        print(f"  Users unfollowed: {stats['users_unfollowed']}")
        print(f"  Likes given: {stats['total_likes_given']}")
        print(f"  Stories watched: {stats['total_stories_watched']}")

        # Recent sessions
        print(f"\n📅 Last 7 Days:")
        session_stats = self.get_session_stats(days=7)
        if "message" not in session_stats:
            print(f"  Sessions: {session_stats['total_sessions']}")
            print(f"  Interactions: {session_stats['total_interactions']}")
            print(f"  Success rate: {session_stats['success_rate']}%")
            print(f"  Avg duration: {session_stats['avg_session_duration_minutes']} min")
        else:
            print(f"  {session_stats['message']}")

        # Filter effectiveness
        print(f"\n🔍 Filter Effectiveness:")
        filter_stats = self.get_filter_effectiveness()
        if "error" not in filter_stats:
            print(f"  Accounts checked: {filter_stats['total_checked']}")
            print(f"  Private accounts: {filter_stats['private_accounts']}")
            print(f"  Empty accounts: {filter_stats['empty_accounts']}")
            print(f"  Rejection rate: {filter_stats['rejection_rate']}%")

        # Top sources
        print(f"\n🎯 Top Sources (by interactions):")
        sources = self.get_source_performance()
        sorted_sources = sorted(
            sources.items(),
            key=lambda x: x[1]["total_attempts"],
            reverse=True
        )[:5]

        for source, data in sorted_sources:
            print(f"  {source}")
            print(f"    Attempts: {data['total_attempts']}, Success: {data['success_rate']}%, Followed: {data['followed']}")

        print(f"\n{'='*60}\n")


def main():
    """CLI interface for metrics analyzer"""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python metrics_analyzer.py <username> [command]")
        print("\nCommands:")
        print("  summary       - Print summary (default)")
        print("  export        - Export metrics to JSON")
        print("  followed      - List followed accounts")
        print("  sources       - Show source performance")
        sys.exit(1)

    username = sys.argv[1]
    command = sys.argv[2] if len(sys.argv) > 2 else "summary"

    analyzer = MetricsAnalyzer(username)

    if command == "summary":
        analyzer.print_summary()

    elif command == "export":
        output_file = analyzer.export_metrics_to_json()
        print(f"✓ Metrics exported to: {output_file}")

    elif command == "followed":
        accounts = analyzer.get_followed_accounts()
        print(f"\n📋 Currently Following ({len(accounts)} accounts):\n")
        for acc in accounts[:20]:  # Show first 20
            print(f"  @{acc['username']}")
            print(f"    Source: {acc['source']}, Last: {acc['last_interaction']}")

    elif command == "sources":
        sources = analyzer.get_source_performance()
        print(f"\n🎯 Source Performance:\n")
        for source, data in sorted(sources.items(), key=lambda x: x[1]["total_attempts"], reverse=True):
            print(f"  {source}:")
            print(f"    Attempts: {data['total_attempts']}, Success: {data['success_rate']}%, Followed: {data['followed']}")

    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
