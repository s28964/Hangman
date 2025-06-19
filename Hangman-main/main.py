import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from register_or_login import register, login
from stats import get_player_stats, get_top_players
from export import export_stats_to_csv
from database import session
from models import User, Word
from game import get_two_words_from_category, get_word_of_equal_length, lives
from init_words import add_words
from PIL import Image, ImageTk



class HangmanGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wisielec")
        self.geometry("1200x1000")
        self.resizable(True, True) 
        self.current_user = None
        self.player2 = None
        self.game_mode = None
        self.category = None
        self.hangman_images = []
        for i in range(8):  # 0-7 (7 żyć = 8 obrazków, w tym 0 błędów)
            img = Image.open(f"{i}.png")
            self.hangman_images.append(ImageTk.PhotoImage(img))
        self.lives = lives
        self.init_login_screen()


    def clear_screen(self): #czyści okno przed załadowaniem ponownie
        for widget in self.winfo_children():
            widget.destroy()


    def init_login_screen(self): #logowanie/rejestracja
        self.clear_screen()
        tk.Label(self, text="Wisielec", font=("Helvetica", 30)).pack(pady=30)
        frame = tk.Frame(self)
        frame.pack(pady=10)
        tk.Label(frame, text="Nazwa użytkownika:").grid(row=0, column=0, sticky="e")
        username_entry = tk.Entry(frame)
        username_entry.grid(row=0, column=1)
        tk.Label(frame, text="Hasło:").grid(row=1, column=0, sticky="e")
        password_entry = tk.Entry(frame, show="*")
        password_entry.grid(row=1, column=1)

        def do_login():
            username = username_entry.get()
            password = password_entry.get()
            success, msg = login(username, password)
            if success:
                self.current_user = session.query(User).filter_by(username=username).first()
                self.init_main_menu()
            else:
                messagebox.showerror("Błąd logowania", msg)

        def do_register():
            username = username_entry.get()
            password = password_entry.get()
            success, msg = register(username, password)
            if success:
                messagebox.showinfo("Rejestracja", "Zarejestrowano pomyślnie! Możesz się zalogować.")
            else:
                messagebox.showerror("Błąd rejestracji", msg)

        tk.Button(self, text="Zaloguj", command=do_login, width=20).pack(pady=10)
        tk.Button(self, text="Zarejestruj", command=do_register, width=20).pack()


    def init_main_menu(self): #glowne menu po zalogowaniu
        self.clear_screen()
        tk.Label(self, text=f"Witaj, {self.current_user.username}", font=("Helvetica", 20)).pack(pady=20)
        tk.Button(self, text="Rozpocznij grę", command=self.init_choose_opponent, width=30, height=2).pack(pady=10)
        tk.Button(self, text="Statystyki", command=self.init_stats_screen, width=30, height=2).pack(pady=10)
        tk.Button(self, text="Eksportuj wyniki", command=self.export_stats, width=30, height=2).pack(pady=10)
        tk.Button(self, text="Wyloguj", command=self.init_login_screen, width=30, height=2).pack(pady=10)


    def init_choose_opponent(self): #konfiguracja gry -> gracz z bazdy, tryb gry, kategoria
        self.clear_screen()
        tk.Label(self, text="Wybierz przeciwnika", font=("Helvetica", 16)).pack(pady=10)
        users = session.query(User).filter(User.username != self.current_user.username).all()
        user_list = [u.username for u in users]
        if not user_list:
            messagebox.showerror("Brak graczy", "Brak innych użytkowników. Dodaj nowego gracza.")
            self.init_main_menu()
            return
        self.opponent_var = tk.StringVar(value=user_list[0])
        tk.OptionMenu(self, self.opponent_var, *user_list).pack(pady=10)
        tk.Label(self, text="Wybierz tryb gry:").pack(pady=5)
        self.mode_var = tk.StringVar(value="normalny")
        tk.Radiobutton(self, text="Tryb normalny", variable=self.mode_var, value="normalny").pack()
        tk.Radiobutton(self, text="Tryb losowy", variable=self.mode_var, value="losowy").pack()
        tk.Label(self, text="Wybierz kategorię (opcjonalnie, niedostępne dla trybu losowego):").pack(pady=5)
        categories = sorted(set([w.category for w in session.query(Word).all()]))
        self.cat_var = tk.StringVar(value="")
        self.category_menu = tk.OptionMenu(self, self.cat_var, "", *categories)
        self.category_menu.pack(pady=10)
        tk.Button(self, text="Rozpocznij grę", command=self.start_game, width=25).pack(pady=20)
        tk.Button(self, text="Wróć", command=self.init_main_menu, width=25).pack()
        # Funkcja do wyszarzania
        def update_category_state(*args):
            if self.mode_var.get() == "losowy":
                self.category_menu.config(state="disabled")
            else:
                self.category_menu.config(state="normal")

        # Podpięcie funkcji do zmiany trybu gry
        self.mode_var.trace("w", update_category_state)

    def start_game(self):  #rozpoznanie trybu gry + start
        self.player2 = session.query(User).filter_by(username=self.opponent_var.get()).first()
        self.game_mode = self.mode_var.get()
        self.category = self.cat_var.get() if self.cat_var.get() else None
        if self.game_mode == "normalny":
            self.init_game_screen(normal=True)
        else:
            self.init_game_screen(normal=False)

    def init_game_screen(self, normal=True):  #inicjalizacja trybu gdy
        self.clear_screen()
        # Wybór słów i inicjalizacja stanu
        if normal:
            if self.category:
                word1, word2 = get_two_words_from_category(self.category)
            else:
                word1, word2 = get_word_of_equal_length()
        else:
            from game import get_two_random_words
            word1, word2 = get_two_random_words()
        self.state = {
            "player1": {"word": word1, "guessed_letters": set(), "errors": 0, "word_guessed": False},
            "player2": {"word": word2, "guessed_letters": set(), "errors": 0, "word_guessed": False},
        }
        self.current_player = "player1"
        self.update_game_screen()

    def update_game_screen(self):
        self.clear_screen()
        player = self.current_user if self.current_player == "player1" else self.player2
        pdata = self.state[self.current_player]

        # Nagłówek i informacje o grze
        tk.Label(self, text=f"Tura gracza: {player.username}", font=("Helvetica", 16)).pack(pady=10)
        tk.Label(
            self,
            text=f"Słowo: {' '.join([l if l == ' ' or l in pdata['guessed_letters'] else '_' for l in pdata['word']])}",
            font=("Helvetica", 20)
        ).pack(pady=10)
        tk.Label(self, text=f"Pozostałe życia: {self.lives - pdata['errors']}", font=("Helvetica", 14)).pack(pady=10)

        # Pole do zgadywania i komunikaty
        guess_entry = tk.Entry(self, font=("Helvetica", 16))
        guess_entry.pack(pady=10)
        msg_label = tk.Label(self, text="", font=("Helvetica", 12))
        msg_label.pack()

        # Przyciski NAJPIERW
        submit_button = tk.Button(self, text="Zatwierdź", command=lambda: submit_guess(), width=15)
        submit_button.pack(pady=10)
        tk.Button(self, text="Przerwij", command=self.init_main_menu, width=15).pack(pady=10)

        # Obrazek wisielca NA KONIEC
        image_label = tk.Label(self, image=self.hangman_images[pdata['errors']])
        image_label.pack(pady=10)


        def submit_guess():
            win = False
            lose = False
            guess = guess_entry.get().strip().upper()
            if not guess:
                msg_label.config(text="Wpisz literę lub słowo.")
                return
            if not all(c.isalpha() or c == ' ' for c in guess):
                msg_label.config(text="Tylko litery i spacje.")
                return
            if len(guess) == 1:
                if guess in pdata['guessed_letters']:
                    msg_label.config(text="Litera już była.")
                    return
                pdata['guessed_letters'].add(guess)
                if guess in pdata['word']:
                    msg_label.config(text="Dobra litera!")
                else:
                    msg_label.config(text="Zła litera!")
                    pdata['errors'] += 1
            else:
                if guess == pdata['word']:
                    msg_label.config(text="Odgadnięto całe słowo!")
                    pdata['word_guessed'] = True
                else:
                    msg_label.config(text="Złe słowo!")
                    pdata['errors'] += 1
            if pdata['errors'] >= self.lives:
                msg_label.config(text=f"Przegrana. Prawidłowe słowo: {pdata['word']}")
                pdata['word_guessed'] = True
                lose = True
            elif set([l for l in pdata['word'] if l != ' ']).issubset(pdata['guessed_letters']):
                msg_label.config(text="Brawo! Odgadnięto słowo.")
                pdata['word_guessed'] = True
                win = True
            if lose:
                self.after(3000, self.next_turn)  
            elif win:
                self.after(1200, self.next_turn)
            else:
                self.after(1200, self.next_turn)

        tk.Button(self, text="Zatwierdź", command=submit_guess, width=15).pack(pady=10)
        tk.Button(self, text="Przerwij", command=self.init_main_menu, width=15).pack(pady=10)

    def next_turn(self):
        # Jeśli którykolwiek z graczy odgadł lub przegrał, nie pokazuj już jego tury
        if self.state["player1"]["word_guessed"] and self.state["player2"]["word_guessed"]:
            for player, pdata in zip([self.current_user, self.player2], [self.state['player1'], self.state['player2']]):
                player.games_played += 1
                if pdata['errors'] < self.lives:
                    player.games_won += 1
            session.commit()
            messagebox.showinfo("Koniec gry", "Gra zakończona! Wyniki zapisane.")
            self.init_main_menu()
            return
        self.current_player = "player2" if self.current_player == "player1" else "player1"
        if self.state[self.current_player]["word_guessed"]:
            self.after(500, self.next_turn)
        else:
            self.update_game_screen()

    def init_stats_screen(self):  #ekran statystyk
        self.clear_screen()
        tk.Label(self, text="Statystyki graczy", font=("Helvetica", 18)).pack(pady=10)
        top = get_top_players(10)
        cols = ("Nazwa", "Rozegrane", "Wygrane", "Win rate [%]")
        tree = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c)
        for p in top:
            tree.insert("", "end", values=(p["username"], p["games_played"], p["games_won"], p["win_rate"]))
        tree.pack(pady=10)
        tk.Button(self, text="Pokaż moje statystyki", command=self.show_my_stats, width=25).pack(pady=5)
        tk.Button(self, text="Wróć", command=self.init_main_menu, width=25).pack(pady=5)

    def show_my_stats(self):
        stats = get_player_stats(self.current_user.username)
        if stats:
            messagebox.showinfo("Twoje statystyki",
                                f"Nazwa: {stats['username']}\nRozegrane: {stats['games_played']}\nWygrane: {stats['games_won']}\nWin rate: {stats['win_rate']}%")
        else:
            messagebox.showinfo("Brak statystyk", "Nie znaleziono statystyk.")


    def export_stats(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            export_stats_to_csv(filename)
            messagebox.showinfo("Eksport", f"Wyniki wyeksportowane do {filename}")




if __name__ == "__main__":
    add_words()
    app = HangmanGUI()
    app.mainloop()
