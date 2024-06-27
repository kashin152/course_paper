import json
import logging
import os
import re
from typing import List

logger = logging.getLogger("services")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs", "services.log"), mode="w"
)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def list_transactions_sort_search(list_txn: List[dict], search_bar: str) -> str:
    """Функция, которая возвращает список словарей, у которых в любом поле есть строка поиска вводимая пользователем
    и отдает JSON-ответ"""
    new_list_transactions = []
    # logger.info("Перебираем словари в списке")
    for transactions in list_txn:
        # logger.info("Перебираем ключи и значения в словаре")
        for key, value in transactions.items():
            # logger.info("Проверяем является ли значение строкой и находится ли слово для поиска в значениях словаря")
            if isinstance(value, str) and re.search(search_bar, value, flags=re.IGNORECASE):
                # logger.info("Записываем найденную транзакцию в список")
                new_list_transactions.append(transactions)
                break
    # logger.info("Возвращаем JSON-ответ")
    return json.dumps(new_list_transactions, ensure_ascii=False)
