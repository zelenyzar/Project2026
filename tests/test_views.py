from unittest.mock import patch

from src.views import sorted_operation


@patch("src.views.currency_rate")
@patch("src.views.stock_price")
def test_sorted_operation(mock_price, mock_currency, operation_2, operation_3, operation_1, operation_4):
    mock_price.return_value = operation_3
    mock_currency.return_value = operation_2
    assert sorted_operation("20.12.2021") == operation_1
    assert sorted_operation("20.12.2021", "10.12.2021") == operation_4
    assert sorted_operation("1023.514.120") == "Неверный формат даты"
