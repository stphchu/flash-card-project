from tkinter import *
import pandas
import random
import shutil
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
TITLE = ("Ariel", 40, "italic")
WORD = ("Ariel", 60, "bold")
TO_LEARN_FILE_PATH = "data/words_to_learn.csv"
ORIGINAL_FILE_PATH = "data/french_words.csv"
DELAY_TIME = 3000


data = None
current_card = {}


try:
    data = pandas.read_csv(TO_LEARN_FILE_PATH)
except FileNotFoundError:
    shutil.copyfile(ORIGINAL_FILE_PATH, TO_LEARN_FILE_PATH)
    data = pandas.read_csv(TO_LEARN_FILE_PATH)
finally:
    if not any(line.strip() for line in open(TO_LEARN_FILE_PATH)):
        raise Exception("File is empty. Please delete or edit.")
    dataframe = pandas.DataFrame(data).to_dict(orient="records")
    csv_column_1_header = data.columns[0]
    csv_column_2_header = data.columns[1]


def card_front_format():
    canvas.itemconfig(card, image=card_front_image)
    canvas.itemconfig(title, fill="black")
    canvas.itemconfig(word, fill="black")


def card_back_format():
    canvas.itemconfig(card, image=card_back_image)
    canvas.itemconfig(title, fill="white")
    canvas.itemconfig(word, fill="white")


def next_card():
    global current_card, timer
    card_front_format()
    window.after_cancel(timer)
    try:
        current_card = random.choice(dataframe)
    except (IndexError, ValueError):
        messagebox.showinfo(message="No more remaining items on the list")
    else:
        canvas.itemconfig(title, text=f"{csv_column_1_header}")
        canvas.itemconfig(word, text=f"{current_card[csv_column_1_header]}")
        timer = window.after(DELAY_TIME, flip_card, current_card)


def flip_card(current_card_data):
    card_back_format()
    canvas.itemconfig(title, text=f"{csv_column_2_header}")
    canvas.itemconfig(word, text=f"{current_card_data[csv_column_2_header]}")


def know():
    try:
        dataframe.remove(current_card)
    except (IndexError, ValueError):
        messagebox.showinfo(message="No more remaining items on the list")
    else:
        pandas.DataFrame(dataframe).to_csv(TO_LEARN_FILE_PATH, index=False)
        next_card()


window = Tk()
window.title("Flashy")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)

canvas = Canvas()
canvas.config(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
card_front_image = PhotoImage(file="images/card_front.png")
card = canvas.create_image(400, 263, image=card_front_image)

card_back_image = PhotoImage(file="images/card_back.png")

wrong_button_img = PhotoImage(file="images/wrong.png")
right_button_img = PhotoImage(file="images/right.png")
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=next_card)
right_button = Button(image=right_button_img, highlightthickness=0, command=know)
wrong_button.grid(column=0, row=1)
right_button.grid(column=1, row=1)

title = canvas.create_text(400, 150, text="", font=TITLE)
word = canvas.create_text(400, 263, text="", font=WORD)

timer = window.after(DELAY_TIME, flip_card, current_card)
next_card()

window.mainloop()
