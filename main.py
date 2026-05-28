import json

from src.reports import expenses_category
from src.services import search_point
from src.utils import read_file
from src.views import sorted_operation


def main():
    while True:
        quest_1 = input(
            "Доброго времени суток, дорогой клиент! Вы зашли в программу сортировки банковских операций.\n"
            "Доступный функционал:\n"
            "1. Найти популярные расходы и категории доходов\n"
            "2. Найти операции по ключевому слову\n"
            "3. Найти расходы по выбранной категории за три месяца\n"
            "Укажите номер запроса: 1, 2 или 3 \n"
        ).lower()
        if quest_1 == "1":
            quest_1_1 = input(
                "Введите дату окончания нужного периода осуществления банковских операций. В формате: ДД.ММ.ГГГГ \n"
            )
            quest_1_2 = input(
                "Хотите указать начало периода? Да/Нет\n"
                "* Если начало периода не указано, автоматически будет выбрано начало месяца.\n"
            ).lower()
            if quest_1_2 == "да":
                quest_1_3 = input(
                    "Введите дату начала нужного периода осуществления банковских операций. В формате: ДД.ММ.ГГГГ \n"
                )
                operation = sorted_operation(quest_1_1, quest_1_3)
            elif quest_1_2 == "нет":
                operation = sorted_operation(quest_1_1)
            else:
                print("Данный ответ не может быть принят. Дата начала поиска будет установлена по умолчанию.")
                operation = sorted_operation(quest_1_1)
            operation = json.dumps(operation, ensure_ascii=False)
            print(operation)
            break
        elif quest_1 == "2":
            quest_2 = input("Введите ключевое слово для поиска операции: \n").lower()
            operation = search_point(quest_2)
            print(operation)
            break
        elif quest_1 == "3":
            quest_3 = input("Введите категорию запроса: \n").capitalize()
            quest_3_1 = input("Хотите указать предельный диапазон даты поиска? Да/Нет \n").lower()
            transaction = read_file()
            if quest_3_1 == "да":
                quest_3_2 = input("Введите дату в формате: ГГГГ.ММ.ДД \n")
                operation = expenses_category(transaction, quest_3, quest_3_2)
            elif quest_3_1 == "нет":
                operation = expenses_category(transaction, quest_3)
            else:
                print("Данный ответ не может быть принят. Дата начала поиска будет установлена по умолчанию.")
                operation = expenses_category(transaction, quest_3)
            if not isinstance(operation, str):
                operation = operation.to_json(orient="records", force_ascii=False, date_format="iso")
            print(operation)
            break


if __name__ == "__main__":
    main()
