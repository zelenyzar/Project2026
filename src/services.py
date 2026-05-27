import json
import re

from src.utils import read_file


def search_point(key_word):
    """Поиск транзакций по слову в категории или описании"""
    transaction = read_file()
    transaction = transaction.fillna("")
    transaction_dict = transaction.to_dict(orient="records")
    result = []
    if key_word == "" or key_word == " ":
        return "Вы не задали слово"
    else:
        pattern = re.compile(rf"{key_word}", re.IGNORECASE)
        for transaction in transaction_dict:
            if pattern.search(transaction.get("Категория", "")):
                result.append(transaction)
            elif pattern.search(transaction.get("Описание", "")):
                result.append(transaction)
        if len(result) == 0:
            print("Операции не найдены")
    trans_result = json.dumps(result, ensure_ascii=False)
    return trans_result
