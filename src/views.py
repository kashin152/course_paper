import json
import logging
import os

from src.config import data_json, url, url_stocks
from src.utils import (data_transaction, filter_by_period, get_response, getting_data_currencies,
                       getting_data_stock_prices, getting_top_specified_period, information_cards)

logger = logging.getLogger("views")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs", "views.log"), mode="w"
)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def main(date):
    logger.info("Присваиваем переменным полученные результаты из функций")
    greeting = get_response(date)
    transactions = information_cards(filter_by_period(data_transaction, date))
    top_transactions = getting_top_specified_period(filter_by_period(data_transaction, date))
    course = getting_data_currencies(url, data_json)
    stock_prices = getting_data_stock_prices(url_stocks, data_json)

    logger.info("Полученные данные преобразовываем в заданный словарь")
    response = {
        "greeting": greeting,
        "cards": transactions,
        "top_transactions": top_transactions,
        "currency_rates": course,
        "stock_prices": stock_prices,
    }

    logger.info("Выводим результат")
    return json.dumps(response, ensure_ascii=False)
