#!/usr/bin/env python3
import json
import random
from pathlib import Path

class Question(object):
    def __init__(self, jsonQuestion):
        self.question = jsonQuestion['question']
        self.answers = jsonQuestion['answers']
        self.answer = jsonQuestion['answer']
        self.answers.append(jsonQuestion['answer'])
        random.shuffle(self.answers)
        index = 0
        for a in self.answers:
            if a == jsonQuestion['answer']:
                self.answerIndex = index
            index = index + 1

def loadQuestions(filename):
    parent = Path(__file__).parent
    f = open(str(parent / filename))
    questionFile = json.load(f)
    f.close()

    questions = []
    for q in questionFile['questions']:
        questions.append(Question(q))

    return questions

if __name__ == '__main__':
    questions = loadQuestions("questions.json")
    for q in questions:
        print(q.question)
        print("Answer index %d" % q.answerIndex)
        for a in q.answers:
            if a == q.answer:
                print("\t* %s" % a)
            else:
                print("\t%s" % a)
