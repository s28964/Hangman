from models import User
from database import session

def get_player_stats(username: str):
    user = session.query(User).filter_by(username = username).first()
    if not user:
        return None

    played = user.games_played
    won = user.games_won
    win_rate = (won / played * 100) if played > 0 else 0.0

    return {
        "username": user.username,
        "games_played": played,
        "games_won": won,
        "win_rate": round(win_rate, 2)
    }

def get_top_players(limit=5):
    users = session.query(User).filter(User.games_played > 0).all()
    ranked = sorted(users, key=lambda u: u.games_won, reverse=True)

    top = []
    for user in ranked[:limit]:
        win_rate = round((user.games_won / user.games_played)* 100, 2)
        top.append({
            "username": user.username,
            "games_played": user.games_played,
            "games_won": user.games_won,
            "win_rate": win_rate
        })
    return top