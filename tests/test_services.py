from src.services import search_point


def test_search_point(search_1):
    assert search_point("") == "Вы не задали слово"
    assert search_point("вашем") == search_1
    assert search_point("крокодил") == "[]"
