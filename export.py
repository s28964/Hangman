import csv
from models import User
from database import session
from stats import get_player_stats

def export_stats_to_csv(filename = "stats.csv"): #ustawia nazwę pliku na stats.csv
    users = session.query(User).filter(User.games_played > 0 ).all() #pobiera z bazy tych graczy, którzy mają co najmniej jedną grę

    if not users:
        print("\nNo users with at least 1 game found") #Jeżeli nie ma takich graczy to wypisuje komunikat i kończy działanie funkcji
        return

    with open (filename, mode='w', newline='', encoding='utf-8') as file: #otwiera lub tworzy plik do zapsiu, bez pustych linii, w formacie UTF-8
        writer = csv.writer(file)
        writer.writerow(["username", "games_played", "games_won", "win_rate"]) #zapisuje 1 wiersz jako nagłówki kolumn

        for user in users: #dla każdego gracza pobiera jego staty i zapisuje do pliku
            stats = get_player_stats(user.username)
            writer.writerow([
                stats['username'],
                stats['games_played'],
                stats['games_won'],
                stats['win_rate'],
            ])

    print(f"\n All player's stats have been exported to {filename}")