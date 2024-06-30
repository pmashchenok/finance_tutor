from dataclasses import dataclass
from enum import Enum

# Тип продукта
# - Кредит на любые цели
# - Кредит на покупку
class ProductType(Enum):
    LOAN_MAIN = 1
    LOAN_TARGET = 2

# Кредит
# (Базовый класс)
@dataclass
class Loan:
    amnt: int              # Сумма
    duration: int          # Срок (в месяцах)
    has_furry_zero: bool   # Хочу 0

    def annuity_payment(self):
        P = self.amnt
        r = self.year_interest / 12
        n = self.duration
        x = (1 + r)**n

        return int(P*(r*x) / (x-1))
    
    @staticmethod
    def debt_part(debt, interest, payment):
        return payment - (debt * interest/12)

# Кредит на любые цели
@dataclass
class MainLoan(Loan):
    year_interest_1st_period: float 
    first_period_dur: int 
    # ^ определяется индивидуально, от 25% до 59.5%
    # от 6 до 36 месяцев

    is_client: bool  # Тип клиента

    # Инициализация
    def __init__(self, type: bool, duration: int, 
                 amnt: int, has_furry_zero: bool, interest_1st_period: float,
                 first_period_dur: int):
        self.is_client = type
        self.amnt = amnt
        self.duration = duration
        self.has_furry_zero = has_furry_zero
        self.year_interest_1st_period = interest_1st_period
        self.first_period_dur = first_period_dur
        self.year_interest_2nd_period = 0.039

    # TODO Я не понимаю как считаются проценты с меняющейся годовой ставкой
    def set_year_interest(self, cur_month: int):
        self.year_interest = self.year_interest_1st_period
        #if self.first_period_dur >= cur_month:
        #    self.year_interest = self.year_interest_1st_period
        #else:
        #    self.year_interest = self.year_interest_2nd_period

# Кредит на товар
@dataclass
class TargetLoan(Loan):
    year_interest: float # Устанавливается индивидуально

    # Инициализация
    def __init__(self, type: bool, duration: int, 
                 amnt: int, has_furry_zero: bool, interest: float) -> bool:
        self.amnt = amnt
        self.duration = duration
        self.has_furry_zero = has_furry_zero
        self.year_interest = interest