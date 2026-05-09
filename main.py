import customtkinter as ctk
import secrets
import string
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from PIL import Image
import os
import sys
import math

# ---------------------- Resource Path ----------------------
def resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

APP_ICON = resource_path("logo.ico")
LOGO_IMAGE_PATH = resource_path("assets/logo.png")

# ---------------------- Word Lists ----------------------
COMMON_WORDS = [
    "moon", "star", "sun", "sky", "wind", "fire", "rain", "tree", "leaf", "rock",
    "blue", "red", "green", "black", "white", "fast", "run", "jump", "light", "dark",
    "dog", "cat", "fox", "wolf", "bird", "fish", "boat", "road", "home", "city",
    "cup", "book", "code", "key", "lock", "safe", "mind", "note", "song", "frame"
]

SHORT_WORDS = [w for w in COMMON_WORDS if len(w) <= 4]

DICEWARE = [
    "alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel",
    "india", "junior", "kilo", "lima", "mike", "november", "oscar", "papa",
    "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey"
]

VOWELS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"

# ---------------------- Utilities ----------------------
def secure_random_float() -> float:
    return secrets.randbelow(1000) / 1000.0

def random_digits(length: int = 2) -> str:
    return ''.join(secrets.choice(string.digits) for _ in range(length))

def misspell_word(word: str) -> str:
    replacements = {"a": "@", "o": "0", "i": "1", "e": "3", "s": "$", "t": "7"}
    result = ""
    for char in word:
        if char.lower() in replacements and secure_random_float() < 0.4:
            result += replacements[char.lower()]
        elif secure_random_float() < 0.1:
            result += char.upper()
        else:
            result += char
    return result

def sentence_abbreviation(sentence: str) -> str:
    words = sentence.split()
    abbr = ''.join(word[0].upper() if secure_random_float() < 0.6 else word[0].lower() for word in words)
    if secure_random_float() < 0.7:
        abbr += random_digits(2)
    if secure_random_float() < 0.5:
        abbr += secrets.choice("!@#")
    return abbr

def calculate_entropy(password: str) -> float:
    pool_size = 0
    if any(c.islower() for c in password): pool_size += 26
    if any(c.isupper() for c in password): pool_size += 26
    if any(c.isdigit() for c in password): pool_size += 10
    if any(c in string.punctuation for c in password): pool_size += 32
    
    if pool_size == 0: return 0.0
    # Entropy formula: $$E = L \times \log_2(R)$$
    return len(password) * math.log2(pool_size)

def estimate_crack_time(entropy: float) -> str:
    guesses_per_second = 10**10 # Assume powerful offline attacker
    seconds = (2 ** entropy) / guesses_per_second
    
    if seconds < 1: return "Instant"
    if seconds < 60: return "Seconds"
    if seconds < 3600: return "Minutes"
    if seconds < 86400: return "Hours"
    if seconds < 31536000: return "Days"
    if seconds < 31536000 * 100: return "Years"
    return "Centuries"

def evaluate_password_strength(password: str) -> dict:
    if not password.strip():
        return {"score": 0, "desc": "Empty", "entropy": 0, "crack_time": "-", "memory": "Easy", "typing": "Easy"}
    
    # Base Score
    score = 0
    length = len(password)
    score += min(40, length * 4)
    if any(c.islower() for c in password) and any(c.isupper() for c in password): score += 15
    if any(c.isdigit() for c in password): score += 15
    if any(c in string.punctuation for c in password): score += 20
    score = max(0, min(100, score))

    if score < 40: strength = "Weak"
    elif score < 65: strength = "Moderate"
    elif score < 85: strength = "Strong"
    else: strength = "Very Strong"

    # Entropy
    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)

    # Memory Score
    memory_score = "Hard"
    if any(w in password.lower() for w in COMMON_WORDS): memory_score = "Easy"
    elif length < 10 and len([c for c in password if c in string.punctuation]) <= 1: memory_score = "Medium"

    # Typing Score
    typing_score = "Easy"
    hard_letters = "qzxw"
    symbol_count = len([c for c in password if c in string.punctuation])
    if any(c.lower() in hard_letters for c in password) or symbol_count > 2:
        typing_score = "Medium"
    if symbol_count > 4 or (any(c.islower() for c in password) and any(c.isupper() for c in password) and symbol_count > 2):
        typing_score = "Hard"

    return {
        "score": score, "desc": strength, "entropy": entropy, 
        "crack_time": crack_time, "memory": memory_score, "typing": typing_score
    }

# ---------------------- Password Generators ----------------------
def generate_three_words(avoid_hard: bool, count: int = 3, digits: int = 2) -> str:
    pool = SHORT_WORDS if avoid_hard else COMMON_WORDS
    words = [secrets.choice(pool) for _ in range(count)]
    return '-'.join(words) + '-' + random_digits(digits)

def generate_pattern(digits: int = 2) -> str:
    animals = ["dog", "cat", "fox", "wolf", "bird", "fish"]
    colors = ["blue", "red", "green", "black", "white"]
    return secrets.choice(animals) + secrets.choice(colors).capitalize() + random_digits(digits)

def generate_misspelled(avoid_hard: bool, digits: int = 2) -> str:
    pool = SHORT_WORDS if avoid_hard else COMMON_WORDS
    word = secrets.choice(pool)
    return misspell_word(word) + random_digits(digits)

def generate_abbreviation() -> str:
    sentences = [
        "I love black coffee",
        "Never stop learning",
        "Build secure things",
        "Keep it simple stupid",
        "Time is money",
        "Stay curious always",
        "Think different"
    ]
    return sentence_abbreviation(secrets.choice(sentences))

def generate_diceware(count: int = 4) -> str:
    return '-'.join(secrets.choice(DICEWARE) for _ in range(count))

def generate_pronounceable(length: int = 8, digits: int = 2) -> str:
    word = ""
    for i in range(length):
        word += secrets.choice(CONSONANTS) if i % 2 == 0 else secrets.choice(VOWELS)
    return word + random_digits(digits)

# ---------------------- Main App ----------------------
class ThughLockApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("ThughLock 🔐 - Smart Password Generator")
        self.geometry("1100x750")
        self.minsize(1000, 700)

        if os.path.exists(APP_ICON):
            try:
                self.iconbitmap(APP_ICON)
            except:
                pass

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.password_var = tk.StringVar()
        self.password_var.trace("w", self.on_password_change)

        self.session_passwords = set()
        self.history_list = []
        self.clipboard_clear_job = None
        self.clipboard_countdown = 0

        self._build_sidebar()
        self._build_main_area()
        self._load_logo()
        self._setup_shortcuts()

        self.generate_password()

    def _setup_shortcuts(self):
        self.bind("<Control-g>", lambda e: self.generate_password())
        self.bind("<Control-c>", lambda e: self.copy_to_clipboard())
        self.bind("<Control-m>", lambda e: self.mutate_word_action())

    def on_password_change(self, *args):
        current_pw = self.password_var.get()
        stats = evaluate_password_strength(current_pw)
        
        if not current_pw.strip():
            self.strength_text.configure(text="Strength: —")
            self.strength_bar.set(0)
            self.strength_bar.configure(progress_color="#666666")
            self.stats_label.configure(text="Entropy: 0 bits | Crack time: - | Memory: - | Typing: -")
        else:
            self.strength_text.configure(text=f"Strength: {stats['desc']} ({stats['score']})")
            self.strength_bar.set(stats['score'] / 100)
            color = "#ff4444" if stats['score'] < 40 else "#ffbb33" if stats['score'] < 65 else "#00C851"
            self.strength_bar.configure(progress_color=color)
            
            stats_text = (f"Entropy: {stats['entropy']:.1f} bits | "
                          f"Crack Time: {stats['crack_time']} | "
                          f"Memory: {stats['memory']} | "
                          f"Typing: {stats['typing']}")
            self.stats_label.configure(text=stats_text)

    def _load_logo(self):
        try:
            if os.path.exists(LOGO_IMAGE_PATH):
                image = Image.open(LOGO_IMAGE_PATH)
                self.logo_ctk = ctk.CTkImage(light_image=image, dark_image=image, size=(140, 140))
                self.logo_label.configure(image=self.logo_ctk, text="")
            else:
                raise FileNotFoundError
        except:
            self.logo_label.configure(text="🔒\nThughLock", font=ctk.CTkFont(size=22, weight="bold"))

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=320, corner_radius=15)
        self.sidebar.grid(row=0, column=0, sticky="nswe", padx=(20, 10), pady=20)
        self.sidebar.grid_rowconfigure(9, weight=1)
        self.sidebar.grid_propagate(False)

        self.logo_label = ctk.CTkLabel(self.sidebar, text="", width=140, height=140)
        self.logo_label.grid(row=0, column=0, pady=(30, 10), padx=20)

        title = ctk.CTkLabel(self.sidebar, text="Password Style", font=ctk.CTkFont(size=17, weight="bold"))
        title.grid(row=1, column=0, pady=(5, 10), padx=30, sticky="w")

        self.mode_var = tk.StringVar(value="Three Words")
        modes = [
            ("Three Words + Number", "Three Words"),
            ("Four Human Words", "Human Words"),
            ("Animal + Color Pattern", "Pattern"),
            ("Misspelled Word", "Mis-Spell"),
            ("Sentence Abbreviation", "Abbrev"),
            ("Diceware Style", "Diceware"),
            ("Pronounceable", "Pronounceable")
        ]

        for i, (text, value) in enumerate(modes):
            rb = ctk.CTkRadioButton(
                self.sidebar,
                text=text,
                variable=self.mode_var,
                value=value,
                font=ctk.CTkFont(size=14),
                radiobutton_width=20,
                radiobutton_height=20
            )
            rb.grid(row=2 + i, column=0, sticky="w", padx=40, pady=6)

        # Mutator Section
        mutator_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        mutator_frame.grid(row=10, column=0, padx=25, pady=5, sticky="we")
        
        self.mutate_entry = ctk.CTkEntry(mutator_frame, placeholder_text="Base word to mutate...", width=160)
        self.mutate_entry.pack(side="left", padx=(0, 5))
        ctk.CTkButton(mutator_frame, text="Mutate", width=60, command=self.mutate_word_action).pack(side="left")

        # Settings
        settings_frame = ctk.CTkFrame(self.sidebar, corner_radius=12)
        settings_frame.grid(row=11, column=0, padx=25, pady=(15, 25), sticky="we")

        self.avoid_hard_var = tk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            settings_frame,
            text="Avoid hard-to-type letters",
            variable=self.avoid_hard_var,
            font=ctk.CTkFont(size=13)
        ).pack(padx=20, pady=15, anchor="w")

        ctk.CTkLabel(settings_frame, text="Trailing digits count:", font=ctk.CTkFont(size=13)).pack(padx=20, pady=(5, 5), anchor="w")

        self.digits_var = ctk.IntVar(value=2)
        slider = ctk.CTkSlider(
            settings_frame,
            from_=1,
            to=6,
            number_of_steps=5,
            variable=self.digits_var,
            width=220
        )
        slider.pack(padx=20, pady=(0, 10))

        self.digits_label = ctk.CTkLabel(settings_frame, text="2 digits", font=ctk.CTkFont(size=12))
        self.digits_label.pack(padx=20, anchor="w")
        self.digits_var.trace("w", lambda *_: self.digits_label.configure(text=f"{self.digits_var.get()} digit{'s' if self.digits_var.get() > 1 else ''}"))

    def _build_main_area(self):
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, sticky="nswe", padx=(10, 20), pady=20)
        self.main_frame.grid_rowconfigure(4, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        top_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        top_bar.grid(row=0, column=0, sticky="we", pady=(25, 15), padx=40)
        top_bar.grid_columnconfigure(0, weight=1)

        self.generate_btn = ctk.CTkButton(
            top_bar,
            text="Generate New Password",
            command=self.generate_password,
            width=200,
            height=48,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=12
        )
        self.generate_btn.grid(row=0, column=1)

        self.copy_btn = ctk.CTkButton(
            top_bar,
            text="Copy 📋",
            command=self.copy_to_clipboard,
            width=110,
            height=48,
            font=ctk.CTkFont(size=15),
            corner_radius=12
        )
        self.copy_btn.grid(row=0, column=0, sticky="e", padx=(0, 15))

        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            textvariable=self.password_var,
            font=ctk.CTkFont(size=28, weight="bold", family="Consolas"),
            height=70,
            corner_radius=15,
            justify="center"
        )
        self.password_entry.grid(row=1, column=0, sticky="we", padx=60, pady=25)

        # Strength Bar & Stats
        strength_frame = ctk.CTkFrame(self.main_frame, corner_radius=12)
        strength_frame.grid(row=2, column=0, sticky="ew", padx=60, pady=(0, 20))
        strength_frame.grid_columnconfigure(1, weight=1)

        self.strength_text = ctk.CTkLabel(
            strength_frame,
            text="Strength: —",
            font=ctk.CTkFont(size=19, weight="bold"),
            anchor="w"
        )
        self.strength_text.grid(row=0, column=0, padx=30, pady=(15, 5), sticky="w")

        self.strength_bar = ctk.CTkProgressBar(strength_frame, height=22, corner_radius=11)
        self.strength_bar.grid(row=0, column=1, padx=(15, 30), pady=(15, 5), sticky="we")
        self.strength_bar.set(0)
        self.strength_bar.configure(progress_color="#666666")

        self.stats_label = ctk.CTkLabel(
            strength_frame,
            text="Entropy: 0 bits | Crack time: - | Memory: - | Typing: -",
            font=ctk.CTkFont(size=13),
            text_color="gray"
        )
        self.stats_label.grid(row=1, column=0, columnspan=2, pady=(0, 15))

        # History Area
        history_header = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        history_header.grid(row=3, column=0, sticky="we", padx=60, pady=(15, 8))
        history_header.grid_columnconfigure(0, weight=1)
        
        history_label = ctk.CTkLabel(history_header, text="Password History (Last 20)", font=ctk.CTkFont(size=17, weight="bold"))
        history_label.grid(row=0, column=0, sticky="w")
        
        self.clear_hist_btn = ctk.CTkButton(history_header, text="Clear History", width=100, height=28, command=self.clear_history)
        self.clear_hist_btn.grid(row=0, column=1, sticky="e")

        self.history_textbox = ctk.CTkTextbox(
            self.main_frame,
            font=ctk.CTkFont(size=14, family="Consolas"),
            corner_radius=12
        )
        self.history_textbox.grid(row=4, column=0, sticky="nswe", padx=60, pady=(0, 20))
        self.history_textbox.configure(state="disabled")

        # Bottom Bar
        bottom_bar = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        bottom_bar.grid(row=5, column=0, sticky="we", padx=60, pady=(0, 25))
        bottom_bar.grid_columnconfigure(2, weight=1)

        ctk.CTkButton(bottom_bar, text="Evaluate Current", command=self.evaluate_current, width=150, corner_radius=10).pack(side="left")
        ctk.CTkButton(bottom_bar, text="Export to TXT", command=self.export_history, width=120, corner_radius=10).pack(side="left", padx=15)
        
        self.clipboard_status = ctk.CTkLabel(bottom_bar, text="", text_color="gray", font=ctk.CTkFont(size=12))
        self.clipboard_status.pack(side="right")

    def mutate_word_action(self):
        base_word = self.mutate_entry.get().strip()
        if not base_word:
            messagebox.showwarning("Empty", "Enter a base word to mutate!")
            return
        
        # Simple Mutator: dragon -> Dr@g0n!82
        replacements = {'a': '@', 'o': '0', 'i': '1', 'e': '3', 's': '$', 't': '7'}
        mutated = ""
        for i, char in enumerate(base_word):
            if char.lower() in replacements:
                mutated += replacements[char.lower()]
            elif i == 0:
                mutated += char.upper()
            else:
                mutated += char.lower() if secure_random_float() < 0.8 else char.upper()
                
        mutated += secrets.choice("!@#$%&*") + random_digits(self.digits_var.get())
        
        self.password_var.set(mutated)
        self.add_to_history(mutated)

    def generate_password(self):
        mode = self.mode_var.get()
        avoid_hard = self.avoid_hard_var.get()
        digits = self.digits_var.get()

        for _ in range(10): # Try up to 10 times to prevent duplicates
            if mode == "Human Words": pw = generate_three_words(avoid_hard, count=4, digits=digits)
            elif mode == "Three Words": pw = generate_three_words(avoid_hard, count=3, digits=digits)
            elif mode == "Pattern": pw = generate_pattern(digits=digits)
            elif mode == "Mis-Spell": pw = generate_misspelled(avoid_hard, digits=digits)
            elif mode == "Abbrev": pw = generate_abbreviation()
            elif mode == "Diceware": pw = generate_diceware(count=4)
            elif mode == "Pronounceable": pw = generate_pronounceable(length=8, digits=digits)
            else: pw = generate_three_words(avoid_hard, count=3, digits=digits)

            if secure_random_float() < 0.3 and not any(c in string.punctuation for c in pw):
                pw += secrets.choice("!@#$%&*")
                
            if pw not in self.session_passwords:
                break

        self.session_passwords.add(pw)
        self.password_var.set(pw)
        self.add_to_history(pw)

    def copy_to_clipboard(self):
        pw = self.password_var.get().strip()
        if not pw:
            messagebox.showwarning("Empty", "Generate a password first!")
            return
        self.clipboard_clear()
        self.clipboard_append(pw)
        
        self.clipboard_countdown = 30
        self._update_clipboard_status()

    def _update_clipboard_status(self):
        if self.clipboard_clear_job:
            self.after_cancel(self.clipboard_clear_job)
            
        if self.clipboard_countdown > 0:
            self.clipboard_status.configure(text=f"Clipboard clears in {self.clipboard_countdown}s")
            self.clipboard_countdown -= 1
            self.clipboard_clear_job = self.after(1000, self._update_clipboard_status)
        else:
            self.clipboard_clear()
            self.clipboard_status.configure(text="Clipboard cleared")
            self.clipboard_clear_job = self.after(3000, lambda: self.clipboard_status.configure(text=""))

    def evaluate_current(self):
        pw = self.password_var.get().strip()
        if not pw:
            messagebox.showwarning("No Password", "Generate or enter a password first!")
            return
        stats = evaluate_password_strength(pw)
        msg = (f"Strength: {stats['desc']}\n"
               f"Score: {stats['score']}/100\n"
               f"Entropy: {stats['entropy']:.1f} bits\n"
               f"Estimated Crack Time: {stats['crack_time']}\n"
               f"Memorability: {stats['memory']}\n"
               f"Typing Difficulty: {stats['typing']}")
        messagebox.showinfo("Detailed Evaluation", msg)

    def add_to_history(self, password: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        entry = f"{timestamp} → {password}"
        self.history_list.insert(0, entry)
        
        if len(self.history_list) > 20:
            self.history_list.pop()
            
        self._refresh_history_ui()

    def clear_history(self):
        self.history_list.clear()
        self._refresh_history_ui()

    def _refresh_history_ui(self):
        self.history_textbox.configure(state="normal")
        self.history_textbox.delete("1.0", "end")
        self.history_textbox.insert("end", f"Session started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for item in self.history_list:
            self.history_textbox.insert("end", item + "\n")
        self.history_textbox.configure(state="disabled")

    def export_history(self):
        if not self.history_list:
            messagebox.showwarning("Empty History", "No passwords to export yet.")
            return
        content = "\n".join(self.history_list)
        filename = f"ThughLock_History_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write("ThughLock - Password History\n")
                f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                f.write(content)
            messagebox.showinfo("Exported", f"History saved to:\n{filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export:\n{e}")

# ---------------------- Run ----------------------
if __name__ == "__main__":
    app = ThughLockApp()
    app.mainloop()
