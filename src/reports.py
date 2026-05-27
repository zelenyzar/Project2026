import functools
import os
from datetime import datetime

import pandas as pd

from src.utils import read_file


def expenses_category_output(file_name="expenses_category.xlsx"):
    """Декоратор записи результата функции в файл"""

    def decorators(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            result.to_excel(os.path.join(os.path.dirname(__file__), "..", "data", file_name), index=False)
            result = result.to_json(date_format="iso", force_ascii=False)
            return result

        return wrapper

    return decorators


@expenses_category_output()
def expenses_category(transactions, category, some_date=None):
    """Функция получения трат по заданной категории за три месяца"""
    if some_date == None:
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

    transactions["Дата платежа"] = pd.to_datetime(transactions["Дата платежа"], dayfirst=True)
    transaction_date = transactions.loc[start_date <= transactions["Дата платежа"]].loc[
        transactions["Дата платежа"] <= some_date
    ]
    expenses = transaction_date[transaction_date["Сумма операции"] < 0]
    trans_category = expenses[expenses["Категория"] == category]

    return trans_category



