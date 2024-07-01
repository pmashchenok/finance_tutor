from dataclasses import dataclass
from enum import Enum
import random
from . import products
import sqlite3

class PlayState(Enum):
    PLAYING = 0
    WIN = 1
    LOSS = 2

class EventType(Enum):
    CHOICE = 1
    INPUT = 2
    CREDIT = 3
    END = 4

class MonthStatus(Enum):
    BEGIN = 1
    MIDDLE = 2
    END1 = 3
    END2 = 4

def cut_off_add(a, b):
    return a + b if a + b > 0 else 0

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
    rating: float

    def __dict__(self):
        return {
            "name": self.name,
            "age": self.age,
            "citizenship": self.citizenship,
            "income": self.income,
            "work_exp": self.work_exp,
            "balance": self.balance,
            "client": self.client,
            "rating": self.rating
        }

class GameState:
    char: Character
    product: products.MainLoan | products.TargetLoan
    product_type: products.ProductType
    debt: int
    month_rem: int
    turn: int 
    event: Event
    event_counter: int
    month_status: MonthStatus


    def __init__(self, char: Character, prod, product_type: products.ProductType):
        self.char = char        
        self.product = prod
        self.product_type = product_type
        self.debt = 0
        self.turn = 0
        self.event = None 
        self.event_counter = 0
        self.month_status = MonthStatus.BEGIN

    def __dict__(self):
       return {
            "char": self.char.__dict__(),
            "product": self.product.__dict__,
            "product_type": self.product_type.__dict__["_name_"],
            "debt": self.debt,
            "turn": self.turn,
            "event": self.event.__dict__(),
            "event_counter": self.event_counter,
            "month_status": self.month_status.__dict__["_name_"],
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
                duration = int(request.POST["duration"])
                amnt = int(request.POST["amnt"])
                has_furry_zero = request.POST["hfz"] == "y"
                # TODO не знаю как это определяется я просто взял
                # мин. значения с сайта
                interest_1st_period = 0.25
                duration_1st_period = 6
                product = products.MainLoan(is_client, duration, amnt, has_furry_zero,
                                            interest_1st_period, duration_1st_period)
                debt = amnt
                product.set_year_interest(0)
            case "targetloan":
                product_type = products.ProductType.LOAN_TARGET
                is_client = character.client
                duration = int(request.POST["duration"])
                amnt = int(request.POST["amnt"])
                has_furry_zero = request.POST["hfz"] == "y"
                # TODO 
                year_interest = 0.25
                product = products.TargetLoan(is_client, duration, amnt, has_furry_zero, year_interest)
                debt = amnt
        state = GameState(character, product, product_type)
        first_ev_text = """
            Поздравляем с успешным получением кредита! Не забывайте про ежемесячные выплаты по кредиту,
            а также по коммунальным услугам и другим потребностям (будут в конце месяца). <br><br>
            Каждый месяц происходит от 3-х до 5-и случайных событий двух типов: <br>
            1. Выбор из 3-х вариантов <br>
            2. "Форс-мажор" (выбор отсутствует) <br>
            Выбирайте так, чтобы в случае форс-мажора у Вас остались деньги на коммунальные услуги и выплату по кредиту. <br><br>
            Удачи!
        """
        first_event = Event(EventType.CHOICE, first_ev_text, "Ассистент", {"OK": "0"})
        state.event = first_event
        state.debt = debt
        state.turn = 0
        return state
    
    def get_event(self):
        conn = sqlite3.connect("db.sqlite3")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Events ORDER BY RANDOM() LIMIT 1")
        results = cursor.fetchone()
        if results[0] == "CHOICE":
            ev_inputs = {results[3]: int(results[4])}
        else:
            ev_inputs = {results[3]: int(results[4]), 
                      results[5]: int(results[6]),
                      results[7]: int(results[8])}
        ev_type_str = results[0]
        ev_text = results[1]
        ev_char = results[2]
        match ev_type_str:
            case "INPUT":
                ev_type = EventType.INPUT
            case "CHOICE":
                ev_type = EventType.CHOICE
        return Event(ev_type, ev_text, ev_char, ev_inputs)
    
    def get_paid_event(self):
        ev_type = EventType.CHOICE
        ev_text = f"Зарплата! Вам начислено {self.char.income}₽."
        ev_char = "Ассистент"
        ev_inputs = {"OK": self.char.income}
        return Event(ev_type, ev_text, ev_char, ev_inputs)
    
    def pay_bills_event(self):
        ev_type = EventType.CHOICE
        bills = int(self.char.income / 5 + 5000)
        ev_text = f"Вам необходимо оплатить {bills}₽ за коммунальные услуги и на необходимые потребности."
        ev_char = "Ассистент"
        ev_inputs = {"OK": -bills}
        return Event(ev_type, ev_text, ev_char, ev_inputs)

    def pay_credit_event(self):
        ev_type = EventType.CREDIT
        ev_text = f"Вам также необходимо совершить месячную выплату по кредиту (см. справку)."
        ev_char = "Ассистент"
        ev_inputs = {"Введите число": 0}
        return Event(ev_type, ev_text, ev_char, ev_inputs)
    
    def win_event(self):
        self.char.rating = self.rating()
        ev_type = EventType.END
        ev_text = f"Поздравляем, Вы вовремя выплатили кредит! Ваш рейтинг: {self.char.rating}"
        ev_char = "Ассистент"
        ev_inputs = {"Вернуться на главную": 0}
        return Event(ev_type, ev_text, ev_char, ev_inputs)

    def lose_event(self):
        self.char.rating = self.rating()
        ev_type = EventType.END
        if self.char.balance <= 0:
            ev_text = "К сожалению, Вы обанкротились!"
        elif self.turn > self.product.duration and self.debt > 0:
            ev_text = "К сожалению, Вы не успели выплатить кредит!"
        ev_text += f"Ваш рейтинг: {self.char.rating}"
        ev_char = "Ассистент"
        ev_inputs = {"Вернуться на главную": 0}

        return Event(ev_type, ev_text, ev_char, ev_inputs)

    def play_state(self):
        if self.char.balance <= 0:
            return PlayState.LOSS
        if self.debt <= 0:
            return PlayState.WIN
        if self.month_status is MonthStatus.BEGIN and self.turn > self.product.duration:
            if self.debt > 0:
                return PlayState.LOSS
            else:
                return PlayState.WIN
        return PlayState.PLAYING

    def progress(self, game_input):
        if self.product_type is products.ProductType.LOAN_MAIN:
            self.product.set_year_interest(self.turn)
        
        if self.event.type is EventType.CREDIT:
            self.char.balance = cut_off_add(self.char.balance, -game_input)
            debt_part = products.Loan.debt_part(self.debt, self.product.year_interest, game_input) 
            self.debt = int(cut_off_add(self.debt, -debt_part))
        else:
            self.char.balance = cut_off_add(self.char.balance, game_input)

        if self.play_state() is PlayState.WIN:
            self.event = self.win_event()
            return
        elif self.play_state() is PlayState.LOSS:
            self.event = self.lose_event()
            return

        match self.month_status:
            case MonthStatus.BEGIN:
                self.turn += 1
                self.event_counter = random.randint(3, 5)
                print("ev_counter", self.event_counter)
                self.event = self.get_paid_event()
                self.month_status = MonthStatus.MIDDLE
            case MonthStatus.MIDDLE:
                self.event_counter -= 1
                self.event = self.get_event()
                if self.event_counter == 0:
                    self.month_status = MonthStatus.END1
            case MonthStatus.END1:
                self.event = self.pay_bills_event()
                self.month_status = MonthStatus.END2
            case MonthStatus.END2:
                self.event = self.pay_credit_event()
                self.month_status = MonthStatus.BEGIN
        return 
    
    def rating(self) -> float:
        total_dur = self.turn
        prod_dur = self.product.duration
        rem_amnt = self.debt
        total_amnt = self.product.amnt
        rate = 0
        if total_dur <= 12:
            rate += 0.05
            if total_amnt <= 100_000:
                rate += 0.15
            elif total_amnt <= 500_000:
                rate += 0.25
            elif total_amnt <= 1_500_000:
                rate += 0.45
            else:
                rate += 0.65
        elif total_dur <= 48:
            rate += 0.1
            if total_amnt <= 100_000:
                rate += 0.2
            elif total_amnt <= 500_000:
                rate += 0.3
            elif total_amnt <= 1_500_000:
                rate += 0.6
            else:
                rate += 0.8
        else:
            rate += 0.2
            if total_amnt <= 100_000:
                rate += 0.2
            elif total_amnt <= 500_000:
                rate += 0.4
            elif total_amnt <= 1_500_000:
                rate += 0.6
            else:
                rate += 0.8
        if total_dur == prod_dur and rem_amnt == 0:
            return rate
        else:
            return -rate