#!/usr/bin/python

import tkinter as tk
import tkinter.font as tkFont

class Answer:
    def __init__(self, text, correct=False):
        self.text = text
        self.correct = correct
    def is_correct(self):
        return self.correct

class Item:
    def __init__(self, question):
        self.question = question
        self.options = [Answer("Answer A"), Answer("Answer B", correct=True), Answer("Answer C")]
        self.asked = False
        self.answered_correctly = False

class Category:
    def __init__(self, name, items):
        self.name = name
        self.items = items

class Kviz(tk.Frame):
    def __init__(self, parent, categories):
        super().__init__(parent)
        self.frames = {
            'home': HomeFrame(self, categories),
            'question': QuestionFrame(self),
        }
        VolumeControls(self, self.font_resize).pack(fill=tk.X)
        self.current_frame = 'home'
        self.frames['home'].pack(expand=True, fill=tk.BOTH)
        self.bind('<Configure>', self.font_resize)

    def switch_frames(self, frame):
        self.frames[self.current_frame].pack_forget()
        self.frames[frame].pack(expand=True, fill=tk.BOTH)
        self.current_frame = frame

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
                tk.Button(self, text=item.question, command=lambda: parent.switch_frames('question')).grid(column=category_number, row=item_number+1, sticky="news")
        self.columnconfigure(tuple(range(self.grid_size()[0])), weight=1)
        self.rowconfigure(tuple(range(1, self.grid_size()[1])), weight=1)
        

class QuestionFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Button(self, text="+", command=lambda: parent.switch_frames('home')).pack()

class VolumeControls(tk.Frame):
    def __init__(self, parent, method):
        super().__init__(parent)
        self.configure(background=COLOR, pady="2") 
        self.method = method
        tk.Button(self, height=-1, font=tkFont.nametofont('TkTextFont'), text="+", command=lambda: method("+")).pack(side=tk.RIGHT)
        tk.Button(self, height=-1, font=tkFont.nametofont('TkTextFont'), text="-", command=lambda: method("-")).pack(side=tk.RIGHT)

COLOR = "#5555dd"

category1 = Category("Category 1", [Item("Question A"), Item("Question B")])
category2 = Category("Category 2", [Item("Question C"), Item("Question D")])

categories = [category1, category2]

root = tk.Tk()
root.title("Kvíz")
root.minsize(400, 200)

default_font = tkFont.nametofont("TkDefaultFont")

kviz = Kviz(root, categories)
kviz.pack(expand=True, fill=tk.BOTH)

root.mainloop()
