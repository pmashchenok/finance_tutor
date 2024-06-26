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

@dataclass
class Character:
    name: str
    age: int
    citizenship: str
    income: int
    work_exp: int
    balance: int
    client: bool

class GameState:
    char: Character
    product: products.CC200Days | products.CC2Years | products.MainLoan | products.TargetLoan
    product_type: products.ProductType
    debt: float
    turn: int 
    play_state: PlayState
    event: Event
    event_correctly_solved: bool


    def __init__(self):
        self.char = None        
        self.product = None
        self.product_type = None
        self.debt = 0
        self.turn = 0
        self.play_state = PlayState.PLAYING
        self.event = None 
        self.event_correctly_solved = False 