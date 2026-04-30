from tkinter import *
from tkinter import messagebox
from english_words import get_english_words_set
import keyboard
import random

class Screen():
    def __init__(self):
        self.window = Tk()
        self.window.title("Typing Speed Test")
        self.window.minsize(150, 150)
        self.window.config(padx=30, pady=10, bg="black")

        self.difficulty_label = Label()
        self.generated_text = Text()
        self.entry_field = Entry()
        self.entry = Entry()
        self.wpm_value = Label()
        self.cpm_value = Label()
        self.mist_value = Label()

        self.timer_text = None
        self.time = None
        self.points = 0
        self.time_start = False
        self.set_of_words = []
        self.written_words = []
        self.text = ""
        self.entry_txt = ""
        self.spelling = []
        self.spelling_points = 0
        self.words_points = 0
        self.mistakes = 0
        self.net_wpm = 0
        self.difference = 0

        with open("data.txt") as data:
            self.high_score = int(data.read())

        self.choose_difficulty()

        self.window.mainloop()

    def choose_difficulty(self):
        self.difficulty_label = Label(text="Choose a Difficulty", font=("Tahoma", 25, "bold"), bg = "#000000")
        self.difficulty_label.grid(column=0, row=0, columnspan=3, padx=50, pady=20)

        easy = Button(text="EASY", font=("Tahoma", 20, "bold"), bg="black", fg="#00e600", command=lambda: [self.create_text_easy(), easy.destroy(), hard.destroy(), info.destroy()])
        easy.grid(column=0, row=2, padx=20, pady=20)

        hard = Button(text="HARD", font=("Tahoma", 20, "bold"), bg="black", fg="#ff0000", command=lambda: [self.create_text_hard(), easy.destroy(), hard.destroy(), info.destroy()])
        hard.grid(column=2, row=2, padx=20, pady=20)

        info = Button(text="INSTRUCTION", font=("Tahoma", 8, "bold"), bg="black", fg="white", command=lambda: [self.show_info(), easy.destroy(), hard.destroy(), info.destroy()])
        info.grid(column=1, row=1)

    def show_info(self):
        self.difficulty_label.config(text="Welcome to the Typing Speed Test")
        info_text = Label(font=("Tahoma", 15), bg = "black", fg="white", anchor=W, justify="left",
                          text="This app will test your typing speed.\n"
                               "First, choose a difficulty.\n"
                               "A series of randomly chosen words will appear.\n"
                               "The timer will start when you start typing.\n"
                               "Type the words exactly as they appear, including spaces.\n"
                               "The test will automatically end when you finish typing the text.\n"
                               "Your results will appear thereafter.\n"
                               "Mistakes are counted, but you can fix them via backspace without penalty.\n"
                               "Your highscore will be saved.")

        info_text.grid(column=0, row=1, pady=20)

        back_button = Button(text="BACK", font=("Tahoma", 15, "bold"), bg="black", fg="white",
                             command=lambda: [self.clear_screen(), self.choose_difficulty(), info_text.destroy(), back_button.destroy(), self.difficulty_label.config(text="Choose a Difficulty")])
        back_button.grid(column=0, row=3)

    def clear_screen(self):
        self.difficulty_label.destroy()
        self.generated_text.destroy()

        self.entry_field.delete(0,END)

        self.set_of_words.clear()
        self.spelling.clear()

        self.text = ""
        self.spelling_points = 0

        self.window.update()

    def change_into_text(self, list_of_words):
        text = ' '.join(list_of_words)
        self.text = text
        return text

    def create_text_easy(self):
        self.clear_screen()
        self.create_widgets()

        with open("common_english_words.txt", "r") as text:
            all_text = text.read()
            words = list(map(str, all_text.split()))

            for word in range(20):
                self.set_of_words.append(random.choice(words).lower())

            self.generated_text = Text(self.window, bg="black", fg="white", font=("Arial", 20, "bold"), height=4, width=60, wrap="word")
            self.generated_text.grid(column=0, row=1, rowspan=3, columnspan=9, pady=35)
            self.generated_text.insert(END, self.change_into_text(self.set_of_words).lower())

    def create_text_hard(self):
        self.clear_screen()
        self.create_widgets()

        for word in range(20):
            self.set_of_words.append(random.choice(list(get_english_words_set(['web2'], lower=True))))

        self.generated_text = Text(self.window, bg="black", fg="white", font=("Arial", 20, "bold"), height=5, width=60, wrap="word")
        self.generated_text.grid(column=0, row=1, rowspan=3, columnspan=9, pady=35)
        self.generated_text.insert(END, self.change_into_text(self.set_of_words))

    def text_callback(self, var, index, mode):
        self.entry_txt = self.entry_field.get()
        self.check_spelling()
        self.update_screen_board()
        self.start_timer()

    def backspace(self, event):
        try:
            self.spelling.pop()
            self.spelling_points = self.count_points()
            return self.spelling, self.spelling_points
        except IndexError:
            pass

    def count_points(self):
        points = 0
        for check in self.spelling:
            if check == "ok":
                points += 1
            else:
                pass

        if len(self.spelling) == 0:
            points = 0

        return points

    def count_mistakes(self):
        mistakes = 0
        for check in self.spelling:
            if check == "wrong":
                mistakes += 1
            else:
                pass

        if len(self.spelling) == 0:
            mistakes = 0

        return mistakes

    def show_mistake(self, difference):
        entry_len = len(self.entry_txt) - 1 - difference
        self.generated_text.tag_config("#ff0000", foreground="#ff0000")
        char = self.entry_txt[len(self.entry_txt) - 1 - difference]

        self.generated_text.delete(f"1.{entry_len}", f"1.{entry_len + 1}")
        self.generated_text.insert(f"1.{entry_len}", char)
        self.generated_text.tag_add("#ff0000", f"1.{entry_len}")


    def show_correct(self, difference):
        entry_len = len(self.entry_txt) - 1 - difference
        self.generated_text.tag_config("#00e600", foreground="#00e600")
        char = self.text[len(self.entry_txt) - 1 - difference]

        self.generated_text.delete(f"1.{entry_len}", f"1.{entry_len + 1}")
        self.generated_text.insert(f"1.{entry_len}", char)
        self.generated_text.tag_add("#00e600", f"1.{entry_len}")

    def show_original_letter(self):
        self.generated_text.tag_config("white", foreground="white")
        char = self.text[len(self.entry_txt)]

        self.generated_text.delete(f"1.{len(self.entry_txt)}")
        self.generated_text.insert(f"1.{len(self.entry_txt)}", char)
        self.generated_text.tag_add("white", f"1.{len(self.entry_txt)}")

    def check_spelling(self):
        letters = []
        letters_string = ""

        number = -1
        self.points = 0

        try:
            for letter in self.entry_txt.lower():
                if letter != " ":
                    self.points += 1
                    number += 1
                else:
                    number = -1
                letters.append(letter)
                letters_string = ''.join(letters)

            self.written_words = letters_string.split(" ")
            self.words_points = len(self.written_words)

            if len(self.written_words[self.words_points - 1]) > len(self.set_of_words[self.words_points - 1]):
                number -= 1
                self.difference = len(self.written_words[self.words_points - 1]) - len(self.set_of_words[self.words_points - 1])
                self.written_words.pop()
                self.written_words.append(self.written_words[self.words_points - 1][:-self.difference])

            if keyboard.read_key() != "backspace":
                if len(self.entry_txt) == len(self.text):
                    self.time_start = False
                    self.count_score()

                if self.written_words[self.words_points - 1][number] == self.set_of_words[self.words_points - 1][number]:
                    self.spelling.append("ok")
                    self.show_correct(self.difference)
                    self.spelling_points = self.count_points()
                    self.mistakes = self.count_mistakes()
                else:
                    self.spelling.append("wrong")
                    self.show_mistake(self.difference)
                    self.spelling_points = self.count_points()
                    self.mistakes = self.count_mistakes()
            else:
                self.show_original_letter()
        except IndexError:
            pass

    def count_time(self, count):
        if self.time_start:
            self.time = self.window.after(1000, self.count_time, count + 1)
            self.timer_text['text'] = count

    def start_timer(self):
        if len(self.entry_txt) == 1:
            self.time_start = True
            self.count_time(0)
        elif len(self.entry_txt) == 0:
            self.time_start = False

    def update_screen_board(self):
        self.cpm_value['text'] = self.points

        if int(self.timer_text['text']) > 0:
            self.net_wpm = (int(((self.points / 5) - (self.mistakes * ((int(self.timer_text['text'])) / 60))) / ((int(self.timer_text['text'])) / 60)))
            self.wpm_value['text'] = f"{int((self.points / 5) / ((int(self.timer_text['text'])) / 60))}/{self.net_wpm}"

        self.mist_value['text'] = self.mistakes

        if int(self.mist_value['text']) > 0:
            self.mist_value.config(fg="red")
        elif int(self.mist_value['text']) == 0:
            self.mist_value.config(fg="white")

    def count_score(self):
        self.time_start = False
        cpm = int(self.points)
        wpm = int((self.points / 5) / ((int(self.timer_text['text'])) / 60))
        net_wpm = (int(((self.points / 5) - (self.mistakes * ((int(self.timer_text['text'])) / 60))) /
                       ((int(self.timer_text['text'])) / 60)))
        accuracy = (net_wpm * 100) / wpm

        messagebox.showinfo("End", f"CPM is {cpm}.\n"
                                   f"WPM is "
                                   f"{wpm},\n"
                                   f"Net WPN is {net_wpm}.\n"
                                   f"Accuracy was {'%.2f' % accuracy}%.")
        self.save_score(self.net_wpm)

    def save_score(self, net_wpm):
        if self.net_wpm > self.high_score:
            self.high_score = self.net_wpm
            with open("data.txt", mode="w") as data:
                data.write(f"{self.high_score}")

    def restart(self):
        try:
            self.window.destroy()
            self.window.after_cancel(self.time)
            Screen()
        except ValueError:
            Screen()

    def create_widgets(self):
        timer_label = Label(text="TIME", fg="white", bg="black", font=("Tahoma", 12))
        timer_label.grid(column=0, row=0, sticky=E)
        self.timer_text = Label(text="0", fg="white", bg="black", font=("Tahoma", 12))
        self.timer_text.grid(column=1, row=0, sticky=W)

        cpm_label = Label(text=f"CPM: ", fg="white", bg="black", font=("Tahoma", 12))
        cpm_label.grid(column=2, row=0, sticky=E)
        self.cpm_value = Label(text="0", fg="white", bg="black", font=("Tahoma", 12))
        self.cpm_value.grid(column=3, row=0, sticky=W)

        wpm_label = Label(text="WPM/NET WPM: ", fg="#fafafa", bg="#000000", font=("Tahoma", 12))
        wpm_label.grid(column=4, row=0, sticky=E)
        self.wpm_value = Label(text="0", fg="#fafafa", bg="#000000", font=("Tahoma", 12))
        self.wpm_value.grid(column=5, row=0, sticky=W)

        mist_label = Label(text="MISTAKES: ", fg="#fafafa", bg="#000000", font=("Tahoma", 12))
        mist_label.grid(column=6, row=0, sticky=E)
        self.mist_value = Label(text="0", fg="#fafafa", bg="#000000", font=("Tahoma", 12))
        self.mist_value.grid(column=7, row=0, sticky=W)

        high_score_label = Label(text=f"HIGH SCORE: {self.high_score} NET WPM.",
                                 fg="#fafafa", bg="#000000", font=("Tahoma", 12, "bold"))
        high_score_label.grid(column=8, row=0)

        entry_label = Label(text="WRITE BELOW:", width=15, bg="#000000", fg="#fafafa", font=("Tahoma", 12, "bold"))
        entry_label.grid(column=1, row=5)
        self.entry = StringVar()
        self.entry.trace_add('write', self.text_callback)
        self.entry_field = Entry(self.window, width=95, textvariable=self.entry, bg="#242424", fg="#fafafa",
                                 font=("Arial", 12, "bold"))
        self.entry_field.grid(column=1, row=6, columnspan=8, pady=15)
        self.entry_field.bind("<BackSpace>", self.backspace)

        restart = Button(text="RESTART", font=("Tahoma", 12, "bold"), bg="#000000", fg="#fafafa",
                         command=self.restart)
        restart.grid(column=8, row=7)
