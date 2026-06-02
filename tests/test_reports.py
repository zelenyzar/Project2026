from src.reports import expenses_category


def test_expenses_category(df_test_1, expenses, expenses_1):
    assert (
        expenses_category(df_test_1, "Супермаркеты", "2020.03.19").to_json(date_format="iso", force_ascii=False)
        == expenses
    )
    assert expenses_category(df_test_1, "Супермаркеты").to_json(date_format="iso", force_ascii=False) == expenses_1
    assert expenses_category(df_test_1, "").to_json(date_format="iso", force_ascii=False) == expenses_1
    assert expenses_category(df_test_1, "", "125136.25") == "Неверный формат даты"
