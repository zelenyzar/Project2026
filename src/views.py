import json
import os
from datetime import datetime

import pandas as pd

from src.utils import (currency_rate, expenses_categories, expenses_operations, income_categories, income_operations,
                       read_file, stock_price)


def sorted_operation(end_date, start_date=None):
    """Функция, которая сортирует операции в указанном диапазоне дат"""
    calendar = datetime.strptime(end_date, "%d.%m.%Y")
    if start_date is None:
        start_date = datetime(calendar.year, calendar.month, 1)
    else:
        start_date = datetime.strptime(end_date, "%d.%m.%Y")

    operations = read_file()
    operations["Дата платежа"] = pd.to_datetime(operations["Дата платежа"], dayfirst=True)
    operation_date_range = operations.loc[start_date <= operations["Дата платежа"]].loc[
        operations["Дата платежа"] <= calendar
    ]

    path = os.path.join(os.path.dirname(__file__), "..", "data", "user_settings.json")
    with open(path, "r", encoding="utf-8") as f:
        json_file = json.load(f)
        currency_given = ",".join(json_file["user_currencies"])
        stock_list = json_file["user_stocks"]

    categories_name = list(expenses_categories(operation_date_range)["Основные"])
    income_name = list(income_categories(operation_date_range))

    operation_sort = {
        "expenses": {
            "total_amount": expenses_operations(operation_date_range),
            "main": [
                {
                    "category": categories_name[z],
                    "amount": expenses_categories(operation_date_range)["Основные"].get(categories_name[z]),
                }
                for z in range(len(categories_name))
            ],
            "transfer_and_cash": [
                {"category": "Наличные", "amount": expenses_categories(operation_date_range).get("Наличные")},
                {"category": "Переводы", "amount": expenses_categories(operation_date_range).get("Переводы")},
            ],
        },
        "income": {
            "total_amount": income_operations(operation_date_range),
            "main": [
                {
                    "category": income_name[z],
                    "amount": income_categories(operation_date_range).get(income_name[z]),
                }
                for z in range(len(income_name))
            ],
        },
        "currency_rates": currency_rate(currency_given),
        "stock_prices": stock_price(stock_list),
    }

    return operation_sort
