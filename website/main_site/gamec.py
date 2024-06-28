from dataclasses import dataclass
from enum import Enum
import random
from . import products
import sqlite3

MONTHLY_BILLS = 5000

class PlayState(Enum):
    PLAYING = 0
    WIN = 1
    LOSS = 2

class EventType(Enum):
    CHOICE = 1
    INPUT = 2

@dataclass 
class Event:
    type: EventType
    text: str
    character: str

    def __dict__(self):
        return {
            "type": "input" if self.type is EventType.INPUT else "choice",
            "text": self.text,
            "character": self.character,
        }

@dataclass
class Character:
    name: str
    age: int
    citizenship: str
    income: int
    work_exp: int
    balance: int
    client: bool

    def __dict__(self):
        return {
            "name": self.name,
            "age": self.age,
            "citizenship": self.citizenship,
            "income": self.income,
            "work_exp": self.work_exp,
            "balance": self.balance,
            "client": self.client
        }

class GameState:
    char: Character
    product: products.CC200Days | products.CC2Years | products.MainLoan | products.TargetLoan
    product_type: products.ProductType
    debt: float
    turn: int 
    play_state: PlayState
    event: Event
    event_correctly_solved: bool


    def __init__(self, char: Character, prod, product_type: products.ProductType):
        self.char = char        
        self.product = prod
        self.product_type = product_type
        self.debt = 0
        self.turn = 0
        self.play_state = PlayState.PLAYING
        self.event = None 
        self.event_correctly_solved = False

    def __dict__(self):
       return {
            "char": self.char.__dict__(),
            "product": self.product.__dict__,
            "product_type": self.product_type.__dict__["_name_"],
            "debt": self.debt,
            "turn": self.turn,
            "play_state": self.play_state.__dict__["_name_"],
            "event": self.event.__dict__(),
            "event_correctly_solved": self.event_correctly_solved,
        } 