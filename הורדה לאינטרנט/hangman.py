from pyscript import document, window
import random
# הוספת ה-: any אומרת ל-VS Code: "תניח שזה יכול להיות כל דבר, תציע לי הכל"
reset = document.querySelector("#play-again")
reset.style.display = 'none'
msg_box: any = document.querySelector("#message-box")
input_el: any = document.querySelector("#user-letter")
file_path = "words.txt"
num_of_tries = 0
remaining_attempts = 9
old_letters_guessed = []
word = document.querySelector("#secret-word")
remaining = document.querySelector("#remaining-attempts")
btn = document.querySelector("#start-game")
HANGMAN_PHOTOS = {
0: """x-------x"""
, 1: """x-------x
|
|
|
|
|"""
, 2: """x-------x
|           |
|           
|
|
|"""
, 3: """x-------x
|           |
|           0
|           
|
|"""
, 4: """x-------x
|           |
|           0
|           |
|
|
""" 
, 5: """x-------x
|           |
|           0
|          /|
|
|
""" 
, 6: """x-------x
|           |
|           0
|          /|\\
|
|
""" 
, 7: """x-------x
|           |
|           0
|          /|\\
|          /
|
""" 
, 8:  """x-------x
|           |
|           0
|          /|\\
|          / \\
|
"""
, 9: """x-------x
|           |
|           |
|           |
|           0
|          /|\\
|          / \\
"""}  
pic_tree = document.querySelector('#tree')
pic_tree.innerText = HANGMAN_PHOTOS[num_of_tries]


# עכשיו כשתיגש אליהם:
# msg_box. -> יציע innerText, innerHTML, style...
# input_el. -> יציע value, type, placeholder...
def choose_word(file_path):
    with open(file_path, 'r', encoding='utf-8') as take_word:
        list_of_words = take_word.read().split()
        the_word = random.choice(list_of_words)   
    
    word.innerText = '_ '  * len(the_word)
    return the_word
SECRET_WORD = choose_word(file_path)

def handle_keypress(event):
    # בודקים אם המקש שנלחץ הוא Enter
    if event.key == "Enter":
        # מונעים מהדף להתרענן (סטנדרט בדפדפנים)
        event.preventDefault()
        start_game(event)

def start_game(event):
    global old_letters_guessed
    letter = document.querySelector("#guess-letter")
    old_letters = document.querySelector("#letters-guessed")
    if not check_valid_input(letter, old_letters_guessed):
        return 
    old_letters_guessed += [letter.value.lower()]
    show_hidden_word(SECRET_WORD, letter, word, remaining) 
    old_letters.innerText = 'letter that you guessed:' +'\n' + str(old_letters_guessed)
    letter.value = ''

def check_valid_input(letter, old_letters_guessed):
    last_letters = ['ן','ם','ף','ץ','ך']
    if letter.value == '':
        window.alert('לא הוזנה אות לניחוש.') 
        return False
    elif letter.value.isalpha() == True and letter.value not in old_letters_guessed and letter.value not in last_letters:
        return True
    else:
        window.alert('האות שהוזנה אינה תקינה.')
        letter.value = ''
        return False 
    

def show_hidden_word(SECRET_WORD, letter, word, remaining):
    global num_of_tries
    global pic_tree
    global remaining_attempts
    current_guess = letter.value.lower() # עבודה עם אותיות קטנות למניעת טעויות
    
    # 1. בדיקה האם הניחוש הנוכחי נכון או טעות
    if current_guess in SECRET_WORD.lower():
        letter.style.backgroundColor = 'green'
    else:
        letter.style.backgroundColor = 'red'
        num_of_tries += 1
        remaining_attempts -= 1
        pic_tree.innerText = HANGMAN_PHOTOS[num_of_tries]
        remaining.innerText = 'remaining_attempts:' + str(remaining_attempts)
        if remaining_attempts == 0:
            remaining.innerText = 'YOU LOSE!' + '\n' +'the word was: ' + '\n' + str(SECRET_WORD) 
            remaining.style.fontSize = "400%"
            btn.disabled = True
            btn.style.display = "none"
            letter.style.display = "none"
            show_reset_btn()

    # 2. בניית המחרוזת להצגה מחדש (החלק הקריטי)
    display_text = ""
    for char in SECRET_WORD:
        # אם האות היא הניחוש הנוכחי או שהיא כבר נוחשה בעבר
        if char.lower() == current_guess or char.lower() in old_letters_guessed:
            display_text += char + " "
        else:
            display_text += "_ "
    
    # עדכון ה-HTML עם המילה המעודכנת (למשל _ O _ _ )
    word.innerText = display_text.strip()
    check_win(letter, word)

def check_win(letter, word):
    for let in SECRET_WORD:
        if let not in old_letters_guessed:
            return False
    remaining.innerText = 'YOU WON!'
    global btn
    btn.style.display = "none"
    letter.style.display = "none"
    word.style.fontSize = "400%"
    show_reset_btn()

def show_reset_btn():
    reset.style.display = 'block'

def reset_game(event):
    global num_of_tries, remaining_attempts, old_letters_guessed, SECRET_WORD
    
    # 1. איפוס משתנים
    num_of_tries = 0
    remaining_attempts = 9
    old_letters_guessed = []
    
    # 2. בחירת מילה חדשה
    SECRET_WORD = choose_word(file_path)
    
    # 3. איפוס תצוגה
    remaining.innerText = 'ניסיונות נותרו: 9'
    remaining.style.fontSize = "100%"
    remaining.style.color = "black"
    pic_tree.innerText = HANGMAN_PHOTOS[0]
    btn.disabled = False
    
    # 4. החזרת אלמנטים שהסתרנו
    document.querySelector("#guess-letter").style.display = "block"
    document.querySelector("#start-game").style.display = "block"
    document.querySelector("#play-again").style.display = "none" # להסתיר את עצמו
