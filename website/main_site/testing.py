# Логика практически завершена. Осталось сделать фронт.

from typing import Dict
import random
import sqlite3
from dataclasses import dataclass

N_QUESTIONS = 10
DB_NAME = "./db.sqlite3"

def get_questions():
    connection = sqlite3.connect(DB_NAME)
    return connection 

@dataclass
class Question:
    idx: int
    text: str
    labels: list[str]

class TestState:
    score: int 
    question_list: list[Question]
    answers_list: list[int]
    order: list[int]
    # db_conn: sqlite connection

    def __init__(self):
        self.db_conn = get_questions()
        self.score = 0
        self.question_list = []
        self.answers_list = []
        self.order = []

    def get_question_list(self):
        cursor = self.db_conn.cursor()
        question = None
        for _ in range(1, N_QUESTIONS+1):
            if len(self.order) == 0:
                idx = random.randrange(1, N_QUESTIONS+1)
                cursor.execute("SELECT idx, text, label1, label2, label3, label4, answer FROM Test WHERE idx = ?", (idx,))
                results = cursor.fetchone()
                question = Question(results[0], results[1], results[2:-1])
                answer = results[-1]
            else:
                while question.idx in self.order:
                    idx = random.randrange(1, N_QUESTIONS+1)
                    cursor.execute("SELECT idx, text, label1, label2, label3, label4, answer FROM Test WHERE idx = ?", (idx,))
                    results = cursor.fetchone()
                    question = Question(results[0], results[1], results[2:-1])
                    answer = results[-1]
            self.order.append(question.idx)
            self.question_list.append(question)
            self.answers_list.append(answer)


    def check_answers(self, user_answers):
        for (a, b) in zip(self.answers_list, user_answers):
            if a == b:
                self.score += 1

    def rating(self):
        return self.score / 5 - 1