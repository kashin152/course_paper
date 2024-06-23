import logging
import math
import os
from datetime import datetime
from typing import Any, Union

import pandas as pd
import requests

from src.config import API_KEY, API_KEY_STOCKS

logger = logging.getLogger("utils")
file_handler = logging.FileHandler(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "../logs", "utils.log"), mode="w"
)
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


def getting_data_account(data: str) -> list[dict]:
    """Функция, которая считывает данные из файла XLSX и преобразовывает в список словарей"""
    logger.info("Читаем данные из файла XLSX")
    df = pd.read_excel(data)
    result = []
    logger.info("Полученные данные преобразовываем в словари и добавляем в список")
    for index, row in df.iterrows():
        data_dict = {
            "Date_operation": row["Дата операции"],
            "Payment_date": row["Дата платежа"],
            "Card_numbers": row.get("Номер карты"),
            "Status": row["Статус"],
            "amount": row["Сумма операции"],
            "currency": row["Валюта операции"],
            "Payment amount": row["Сумма платежа"],
            "Payment currency": row["Валюта платежа"],
            "Cashback": row["Кэшбэк"],
            "Category": row["Категория"],
            "MCC": row["MCC"],
            "Description": row["Описание"],
            "Bonuses": row["Бонусы (включая кэшбэк)"],
            "Rounding_investment_bank": row["Округление на инвесткопилку"],
            "Amount_rounding_operation": row["Сумма операции с округлением"],
        }
        result.append(data_dict)
    return result


current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, "../data/operations.xls")
data_transaction = getting_data_account(json_file_path)
# print(data_transaction)


def get_greeting(time: datetime) -> str:
    """Возвращает приветствие в зависимости от времени дня"""
    logger.info("Извлекаем часовой компонент из заданного времени и сохраням его в отдельной переменной")
    hour = time.hour

    logger.info("Проверяем в каком промежутке времени находится заданный часа времени для корректного приветствия")
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_response(date_time_str: str) -> str:
    """Главная функция, которая передает указаннаю дату и возвращает привествие"""
    logger.info("Выводим приветствие в зависимости от заданного времени")
    greeting = get_greeting(datetime.strptime(date_time_str, "%d-%m-%Y %H:%M:%S"))
    return greeting


def filter_by_period(data: list[dict], date_string: str) -> list[dict]:
    """Функция, которая фильтрует список словарей за период с начала месяца до указанной даты"""
    logger.info("Переводим заданную дату из типа даных str в формат datetime")
    dt = datetime.strptime(date_string, "%d-%m-%Y %H:%M:%S")

    logger.info("Устанавливаем первое число месяца в полученной дате")
    first_day_of_month = dt.replace(day=1)

    logger.info("Присваиваем переменные началу и концу временного периода")
    start_date = first_day_of_month
    end_date = dt

    logger.info("Выводим отфильтрованные транзакции согласно заданному периоду")
    filtered_data = [
        item for item in data if start_date <= datetime.strptime(item["Date_operation"][:10], "%d.%m.%Y") <= end_date
    ]
    return filtered_data


def information_cards(transactions: list[dict]) -> list[dict[str, int | str | Any]]:
    """Функция, которая выводит общую сумму расходов и кэшбек по каждой карте"""

    cards = {}
    logger.info("Перебираем словари в списке транзакций")
    for transaction in transactions:
        card_number = transaction["Card_numbers"]

        logger.info("Проверяем есть ли номер карты в словаре cards")
        if card_number not in cards:
            logger.info("Добавляем в словарь cards новые ключи total_spent и cashback, если номера карты нет в cards")
            cards[card_number] = {"total_spent": 0, "cashback": 0}

        logger.info("Складываем суммы транзакций и добавляем в ключ total_spent")
        cards[card_number]["total_spent"] += transaction["amount"]

        logger.info("Добавляем в cards ключ Cashback и его значение сумму кэшбека")
        cashback = float(transaction["Cashback"])
        if math.isnan(cashback):
            cashback = 0
        cards[card_number]["cashback"] += cashback

    response = []

    logger.info("Перебираем ключи и из значения в cards")
    for card_number, card_info in cards.items():
        try:
            if math.isnan(float(card_number)):
                last_digits = "Неизвестная карта"
            else:
                last_digits = card_number
        except ValueError:
            last_digits = card_number
        logger.info(
            """Записываем в список новый словарь с установленными ключами,
            где значениями выступают ключи и значения из cards"""
        )
        response.append(
            {
                "last_digits": last_digits,
                "total_spent": round(card_info["total_spent"], 2),
                "cashback": card_info["cashback"],
            }
        )

    logger.info("Выводим результат")
    return response


def getting_top_specified_period(data: list[dict]) -> list[dict]:
    """Фукнция, котораая возвращает топ-5 транзакций по сумме платежа"""
    logger.info("Преобразовываем список словарей в DataFrame")
    pd_data = pd.DataFrame(data)

    logger.info("Проверяем статус операции, которая должна быть успешной")
    pd_data = pd_data.loc[pd_data["Status"] == "OK"]

    logger.info("Сортируем транзакции по убыванию по сумме операции с округлением")
    pd_data = pd_data.sort_values(by="Amount_rounding_operation", ascending=False)

    logger.info("Выводи первые 5 транзакций")
    data = pd_data.head(5)

    logger.info("Преобразовываем в список словарей")
    top_transactions = data.to_dict("records")

    result = []
    logger.info(
        """Записываем в список новый словарь с установленными ключами,
        где значениями выступают значения ключей из отфильтрованного списка словарей"""
    )
    for top_transaction in top_transactions:
        result.append(
            {
                "date": top_transaction["Date_operation"][:10],
                "amount": top_transaction["amount"],
                "category": top_transaction["Category"],
                "description": top_transaction["Description"],
            }
        )

    logger.info("Выводим результат")
    return result


def getting_data_currencies(api: str, currencies: dict) -> list[dict]:
    """Функция, которая получает данные о курсе валют из указанного API для заданной валюты"""
    result = []
    try:
        logger.info("Перебираем валюты из заданного списка словарей валют")
        for currency in currencies["user_currencies"]:

            logger.info("Делаем запрос на сервис API для получения курса валют")
            response = requests.get(api, params={"get": "rates", "pairs": f"{currency}RUB", "key": API_KEY})

            logger.info("Получаем JSON данные")
            response_json = response.json()

            logger.info("Полученные данные преобразовываем в заданный словарь")
            result.append({"currency": currency, "rate": list(response_json["data"].values())[0]})

        logger.info("Выводим результат")
        return result
    except requests.exceptions.RequestException:
        logger.error("Запрос на сервис API не успешный")
        return []


def getting_data_stock_prices(api: str, stocks: dict) -> Union[list[dict] | dict]:
    """Функция, которая получает данные о ценах акции из указанного API для заданной акции"""
    result = []
    try:
        for stock in stocks["user_stocks"]:

            logger.info("Делаем запрос на сервис API для получения цен акций")
            response = requests.get(api, params={"symbol": stock, "token": API_KEY_STOCKS})

            logger.info("Получаем JSON данные")
            response_json = {"stock": stock, "data": response.json()}

            logger.info("Полученные данные преобразовываем в заданный словарь")
            result.append({"stock": response_json["stock"], "price": response_json["data"]["c"]})

        logger.info("Выводим результат")
        return result
    except requests.exceptions.RequestException:
        logger.error("Запрос на сервис API не успешный")
        return []
