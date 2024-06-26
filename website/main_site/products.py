from dataclasses import dataclass
from enum import Enum

# Тип продукта
# - Кредит на любые цели
# - Кредит на покупку
# - Кредитка 2 года без %
# - Кредитка 200 дней без %
class ProductType(Enum):
    LOAN_MAIN = 1
    LOAN_TARGET = 2
    CC_2Y = 3
    CC_200D = 4

# Кредит
# (Базовый класс)
@dataclass
class Loan:
    amnt: float            # Сумма
    duration: int          # Срок (в месяцах)
    has_furry_zero: bool   # Хочу 0

    def annuity_payment(self):
        P = self.amnt
        r = self.year_interest / 12
        n = self.duration
        x = (1 + r)**n

        return P*(r*x) / (x-1)

# Кредит на любые цели
@dataclass
class MainLoan(Loan):
    year_interest_1st_period: float 
    first_period_dur: int 
    # ^ определяется индивидуально, от 25% до 59.5%
    # от 6 до 36 месяцев
    year_interest_2nd_period: float
    MIN_AGE: int
    MAX_AGE = 70

    is_client: bool  # Тип клиента

    # Инициализация
    # TODO: рассмотреть как определяется ставка за первый период
    def __init__(self, type: bool, duration: int, 
                 amnt: float, has_furry_zero: bool, interest_1st_period: float,
                 first_period_dur: int):
        self.set_program(type)
        self.is_client = type
        self.amnt = amnt
        self.duration = duration
        self.has_furry_zero = has_furry_zero
        self.year_interest_1st_period = interest_1st_period
        self.first_period_dur = first_period_dur

# Кредит на товар
@dataclass
class TargetLoan(Loan):
    YEAR_INTEREST: float # Устанавливается индивидуально

    # Инициализация
    # TODO: должен возвращаться тип Enum, который определяет, почему не смогли выдать кредит 
    # TODO: рассмотреть как определяется ставка за первый период
    def __init__(self, type: bool, duration: int, 
                 amnt: float, has_furry_zero: bool, interest: float) -> bool:
        self.amnt = amnt
        self.duration = duration
        self.has_furry_zero = has_furry_zero
        self.YEAR_INTEREST = interest

        return True

# Кредитная карта
# (Базовый класс для 2-х типов карт)
# TODO: спросить про условия беспроцентного периода
@dataclass
class CreditCard:
    debt: float            # Сумма задолженности
    high_interest: float   # Повышенная ставка по накопительным счетам
    # TODO: Разобраться с этим ^ подробнее
    limit: float           # Одобренный лимит
    is_0_percent: bool     # Беспроцентный период или нет
    spent_month: float     # Сколько потратили в месяц

    # Коммиссия за снятие наличных
    def commission_cash(self, op_sum: float) -> float:
        return op_sum * 0.059 + 590
    
    # Коммиссия за перевод 
    def commission_transfer(self, op_sum: float) -> float:
        return op_sum * 0.039 + 390
    
    # Минимальные выплаты
    def min_payment(self) -> float:
        result = self.balance * 0.02
        if self.is_0_percent:
            result += 0.01 * self.limit
        if result < 200:
            return 200
        else:
            return result

# Кредитная карта 2 года без %
@dataclass
class CC2Years(CreditCard):
    # Годовые ставки (вне льготного периода):
    INTEREST_BUY = 0.189   # за оплату товаров и услуг
    INTEREST_CASH = 0.289  # при снятии наличных

@dataclass
class CC200Days(CreditCard):
     # Годовые ставки (вне льготного периода):
    INTEREST_BUY = 0.289   # за оплату товаров и услуг
    INTEREST_CASH = 0.289  # при снятии наличных
