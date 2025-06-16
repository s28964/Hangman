import random
from inputimeout import inputimeout, TimeoutOccurred
from database import session
from models import Word, User
from sqlalchemy import func


lives = 7 #Zycie graczy


def choose_word_with_same_length(length): #Funkcja do wylosowania słowa, które zawiera określoną długość (żeby obaj gracze mieli słowa tej samej długości)
    possible_words = session.query(Word).filter(func.length(Word.value) == length).all() #Wybiera te słowa, które pasują długością do pierwszego wylosowanego słowa
    if not possible_words:
        raise ValueError("Lack of words in database of that length") #jak nie ma to zwraca błąd
    return random.choice(possible_words).value.upper() #Jak jest to losuje słowo i je zwraca w dużych literach

def get_word_of_equal_length(): #Funkcja do wylosowania 2 słów o tej samej długości. Używane kiedy nie wybrana kategoria
    words = session.query(Word).all() #pobiera wszystkie hasła z bazy
    if not words:
        raise ValueError("Lack of words in database") #Jak nie ma haseł to rzuca wyjątek
    first_word = random.choice(words).value.upper() #Losuje pierwsze słowo i je bierze do dużych liter
    length = len(first_word) #Oblicza długość wylosowanego słowa
    second_word = choose_word_with_same_length(length) #Wywołuje powyższą funkcję do wylosowania 2 słowa o tej samej długości
    return first_word, second_word #Zwraca oba słowa

def get_two_words_from_category(category: str): #Funkcja do losowania 2 haseł z tej samej kategorii
    words = session.query(Word).filter(Word.category == category.upper()).order_by(func.random()).limit(2).all() #Pobiera tylko słowa z tej samej kategorii i losuje 2 z nich i zwraca jako liste
    if len(words) < 2: #Sprawdza czy są 2 różne słowa
        raise ValueError("Lack of words in database of that category") #Jeżeli nie to rzuca wyjątek
    return words[0].value.upper(), words[1].value.upper() #Zwraca wylosowane hasła jako duże litery



def get_two_random_words(): #Funkcja do losowania 2 losowych haseł
    words = session.query(Word).order_by(func.random()).limit(2).all() #Pobiera wszystkie hasła, losuje 2 i zwraca jako liste
    if len(words) < 2: #Sprawdza czy są co najmniej 2 słowa w bazie
        raise ValueError("There must be at least 2 words in database") #Jak nie to rzuca wyjątek
    return words[0].value.upper(), words[1].value.upper() #Zwraca hasła jako duże litery


def display_word_progress(chosen_word, guessed_letters): #Funkcja do wyświetlania hasła z odgadnientymi literami i podłogami tam gdzie nie odgadnięte
    return " ".join([letter if letter in guessed_letters else "_" for letter in chosen_word]) #Wyświetla listę znaków do wyświetlenia na podstawie liter w liście guessed_letters
    #Wyświetla litere jeżeli odgadnięta, zostawia spacje jeżęli w haśle jest spacja, reszte zamienia na "_"




def player_vs_player(player1: User, player2: User, category: str = None): #1 tryb gry -> gracz vs gracz. Przyjmuje obiekty 2 graczy i opcjonalnie kategorię hasła
    if category:
        word1, word2, = get_two_words_from_category(category) #Jeżeli wybrana kategoria to losuje hasła z tej samej kategorii
    else:
        word1, word2 = get_word_of_equal_length() #A jak nie, to losuje hasła tej samej długości
    state = { #Inicjalizacja stanu rozgrywki dla graczy jako słownik. Dla każdego inicjalizujemy stan jego hasła, set odgadniętych liter, błędy i czy odgadł hasło
        "player1": {"word": word1, "guessed_letters": set(), "errors": 0, "word_guessed": False},
        "player2": {"word": word2, "guessed_letters": set(), "errors": 0, "word_guessed": False},
    }

    print(f"\nBoth words have {len(word1)} letters). Players guess one by one \n")

    current_player = "player1" #Ustawienie gracza rozpoczynającego

    while not (state["player1"]["word_guessed"] and state["player2"]["word_guessed"]): #Dopóki hasło nie odgadnięte
        player = player1 if current_player == "player1" else player2 #Zmiana kolejki odgadywania
        pdata = state[current_player] #Status dla danego gracza
        if pdata["word_guessed"]: #Jak któryś gracz odgadł hasło to pomija jego ture
            current_player = "player2" if current_player == "player1" else "player1"
            continue

        print(f"{player.username} ({current_player}) turn")
        print(f"Word: {display_word_progress(pdata['word'], pdata['guessed_letters'])}")        #Aktualny stan gracza
        print(f"Lives left: {lives - pdata['errors']}")
        print(f"[Hangman: hangman{pdata['errors']}.png]") #Ścieżka do obrazków poszczególnych etapów wisielca (TUTAJ NIE OGARNIĘTE!!!)

        guess = input("\nGuess a letter or whole word: ").strip().upper() #Litera lub całe słowo jako duze litery
        if not guess:
            print("\nInput cannot be empty, try again") #Walidacja typu nie można pustego pola sprawdzic
            continue

        if not guess.isalpha() and " " not in guess:
            print("\nOnly letters ann spaces are allowed, try again") #Walidacja typu tylko litery można wpisać i spacje
            continue

        if len(guess) == 1: #Sprawdza odpowiednio czy litera była już próbowana, znajduje się w słowie, nie znajduje się w słowie
            if guess in pdata['guessed_letters']:
                print("Letter already guessed")
            elif guess in pdata['word']:
                print("Correct letter")
                pdata['guessed_letters'].add(guess)
            else:
                print("Wrong letter")
                pdata['guessed_letters'].add(guess)
                pdata['errors'] += 1
        else: #Sprawdza czy hasło jest poprawne czy nie
            if guess == pdata['word']:
                print("\nCongrats, you won")
                pdata['word_guessed'] = True
            else:
                print("Wrong word")
                pdata['errors'] += 1

        if pdata['errors'] >= lives: #Jak gracz popełnia 7 błąd to przegrywa
            print(f"\n {player.username} lost. Correct word is {pdata['word']}")
            pdata['word_guessed'] = True
        elif set(pdata['word']).issubset(pdata['guessed_letters']): #Jeżeli wszystkie litery zostały odgadnięte to gracz wygrywa
            print(f"\n {player.username} Won.")
            pdata['word_guessed'] = True

        current_player = "player2" if current_player == "player1" else "player2" #Zmiana gracza na koniec tury


    for player, pdata in zip([player1, player2], [state['player1'], state['player2']]): #Aktualizuje statystyki graczy. Zip łączy dwie listy w pary czyli jest player1 i state dla player1
        player.games_played += 1
        if pdata['errors'] < lives:
            player.games_won += 1


    session.commit() #Zapisuje aktualizację statystyk do bazy


def player_vs_player_rng(player1: User, player2: User): #2 tryb gry -> gracz vs gracz, ale wszystko jest losowe (poza życiem)
    word1, word2 = get_two_random_words() #losuje 2 losowe hasła

    state = { #Inicjalizacja stanu rozgrywki dla graczy jako słownik. Dla każdego inicjalizujemy stan jego hasła, set odgadniętych liter, błędy i czy odgadł hasło
        "player1": {"word": word1, "guessed_letters": set(), "errors": 0, "word_guessed": False},
        "player2": {"word": word2, "guessed_letters": set(), "errors": 0, "word_guessed": False},
    }

    print("\nBoth players have random words. Players guess one by one \n")

    current_player = "player1" #Ustawienie gracza rozpoczynającego

    while not (state["player1"]["word_guessed"] and state["player2"]["word_guessed"]): #Dopóki hasło nie odgadnięte
        player = player1 if current_player == "player1" else player2
        pdata = state[current_player] #Status dla danego gracza
        if pdata["word_guessed"]: #Jak któryś gracz odgadł hasło to pomija jego ture
            current_player = "player2" if current_player == "player1" else "player1"
            continue

        print(f"{player.username} ({current_player}) turn")
        print(f"Word: {display_word_progress(pdata['word'], pdata['guessed_letters'])}")    #Aktualny stan gracza
        print(f"Lives left: {lives - pdata['errors']}")
        print(f"[Hangman: hangman{pdata['errors']}.png]") #Ścieżka do obrazków poszczególnych etapów wisielca (TUTAJ NIE OGARNIĘTE!!!)

        timeout = random.randint(5,10) #Ustawia losowy czas na odpowiedź od 5 do 10 sekund
        print(f"\n You have {timeout} seconds left")

        try: #Gracz ma wylosowaną ilość czasu na odpowiedź
            guess = inputimeout(prompt= "Type letter or whole word: ", timeout = timeout).strip().upper()
        except TimeoutOccurred:
            print(f"\n Time's out")
            pdata['errors'] += 1 #Jak nie zdąży nic wpisać to traci życie
            guess = None

        if guess:
            if not guess.isalpha() and " " not in guess:
                print("\nOnly letters ann spaces are allowed, try again") #Walidacja typu tylko litery można wpisać i spacje
                continue

            if len(guess) == 1: #Sprawdza odpowiednio czy litera była już próbowana, znajduje się w słowie, nie znajduje się w słowie
                if guess in pdata['guessed_letters']:
                    print("Letter already guessed")
                elif guess in pdata['word']:
                    print("Correct letter")
                    pdata['guessed_letters'].add(guess)
                else:
                    print("Wrong letter")
                    pdata['guessed_letters'].add(guess)
                    pdata['errors'] += 1
            else: #Sprawdza czy hasło jest poprawne czy nie
                if guess == pdata['word']:
                    print("\nCongrats, you won")
                    pdata['word_guessed'] = True
                else:
                    print("Wrong word")
                    pdata['errors'] += 1

        if pdata['errors'] >= lives:
            print(f"\n {player.username} lost. Correct word is {pdata['word']}") #Jak gracz popełnia 7 błąd to przegrywa
            pdata['word_guessed'] = True
        elif set(pdata['word']).issubset(pdata['guessed_letters']): #Jeżeli wszystkie litery zostały odgadnięte to gracz wygrywa
            print(f"\n {player.username} Won.")
            pdata['word_guessed'] = True

        current_player = "player2" if current_player == "player1" else "player1" #Zmiana gracza na koniec tury

    for player, pdata in zip([player1, player2], [state['player1'], state['player2']]): #Aktualizuje statystyki graczy. Zip łączy dwie listy w pary czyli jest player1 i state dla player1
        player.games_played += 1
        if pdata['errors'] < lives:
            player.games_won += 1

    session.commit() #Zapisuje aktualizację statystyk do bazy
