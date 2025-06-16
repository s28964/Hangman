from models import User
from database import session

def get_player_stats(username: str): #Funkcja do zwracania statystyk dla danego gracza po jego nazwie
    user = session.query(User).filter_by(username = username).first() # Sprawdza czy taki gracz jest w bazie
    if not user: #Jak nie to zwraca None
        return None

    played = user.games_played
    won = user.games_won                                        #Zbiera staty dla gracza
    win_rate = (won / played * 100) if played > 0 else 0.0

    return { #Zwraca staty w formie słownika
        "username": user.username,
        "games_played": played,
        "games_won": won,
        "win_rate": round(win_rate, 2)
    }

def display_player_stats(username: str): #Funkcja do wyświetlania statystyk dla danego gracza po jego nazwie
    if not username:
        print("\nUsername cannot be empty") #Walidacja typu nie można pokazać statów dla pustego pola z nazwą gracza
        return
    stats = get_player_stats(username) #Pobiera staty dla gracza
    if not stats: #Chyba że go nie ma w bazie, wtedy wali błąd
        print("\nPlayer not found")
        return

    print(f"\n Stats for {stats['username']}")
    print(f"\n Games played {stats['games_played']}")
    print(f"\n Games won {stats['games_won']}")
    print(f"\n Win rate {stats['win_rate']}")


def get_top_players(limit=5): #Funkcja do zwracania najlepszych 5 graczy
    users = session.query(User).filter(User.games_played > 0).all() #Pobiera tylko tych graczy którzy mają zagraną co najmniej 1 gre
    ranked = sorted(users, key=lambda u: u.games_won, reverse=True) #Sortuje graczy malejąca po liczbie zwycięstw

    top = [] #Tworzy listę top 5 graczy wraz z ich statami
    for user in ranked[:limit]:
        win_rate = round((user.games_won / user.games_played)* 100, 2)
        top.append({
            "username": user.username,
            "games_played": user.games_played,
            "games_won": user.games_won,
            "win_rate": win_rate
        })
    return top

def display_top_players(limit=5): #Funkcja do wyświetlania top 5 graczy
    top = get_top_players(limit) #Pobiera dane graczy
    print(f"\n Top {limit} players:")
    for number, player in enumerate(top, start=1): #Dla każdego gracza wyświetla jego pozycję, nazwę i staty
        print(f"\n {number}. {player['username']} - {player['games_won']}/{player['games_played']} games won -> ({player['win_rate']}%)")