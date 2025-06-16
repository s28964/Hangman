import bcrypt
from models import User
from database import session

def register(username, password): #Funkcja do rejestracji nowego gracza
    if not username or not password or len(username) < 3 or len(password) < 4: #Walidacja typu nie może być pustych loginu i hasła i login większy niż 3 znaki i hasło więcej niż 4 znaki
        return False, "Username must be at least 3 characters long abd password must be at least 4 characters long"

    if session.query(User).filter_by(username = username).first(): #Sprawdza czy taki gracz już istnieje w bazie
        return False, "User already exists"

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #Haszowanie hasła przy użyciu bcrypt
    user = User(username = username, password = hashed_password.decode('utf-8')) #Tworzy nowego gracza z wpisaną nazwą i zaszyfrowanym hasłem
    session.add(user)
    session.commit() #Dodaje gracza do bazy i zapisuje zmiany
    return True, "User has been registered"

def login(username, password): #Funkcja do logowania gracza
    if not username or not password: #Walidacja typu nie może być pustych loginu i hasła
        return False, "Username and/or password cannot be empty"

    user = session.query(User).filter_by(username = username).first() #Sprawdza czy gracz istnieje w bazie
    if not user: #Jeżeli nie to wyrzuca błąd
        return False, "Wrong login or password"

    if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')): #Sprawdza czy wprowadzone hasło jest zgodne z zapisanym zaszyfrowanym hasłem
        return True, f"Welcome {username}" #Jak tak to loguje
    else:
        return False, "Wrong login or password" #Jak nie to wyrzuca błąd