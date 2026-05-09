# ThughLock 🔐 - Smart Password Generator V3.0

![Version](https://img.shields.io/badge/version-V3.0-blue.svg)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python Version](https://img.shields.io/badge/python-3.8%2B-yellow.svg)
![CustomTkinter](https://img.shields.io/badge/UI-CustomTkinter-blueviolet.svg)
![Security](https://img.shields.io/badge/security-Cryptographically_Secure-red.svg)

Welcome to **ThughLock**, an advanced, open-source desktop password generator built entirely in Python. Designed for both security and usability, ThughLock creates passwords that are highly secure against brute-force attacks yet easy for humans to remember and type.

**Developed by:** [Ali Kamrani (MRThugh)](https://github.com/MRThugh)

---

## 🚀 What's New in V3.0?

Version 3.0 is a massive rewrite focused on cryptographic security and deep password analysis, while maintaining its sleek, single-file architecture.

### ✨ Key Features

*   **Cryptographically Secure:** Replaced standard pseudo-random generators with Python's `secrets` module to ensure cryptographically strong, unpredictable passwords.
*   **Deep Strength Analysis:** Real-time calculation of **Entropy** (in bits) and **Estimated Crack Time** against offline brute-force attacks.
*   **Memorability & Typing Scores:** The AI-inspired evaluation engine now rates how hard a password is to memorize and how difficult it is to type on a standard keyboard.
*   **Password Mutation Tool:** Enter a base word (e.g., `dragon`) and instantly mutate it into a secure, complex format (e.g., `Dr@g0n!82`).
*   **Pronounceable Passwords:** A new generator mode that uses alternating consonant-vowel structures to create memorable, pseudo-words.
*   **Auto-Clearing Clipboard:** For maximum security, passwords copied to the clipboard are automatically wiped after 30 seconds, accompanied by a live countdown timer.
*   **Smart History Management:** Keeps track of your last 20 generated passwords, prevents duplicates in a single session, and allows exporting to a `.txt` file.
*   **Keyboard Shortcuts:** Full workflow optimization with shortcuts: `Ctrl+G` (Generate), `Ctrl+C` (Copy), and `Ctrl+M` (Mutate).
*   **Beautiful Dark UI:** Powered by CustomTkinter, featuring a smooth, modern dark-mode interface.

---

## 🧠 How the Code Works

ThughLock is designed as a monolithic, dependency-free (aside from CustomTkinter and Pillow) application for easy auditing and deployment.

### 1. Cryptography (`secrets` module)
All random generation uses the `secrets` module. For example, `secure_random_float()` uses `secrets.randbelow()` to generate highly unpredictable float values, crucial for randomized capitalization, symbol insertion, and dice-ware selections.

### 2. Password Entropy & Math
The application evaluates password strength using Shannon Entropy. The formula used under the hood is:

$$ E = L \times \log_2(R) $$

Where:
*   $E$ = Entropy in bits
*   $L$ = Length of the password
*   $R$ = Pool size of characters used (e.g., lowercase, uppercase, digits, symbols)

The crack time is then estimated by assuming an attacker can make $10^{10}$ guesses per second: $\text{Seconds} = \frac{2^E}{10^{10}}$.

### 3. Smart Generators
The codebase includes multiple distinct generator functions:
*   `generate_three_words()`: Uses curated lists of common/short words.
*   `generate_pronounceable()`: Loops through string combinations of `VOWELS` and `CONSONANTS`.
*   `generate_diceware()`: Pulls from a standard Diceware wordlist.
*   **Mutator**: Iterates through strings replacing specific characters based on a predefined dictionary (`{'a': '@', 's': '$'...}`) and random capitalization based on a secure probability curve.

### 4. UI Architecture
The UI is an object-oriented `ctk.CTk` subclass. It uses a grid layout separated into a `_build_sidebar()` for settings/modes and `_build_main_area()` for display and real-time interaction using `tk.StringVar().trace()`.

---

## ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/MRThugh/ThughLock.git
   cd ThughLock
   ```

2. **Install requirements:**
   You only need `customtkinter` and `Pillow`.
   ```bash
   pip install customtkinter Pillow
   ```

3. **Run the App:**
   ```bash
   python main.py
   ```

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE). You are free to copy, modify, and distribute the software.

---

## 👤 Author

**Ali Kamrani**
*   GitHub: [@MRThugh](https://github.com/MRThugh)

*If you find this tool helpful, please consider giving the repository a ⭐ on GitHub!*
