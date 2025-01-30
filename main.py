#!/usr/bin/env python

import tkinter as tk
import tkinter.font as tkFont
from data import *

class Kviz(tk.Frame):
    def __init__(self, parent, categories, teams):
        super().__init__(parent)
        self.frames = {
            'home': HomeFrame(self, categories),
            'question': QuestionFrame(self),
        }
        header = tk.Frame(self)
        header.pack(fill=tk.X)
        header.configure(background=COLOR, pady="2", padx="2") 
        VolumeControls(header, self.font_resize).pack(fill=tk.X, side="right")
        self.current_frame = 'home'
        self.frames['home'].pack(expand=True, fill=tk.BOTH)
        self.bind('<Configure>', self.font_resize)

        self.teams = list(map(lambda teamname: {'name': teamname, 'points': 0}, teams))
        self.current_team = 0
        for team in self.teams:
            teamLabel = tk.Label(header, font=tkFont.nametofont('TkTextFont'), text=f"{team['name']} | {team['points']}")
            teamLabel.pack(fill=tk.X, side="left", padx="4")
            team['label'] = teamLabel

    def switch_frames(self, frame):
        self.frames[self.current_frame].pack_forget()
        self.frames[frame].pack(expand=True, fill=tk.BOTH)
        self.current_frame = frame

    def next_team(self):
        self.current_team = (self.current_team+1) % len(self.teams)

    def correct(self):
        team = self.teams[self.current_team]
        team['points'] = team['points'] + 1
        team['label'].configure(text=f"{team['name']} | {team['points']}")
        self.next_team()
        self.switch_frames('home')

    def wrong(self):
        self.next_team()
        self.switch_frames('home')

    def ask_question(self, item):
        self.frames['question'].ask(item)
        self.switch_frames('question')

    def font_resize(self, event):
        if type(event) == str:
            if event == "+":
                new_size = default_font.cget("size") + 1
            elif event == "-":
                new_size = default_font.cget("size") -1
            default_font.configure(size=new_size)
        else:
            default_font.configure(size=int(self.winfo_width()//30))

class HomeFrame(tk.Frame):
    def __init__(self, parent, categories):
        super().__init__(parent)
        for category_number, category in enumerate(categories):
            tk.Label(self, text=category.name).grid(column=category_number, row=0, sticky="news")
            for item_number, item in enumerate(category.items):
                button = tk.Button(self, text=item.question)
                button.grid(column=category_number, row=item_number+1, sticky="news")
                button.configure(command = lambda button_fixed=button, item_fixed=item: self.question_clicked(button_fixed, item_fixed))
        self.columnconfigure(tuple(range(self.grid_size()[0])), weight=1)
        self.rowconfigure(tuple(range(1, self.grid_size()[1])), weight=1)
        
    def question_clicked(self, button, item):
        button.grid_forget()
        button.master.master.ask_question(item)

class QuestionFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Button(self, text="<-", command=lambda: parent.switch_frames('home')).pack()

    def ask(self, item):
        for widget in self.winfo_children():
            widget.destroy()
        tk.Label(self, text=item.question).pack()
        answerFrame = tk.Frame(self).pack()
        for option in item.options:
            tk.Button(self, text=option.text, command=self.master.correct if option.correct else self.master.wrong).pack()


class VolumeControls(tk.Frame):
    def __init__(self, parent, method):
        super().__init__(parent)
        self.method = method
        tk.Button(self, height=-1, font=tkFont.nametofont('TkTextFont'), text="+", command=lambda: method("+")).pack(side=tk.RIGHT)
        tk.Button(self, height=-1, font=tkFont.nametofont('TkTextFont'), text="-", command=lambda: method("-")).pack(side=tk.RIGHT)

COLOR = "#5555dd"

if __name__ == "__main__":

    data = DATA

    root = tk.Tk()
    root.title("Kvíz")
    root.minsize(400, 200)

    default_font = tkFont.nametofont("TkDefaultFont")

    kviz = Kviz(root, data.categories, data.teams)
    kviz.pack(expand=True, fill=tk.BOTH)

    root.mainloop()
