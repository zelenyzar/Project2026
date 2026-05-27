from src.reports import expenses_category


def test_expenses_category(df_test_1, expenses, expenses_1):
    assert expenses_category(df_test_1, "Супермаркеты", "2020.03.19") == expenses
    assert expenses_category(df_test_1, "Супермаркеты") == expenses_1
    assert expenses_category(df_test_1, "") == expenses_1
