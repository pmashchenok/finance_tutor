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
    inputs: dict[str, str]

    def __dict__(self):
        return {
            "type": self.type.__dict__["_name_"],
            "text": self.text,
            "character": self.character,
            "inputs": self.inputs,
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

    @staticmethod
    def start(character, request):
        product_name = request.POST["product_name"]
        product = None
        product_type = None
        match product_name: 
            case "mainloan":
                product_type = products.ProductType.LOAN_MAIN
                is_client = character.client
                duration = request.POST["duration"]
                amnt = request.POST["amnt"]
                has_furry_zero = request.POST["hfz"] == "y"
                # TODO не знаю как это определяется я просто взял
                # мин. значения с сайта
                interest_1st_period = 0.25
                duration_1st_period = 6
                product = products.MainLoan(is_client, duration, amnt, has_furry_zero,
                                            interest_1st_period, duration_1st_period)
            case "targetloan":
                product_type = products.ProductType.LOAN_TARGET
                is_client = character.client
                duration = request.POST["duration"]
                amnt = request.POST["amnt"]
                has_furry_zero = request.POST["hfz"] == "y"
                # TODO 
                year_interest = 0.25
                product = products.TargetLoan(is_client, duration, amnt, has_furry_zero, year_interest)
            case "cc2y":
                product_type = products.ProductType.CC_2Y
                # TODO Как определяется предел?
                product = products.CC2Years(0, 100000, True, 0)
            case "cc200d":
                # TODO
                product_type = products.ProductType.CC_200D
                product = products.CC200Days(0, 100000, True, 0)
        state = GameState(character, product, product_type)
        first_event = Event(EventType.CHOICE, "Поздравляю с получением продукта! Не забывайте совершать ежемесячные выплаты. Справка всегда доступна. И тд",
                            "Ассистент", {"OK": "ok"})
        state.event = first_event
        return state
    
    def progress(self, game_input):
        print(game_input)
        self.event = Event(EventType.INPUT, "Новое событие", "Ассистент", {"OK": "ok"})