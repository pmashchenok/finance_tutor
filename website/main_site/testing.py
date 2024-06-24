# Логика практически завершена. Осталось сделать фронт.

from typing import Dict
import random
import sqlite3
from dataclasses import dataclass

N_QUESTIONS = 10
DB_NAME = "./db.sqlite3"

# TODO Убрать это
# Создание тестовой таблицы
def make_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Questions (
    idx INTEGER PRIMARY KEY,
    text STRING NOT NULL,
    answer STRING NOT NULL
    )
    """)

    for i in range(1, 11):
        cursor.execute("INSERT INTO Questions (idx, text, answer) VALUES (?, ?, ?)", (i, f"Q{i}", i % 4 + 1))

    connection.commit()
    connection.close()

# Предполагается, что БД имеет 3 поля:
# номер вопроса, текст и ответ в виде числа
def get_questions():
    connection = sqlite3.connect(DB_NAME)
    return connection 

@dataclass
class Question:
    idx: int
    text: str

class TestState:
    QUESTION_COUNT = N_QUESTIONS
    score: int 
    question_list: list[Question]
    answers_list: list[int]
    # db_conn: sqlite connection

    def __init__(self):
        self.db_conn = get_questions()
        self.score = 0
        self.question_list = []
        self.answers_list = []

    # Получаем вопрос из pool'а вопросов, выводим его
    # TODO 
    def get_question_list(self):
        cursor = self.db_conn.cursor()
        question = None
        for _ in range(1, N_QUESTIONS+1):
            if len(self.already_answered) == 0:
                idx = random.randrange(1, N_QUESTIONS+1)
                cursor.execute("SELECT idx, text, answer FROM Questions WHERE idx = ?", (idx,))
                results = cursor.fetchone()
                question = Question(results[0], results[1])
                answer = results[2]
            else:
                while self.question[0] in self.already_answered:
                    idx = random.randrange(1, N_QUESTIONS+1)
                    cursor.execute("SELECT idx, text, answer FROM Questions WHERE idx = ?", (idx,))
                    results = cursor.fetchone()
                    question = Question(results[0], results[1])
                    answer = results[2]
            self.question_list.append(question)
            self.answers_list.append(answer)


    def check_answers(self, user_answers):
        for (a, b) in zip(self.answers_list, user_answers):
            if a == b:
                self.score += 1