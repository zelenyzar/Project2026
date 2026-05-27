import os

import finnhub
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")


def currency_rate(currency_given):
    """Функция определения курса валют"""
    amount_given = "RUB"
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={currency_given}&base={amount_given}"
    payload = {}
    headers = {"apikey": os.getenv("API_KEY")}
    response = requests.get(url, headers=headers, data=payload)
    currency_result = []
    for k, value in response.json().get("rates").items():
        currency_result.append({"currency": k, "rate": round(1 / value, 2)})
    return currency_result


def stock_price(stock_list):
    finnhub_client = finnhub.Client(api_key=os.getenv("API_KEY_2"))
    stocky = []
    for stock in stock_list:
        quote = finnhub_client.quote(stock)
        stocky.append({"stock": stock, "price": quote["c"]})
    return stocky


def read_file():
    """Функция чтения xlsx-файла с транзакциями"""
    path = os.path.join(os.path.dirname(__file__), "..", "data", "operations.xlsx")
    data_file = pd.read_excel(path)
    return data_file.sort_values(by="Сумма операции", ascending=False)


def expenses_operations(transaction) -> int:
    """Функция, определяющая общую сумму расходов"""
    transaction_expenses = transaction[transaction["Сумма операции"] < 0]
    sum_expenses = transaction_expenses["Сумма операции"].sum() * -1
    return int(sum_expenses)


def expenses_categories(transaction):
    """Функция группировки по категориям"""
    transaction_expenses = transaction[transaction["Сумма операции"] < 0]
    transaction_group = round(transaction_expenses.groupby("Категория")["Сумма операции"].sum().abs(), 2)
    head_expenses = transaction_group.head(7)
    other_expenses = round(transaction_group.iloc[7:].sum(), 2)
    cash = round(transaction_expenses[transaction_expenses["Категория"] == "Наличные"]["Сумма операции"].sum(), 2) * -1
    wire_transfers = (
        round(transaction_expenses[transaction_expenses["Категория"] == "Переводы"]["Сумма операции"].sum(), 2) * -1
    )
    expenses_result = {
        "Основные": head_expenses.to_dict(),
        "Остальное": int(other_expenses),
        "Наличные": int(cash),
        "Переводы": int(wire_transfers),
    }
    return expenses_result


def income_operations(transaction) -> int:
    """Функция, определяющая общую сумму поступлений"""
    transaction_income = transaction[transaction["Сумма операции"] > 0]
    sum_income = transaction_income["Сумма операции"].sum()
    return int(sum_income)


def income_categories(transaction):
    """Функция сортировки поступлений по категориям (отсортированы по убыванию)"""
    transaction_income = transaction[transaction["Сумма операции"] > 0]
    transaction_group = transaction_income.groupby("Категория")["Сумма операции"].sum().sort_values(ascending=False)
    return transaction_group.to_dict()
