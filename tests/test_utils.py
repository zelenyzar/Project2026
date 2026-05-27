from unittest.mock import patch

from src.utils import (currency_rate, expenses_categories, expenses_operations, income_categories, income_operations,
                       read_file, stock_price)


@patch("requests.get")
def test_currency_rate(mock_response, test_api_currency, test_api_currency_1):
    """Тест апи по валютам"""
    mock_response.return_value.json.return_value = test_api_currency
    assert currency_rate("Eur") == test_api_currency_1


@patch("finnhub.Client")
def test_stock_price(mock_client, test_stock):
    """Тест апи по акциям"""
    mock_client.return_value.quote.return_value = {"c": 308.65}
    assert stock_price(["AAPL"]) == test_stock


def test_read_file(test_file):
    """Тест чтения файла"""
    assert read_file().head(3).fillna(0).to_dict() == test_file


def test_expenses_operations(df_test_1):
    """Тест подсчетов общей суммы расходов"""
    assert expenses_operations(df_test_1) == 15932


def test_expenses_categories(df_test_1, result_category):
    """Тест группировки категорий"""
    assert expenses_categories(df_test_1) == result_category


def test_income_operations(df_test_1):
    """Тест подсчета суммы поступлений"""
    assert income_operations(df_test_1) == 889


def test_income_categories(df_test_1):
    """Тест сортировки поступлений"""
    assert income_categories(df_test_1) == {"Бонусы": 889}
