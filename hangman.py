import os
import platform
import sys
import nltk
import time
import random


from nltk.corpus import words

english_words = set(words.words())
AI_SAVEFILE = r"E:\Programming\Python\Hangman\ai_save.txt"

def clear_terminal():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def get_input(prompt, expected_type):
    print(prompt)
    # Mapping from Python types to friendly descriptions
    friendly_names = {
        int: "whole number",
        float: "decimal number",
        str: "text",
        bool: "true/false value"
    }

    while True:
        try:
            # Get input from user and try to convert to the expected type
            value = input("> ")
            if value.lower() in ["admin quit", "adm quit", "adm qt", "admin qt", "adminquit", "admquit", "admqt", "adminqt"]:
                sys.exit()
            
            # Special case for bool
            if expected_type == bool:
                if value.lower() in ["true", "t", "yes", "y", "1"]:
                    return True
                elif value.lower() in ["false", "f", "no", "n", "0"]:
                    return False
                else:
                    raise ValueError("Not a valid boolean.")
            
            return expected_type(value)
        
        except ValueError:
            print(f"Please enter a valid {friendly_names.get(expected_type, 'value')}.")

def update_word_memory(word):
    word = word.lower()
    words = {}

    # Read existing data
    try:
        with open(AI_SAVEFILE, "r") as f:
            for line in f:
                w, count = line.strip().split(":")
                words[w] = int(count)
    except FileNotFoundError:
        pass

    # Update or add new word
    words[word] = words.get(word, 0) + 1

    # Write back
    with open(AI_SAVEFILE, "w") as f:
        for w, count in words.items():
            f.write(f"{w}:{count}\n")

def setup():
    word = "asdfasdfsdaffdaasdfaffaa"
    word = get_input("What should the word be?", str)
    while word not in english_words:
        print("Sorry, that word is not in the version of the English dictionary being used by this script. Please select another word.")
        word = get_input("What should the word be?", str)
    return(word)

def smart_guess_from_history(pattern, incorrect_letters):
    possible = []
    with open(AI_SAVEFILE, "r") as f:
        for line in f:
            word, count = line.strip().split(":")
            count = int(count)

            if len(word) != len(pattern):
                continue
            if any(letter in incorrect_letters for letter in word):
                continue
            if any(pattern[i] != "_" and pattern[i] != word[i] for i in range(len(pattern))):
                continue
            possible.append((count, word))
    
    if possible:
        possible.sort(reverse=True)
        return(possible[0][1])
    
    return(None)

def get_guess_for_bot(guesses, correct_letters, length, incorrect_words):
    incorrect_letters = [g for g in guesses if g not in correct_letters]
    pattern = "".join([c if c != "" else "_" for c in correct_letters])

    # Try smart AI history guess
    smart_guess = smart_guess_from_history(pattern, incorrect_letters)
    if smart_guess:
        return (True, smart_guess)
    common_letters = "etaoinsrhldcumfpgwybvkxjqz"

    def matches_pattern(word):
        for i, c in enumerate(correct_letters):
            if c != "" and word[i] != c:
                return False
        if any(letter in word for letter in incorrect_letters):
            return False
        return True

    possible_words = [w for w in english_words if len(w) == length and matches_pattern(w) and w not in incorrect_words]

    if 1 <= len(possible_words) <= 5:
        # Score by number of matching positions + common letters
        def score_word(word):
            pattern_score = sum(1 for i, c in enumerate(correct_letters) if c != "" and word[i] == c)
            freq_score = sum(26 - common_letters.index(c) if c in common_letters else 0 for c in set(word) if c not in guesses)
            return pattern_score * 100 + freq_score  # prioritize pattern match, then frequency

        possible_words.sort(key=score_word, reverse=True)
        return (True, possible_words[0])

    # Letter frequency scoring
    letter_counts = {}
    for word in possible_words:
        for letter in set(word):
            if letter not in guesses:
                letter_counts[letter] = letter_counts.get(letter, 0) + 1

    if letter_counts:
        best_letter = max(letter_counts, key=letter_counts.get)
        return (False, best_letter)

    for letter in common_letters:
        if letter not in guesses:
            return (False, letter)

    return (False, "?")

for i in range(3):
    print("\033[1mINITIALIZING HANGMAN.\033[0m")
    time.sleep(0.5)
    clear_terminal()
    print("\033[1mINITIALIZING HANGMAN..\033[0m")
    time.sleep(0.5)
    clear_terminal()
    print("\033[1mINITIALIZING HANGMAN...\033[0m")
    time.sleep(0.5)
    clear_terminal()

print("\033[1mInitialized and done!\033[0m")

man = {
    0 : 
    r"""
    ------- 
    |      |
    |      O
    |     /|\
    |     / \
    |
    |
 ============
""",
1 : 
    r"""
    ------- 
    |      |
    |      O
    |     /|\
    |     / 
    |
    |
 ============
""",
2 : 
    r"""
    ------- 
    |      |
    |      O
    |     /|\
    |     
    |
    |
 ============
""",
3 : 
    r"""
    ------- 
    |      |
    |      O
    |     /|
    |     
    |
    |
 ============
""",
4 : 
    r"""
    ------- 
    |      |
    |      O
    |     /
    |     
    |
    |
 ============
""",
5 : 
    r"""
    ------- 
    |      |
    |      O
    |     
    |     
    |
    |
 ============
""",
6 : 
    r"""
    ------- 
    |      |
    |      
    |     
    |     
    |
    |
 ============
""",
}

while True:
    bot_mode = get_input("Would you like to play against the computer?", bool)

    if bot_mode:
        if get_input("Do you want the bot to be guessing? If not, the bot will pick a word for you. (Yes = guessing, no = picks word)", bool):
            if get_input("Do you want the bot to guess a random word? If not, the bot will guess a word given by you. (Yes = random, no = you pick)", bool):
                correct_word = random.choice(list(english_words))
            else:
                correct_word = setup().lower()
            bot_mode = True       
        else:
            bot_mode = False
            correct_word = random.choice(list(english_words))
    else:
        correct_word = setup().lower()

    print(f"The word is {correct_word}.")

    lives = 6

    guessed_letters = []

    wrong_words = []

    word = ""

    win = False

    correct_letters_in_word = [""] * len(correct_word)

    rounds = 0

    for i in range(3):
        print(f"Clearing word in {3 - i}")
        time.sleep(1)
        clear_terminal()

    while lives > 0:
        rounds += 1
        print(man[lives], end=" ")
        if win:
            print("")
            if bot_mode:
                print(f"BOT GUESSED WORD WITH {lives}/6 LIVES REMAINING - WORD WAS {correct_word} - GUESSED IN {rounds - 1} ROUNDS!")
            else:
                print(f"Congratulations! You guessed the word correctly with {lives}/6 lives remaining! The word was {correct_word}. You guessed it in {rounds - 1} rounds.")
            break
        elif lives == 0:
            if bot_mode:
                print(f"BOT LOST - WORDS WAS {word}")
            else:
                print(f"Man! You lost! The word was {word}.")
        print("   ", end=" ")
        for i in range(len(correct_word)):
            if correct_letters_in_word[i] != "":
                print(''.join(correct_letters_in_word[i] + '\u0332'), end=" ")
            else:
                print("_", end=" ")
        print("")
        print("Guessed letters:")
        for i in range(len(guessed_letters)):
            if i % 5 == 0 and i != 0:
                print(f"{guessed_letters[i].upper()}  ")
            else:
                print(f"{guessed_letters[i].upper()}  ", end=" ")
        print("")
        print(f"Length - {len(correct_word)}")
        if not bot_mode:
            guess_type = get_input("Would you like to guess the word? If not, would you like to guess a letter? (Yes for word, no for letter)", bool)
        else:
            guess_type, guess = get_guess_for_bot(guessed_letters, correct_letters_in_word, len(correct_word), wrong_words)
        if guess_type:
            if bot_mode:
                word = guess
            else:
                word = get_input("What is your guess?", str)
            if word.lower() == correct_word:
                win = True
            else:
                lives -= 1
                wrong_words.append(word)
                if bot_mode:
                    print(f"BOT GUESSED {word.upper()} (INCORRECT). BOT HAS {lives}/6 LIVES LEFT.")
                else:
                    print(f"Man! {word} wasn't the correct word! You have {lives}/6 lives left.")
        else:
            if bot_mode:
                letter = guess
            else:
                letter = get_input("What letter would you like to guess?", str).lower()
            while letter in guessed_letters:
                print("You have already guessed that letter. Please pick another.")
                letter = get_input("What letter would you like to guess?", str).lower()
            guessed_letters.append(letter)
            if letter in correct_word:
                if bot_mode:
                    print(f"BOT GUESSED {letter.upper()} (CORRECT). BOT HAS {lives}/6 LIVES LEFT.")
                else:
                    print(f"Yup! {letter.upper()} is in the word!")
                for i in range(len(correct_word)):
                    if correct_word[i] == letter:
                        correct_letters_in_word[i] = letter
            else:
                lives -= 1
                if bot_mode:
                    print(f"BOT GUESSED {letter.upper()} (INCORRECT). BOT HAS {lives}/6 LIVES LEFT.")
                else:
                    print(f"Man! {letter.upper()} wasn't in the word!")
            if "".join(correct_letters_in_word) == correct_word:
                win == True
        # region redraw
        clear_terminal()
        print(man[lives], end=" ")
        if win:
            print("")
            print(f"Congratulations! You guessed the word correctly with {lives}/6 lives remaining! The word was {correct_word}.")
            break
        elif lives == 0:
            print(f"Man! You lost! The word was {correct_word}.")
        print("   ", end=" ")
        for i in range(len(correct_word)):
            if correct_letters_in_word[i] != "":
                print(''.join(correct_letters_in_word[i] + '\u0332'), end=" ")
            else:
                print("_", end=" ")
        print("")
        print("Guessed letters:")
        for i in range(len(guessed_letters)):
            if i % 5 == 0 and i != 0:
                print(f"{guessed_letters[i].upper()}  ")
            else:
                print(f"{guessed_letters[i].upper()}  ", end=" ")
        print("")
        print(f"Length - {len(correct_word)}")
        if guess_type:
            if bot_mode:
                print(f"BOT GUESSED {word.upper()} (INCORRECT). BOT HAS {lives}/6 LIVES LEFT.")
            else:
                print(f"Man! {word} wasn't the correct word! You have {lives}/6 lives left.")
        else:
            if letter in correct_word:
                if bot_mode:
                    print(f"BOT GUESSED {letter.upper()} (CORRECT). BOT HAS {lives}/6 LIVES LEFT.")
                else:
                    print(f"Yup! {letter.upper()} is in the word!")
            else:
                if bot_mode:
                    print(f"BOT GUESSED {letter.upper()} (INCORRECT). BOT HAS {lives}/6 LIVES LEFT.")
                else:
                    print(f"Man! {letter.upper()} wasn't in the word!")
        # endregion
        get_input("Are you ready to proceed to the next guess?", any)
        clear_terminal()
    update_word_memory(correct_word)
    if not get_input("Do you want to play again?", bool):
        break
