#!/usr/bin/env python

class Answer:
    def __init__(self, text, correct=False):
        self.text = text
        self.correct = correct
    def is_correct(self):
        return self.correct

class Item:
    def __init__(self, question, options):
        self.question = question
        self.options = []
        for option in options:
            if option[0] == '*':
                self.options.append(Answer(option[1:], correct=True))
            else:
                self.options.append(Answer(option))
        if len(options) == 0:
            self.options.append(Answer("+", correct=True))
            self.options.append(Answer("-"))

class Category:
    def __init__(self, lines):
        self.name = lines[0][3:]
        self.items = []
        parts = []
        part_lines = []
        data = lines[1:]
        for line_number, line in enumerate(data):
            if len(line) > 0:
                part_lines.append(line)
            if len(line.strip()) == 0 or line_number == len(data) - 1:
                if len(part_lines) > 0:
                    parts.append(part_lines)
                    part_lines = []

        for item in parts:
            self.items.append(Item(item[0], item[1:]))


class Data:
    def __init__(self, questions, config):
        self.categories = []
        parts = []
        part_lines = []
        lines = questions.splitlines()
        for line_number, line in enumerate(lines):
            if len(line.strip()) > 3 and line[0:3] == "===": # new category
                if len(part_lines) > 0:
                    parts.append(part_lines)
                part_lines = []
                part_lines.append(line)
            elif line_number == len(lines)-1: # last line
                part_lines.append(line)
                parts.append(part_lines)
            else:
                part_lines.append(line)

        for category in parts:
            self.categories.append(Category(category))

        self.teams = []
        for line in config.splitlines():
            self.teams.append(line.strip())

fileQ = open("questions.cfg", "r")
contentQ = fileQ.read().strip()

try:
    fileT = open("teams.cfg", "r")
    contentT = fileT.read().strip()
except: contentT = ""

DATA = Data(contentQ, contentT)
