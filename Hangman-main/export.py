import csv
from models import User
from database import session
from stats import get_player_stats

def export_stats_to_csv(filename = "stats.csv"):
    users = session.query(User).filter(User.games_played > 0 ).all()

    if not users:
        print("\nNo users with at least 1 game found")
        return

    with open (filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["username", "games_played", "games_won", "win_rate"])

        for user in users:
            stats = get_player_stats(user.username)
            writer.writerow([
                stats['username'],
                stats['games_played'],
                stats['games_won'],
                stats['win_rate'],
            ])

    print(f"\n All player's stats have been exported to {filename}")