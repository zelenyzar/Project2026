import json
import logging
import re

from src.utils import read_file

logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
console_handler = logging.FileHandler("logs/services.log", mode="w", encoding="utf-8")
console_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(lineno)d: %(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)


def search_point(key_word):
    """Поиск транзакций по слову в категории или описании"""
    transaction = read_file()
    logger.info("Файл считан")
    transaction = transaction.fillna("")
    transaction_dict = transaction.to_dict(orient="records")
    result = []
    if key_word == "" or key_word == " ":
        logger.debug("Отсутвует слово")
        return "Вы не задали слово"
    else:
        pattern = re.compile(rf"{key_word}", re.IGNORECASE)
        for transaction in transaction_dict:
            if pattern.search(transaction.get("Категория", "")):
                result.append(transaction)
            elif pattern.search(transaction.get("Описание", "")):
                result.append(transaction)
        if len(result) == 0:
            logger.debug("В перечне отсутствует указанная операция")
            print("Операции не найдены")
    trans_result = json.dumps(result, ensure_ascii=False)
    logger.info("Операции с указанным словом найдены")
    return trans_result
