import logging
import os
from datetime import datetime

import pandas as pd

logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
console_handler = logging.FileHandler("logs/reports.log", mode="w", encoding="utf-8")
console_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(lineno)d: %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


def expenses_category_output(file_name="expenses_category.xlsx"):
    """Декоратор записи результата функции в файл"""

    def decorators(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if not isinstance(result, str):
                result.to_excel(os.path.join(os.path.dirname(__file__), "..", "data", file_name), index=False)
                logger.debug("Результат функции записан в файл")
            return result

        return wrapper

    return decorators


@expenses_category_output()
def expenses_category(transactions, category, some_date=None):
    """Функция получения трат по заданной категории за три месяца"""
    try:
        if some_date is None:
            some_date = datetime.today()
            year = int(some_date.strftime("%Y"))
            month = int(some_date.strftime("%m"))
            day = int(some_date.strftime("%d"))

        else:
            some_date = datetime.strptime(some_date, "%Y.%m.%d")
            year = some_date.year
            month = some_date.month
            day = some_date.day

        for month_count in range(3):
            month = month - 1
            if month == 0:
                month = 12
                year = year - 1

        start_date = datetime(year, month, day)
        logger.info("Определен предел диапазона дат поиска")
    except ValueError:
        logger.debug("Неверный формат даты")
        return "Неверный формат даты"

    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)
    transaction_date = transactions.loc[start_date <= transactions["Дата платежа"]].loc[
        transactions["Дата платежа"] <= some_date
    ]
    expenses = transaction_date[transaction_date["Сумма операции"] < 0]
    trans_category = expenses[expenses["Категория"] == category]
    logger.info("Получены траты по заданной категории за три месяца")
    return trans_category
