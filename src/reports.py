import logging
import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd

logger = logging.getLogger("reports")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs", "reports.log"), mode="w"
)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def write_to_file_params(file_name: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(os.path.join(file_name), "w") as file:
                file.write(result.to_string() + "\n")
            return result

        return wrapper

    return decorator


def my_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open("function_report.txt", "w") as file:
            file.write(result.to_string() + "\n")
        return result

    return wrapper


@write_to_file_params(file_name="function_report.txt")
@my_decorator
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:

    if date is None:
        logger.info("Установка текущей даты, если не задана дата")
        selected_date = datetime.today().strftime("%Y-%m-%d")
    else:
        logger.info("Преобразование в datetime заданой даты")
        selected_date = pd.to_datetime(date, dayfirst=True)

    logger.info("Преобразование списка транзакций в DataFrame")
    pd_transactions = pd.DataFrame(transactions)

    logger.info("Находим отчетную дату за 3 месяца")
    three_months_ago = selected_date - timedelta(days=90)

    logger.info("Фильтруем транзакции по категории и за период последних 3-х месяцев")
    filtered_transactions = pd_transactions[
        (pd_transactions["Category"] == category)
        & (pd.to_datetime(pd_transactions["Date_operation"], dayfirst=True) >= three_months_ago)
        & (pd.to_datetime(pd_transactions["Date_operation"], dayfirst=True) <= selected_date)
    ]

    logger.info("Формируем группу отфильтрованных транзаций и выводим их сумму")
    spending = filtered_transactions.groupby("Date_operation")["amount"].sum().reset_index()

    logger.info("Выводим результат")
    return spending
