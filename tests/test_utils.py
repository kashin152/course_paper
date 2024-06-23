import datetime
import os
from unittest.mock import Mock, patch

import pandas as pd
import pytest
from dotenv import load_dotenv

from src.utils import (filter_by_period, get_greeting, get_response, getting_data_account, getting_data_currencies,
                       getting_data_stock_prices, getting_top_specified_period, information_cards)

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_STOCKS = os.getenv("API_KEY_STOCKS")


@patch("pandas.read_excel")
def test_getting_data_account(mock_read_excel):
    file_name = "test.xlsx"
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    data = {
        "Дата операции": ["08.03.2018 20:35:03", "08.03.2018 20:12:02"],
        "Дата платежа": ["10.03.2018", "10.03.2018"],
        "Номер карты": ["*7197", "*7197"],
        "Статус": ["OK", "OK"],
        "Сумма операции": [-899.00, -1194.00],
        "Валюта операции": ["RUB", "RUB"],
        "Кэшбэк": [3, 0],
        "Категория": ["Одежда и обувь", "Одежда и обувь"],
        "Описание": ["OOO Sedmaya Avenyu", "Kontsept Klub"],
        "Сумма платежа": [0, 0],
        "Валюта платежа": ["RUB", "RUB"],
        "MCC": [0, 0],
        "Бонусы (включая кэшбэк)": [0, 0],
        "Округление на инвесткопилку": [0, 0],
        "Сумма операции с округлением": [0, 0],
    }
    df = pd.DataFrame(data)
    mock_read_excel.return_value = df
    result = getting_data_account(file_path)
    assert len(result) == 2
    assert result[0] == {
        "Date_operation": "08.03.2018 20:35:03",
        "Payment_date": "10.03.2018",
        "Card_numbers": "*7197",
        "Status": "OK",
        "amount": -899.00,
        "currency": "RUB",
        "Payment amount": 0,
        "Payment currency": "RUB",
        "Cashback": 3,
        "Category": "Одежда и обувь",
        "MCC": 0,
        "Description": "OOO Sedmaya Avenyu",
        "Bonuses": 0,
        "Rounding_investment_bank": 0,
        "Amount_rounding_operation": 0,
    }
    assert result[1] == {
        "Date_operation": "08.03.2018 20:12:02",
        "Payment_date": "10.03.2018",
        "Card_numbers": "*7197",
        "Status": "OK",
        "amount": -1194.00,
        "currency": "RUB",
        "Payment amount": 0,
        "Payment currency": "RUB",
        "Cashback": 0,
        "Category": "Одежда и обувь",
        "MCC": 0,
        "Description": "Kontsept Klub",
        "Bonuses": 0,
        "Rounding_investment_bank": 0,
        "Amount_rounding_operation": 0,
    }


@pytest.mark.parametrize(
    "date, expected",
    [
        (datetime.datetime(2021, 12, 31, 11, 0, 0), "Доброе утро"),
        (datetime.datetime(2021, 12, 31, 15, 0, 0), "Добрый день"),
        (datetime.datetime(2021, 12, 31, 20, 0, 0), "Добрый вечер"),
        (datetime.datetime(2021, 12, 31, 23, 0, 0), "Доброй ночи"),
    ],
)
def test_get_greeting(date, expected):
    assert get_greeting(date) == expected


@pytest.mark.parametrize(
    "date, expected",
    [
        ("31-12-2021 10:44:00", "Доброе утро"),
        ("31-12-2021 16:44:00", "Добрый день"),
        ("31-12-2021 19:44:00", "Добрый вечер"),
        ("31-12-2021 23:44:00", "Доброй ночи"),
    ],
)
def test_get_response(date, expected):
    assert get_response(date) == expected


def test_filter_by_period(transactions):
    result = filter_by_period(transactions, "01-10-2021 09:56:08")
    assert result == []

    result = filter_by_period(transactions, "30-09-2020 11:53:24")
    assert result == [
        {
            "Amount_rounding_operation": 120000.0,
            "Bonuses": 0,
            "Card_numbers": "*4556",
            "Cashback": "NaN",
            "Category": "Переводы",
            "Date_operation": "30.09.2020 11:53:24",
            "Description": "Игорь Б.",
            "MCC": "NaN",
            "Payment amount": 120000.0,
            "Payment currency": "RUB",
            "Payment_date": "30.09.2020",
            "Rounding_investment_bank": 0,
            "Status": "OK",
            "amount": 120000.0,
            "currency": "RUB",
        }
    ]


def test_information_cards(transactions):
    result = information_cards(
        [
            {
                "Date_operation": "08.10.2021 20:15:16",
                "Payment_date": "08.10.2021",
                "Card_numbers": "nan",
                "Status": "OK",
                "amount": -399.0,
                "currency": "RUB",
                "Payment amount": -399.0,
                "Payment currency": "RUB",
                "Cashback": 3.0,
                "Category": "Онлайн-кинотеатры",
                "MCC": 7841.0,
                "Description": "Иви",
                "Bonuses": 3,
                "Rounding_investment_bank": 0,
                "Amount_rounding_operation": 399.0,
            },
            {
                "Date_operation": "18.08.2019 17:54:47",
                "Payment_date": "18.08.2019",
                "Card_numbers": "*1112",
                "Status": "FAILED",
                "amount": -3000.0,
                "currency": "RUB",
                "Payment amount": -3000.0,
                "Payment currency": "RUB",
                "Cashback": "nan",
                "Category": "nan",
                "MCC": "nan",
                "Description": "Перевод с карты",
                "Bonuses": 0,
                "Rounding_investment_bank": 0,
                "Amount_rounding_operation": 3000.0,
            },
        ]
    )
    assert result == [
        {"cashback": 3.0, "last_digits": "Неизвестная карта", "total_spent": -399.0},
        {"cashback": 0, "last_digits": "*1112", "total_spent": -3000.0},
    ]

    result = information_cards(transactions)
    assert result == [
        {"cashback": 0, "last_digits": "*4556", "total_spent": 170000.0},
        {"cashback": 0, "last_digits": "*7197", "total_spent": -187.0},
    ]


def test_getting_top_specified_period(transactions_data):
    result = getting_top_specified_period(transactions_data)
    assert result == [
        {"amount": -3000.0, "category": "Переводы", "date": "01.01.2018", "description": "Линзомат ТЦ Юность"},
        {"amount": -316.0, "category": "Красота", "date": "01.01.2018", "description": "OOO Balid"},
        {"amount": 200.0, "category": "Переводы", "date": "27.08.2019", "description": "Пополнение счета"},
        {"amount": -100.0, "category": "Связь", "date": "30.08.2019", "description": "МТС"},
        {"amount": -21.0, "category": "Красота", "date": "03.01.2018", "description": "OOO Balid"},
    ]


@patch("requests.get")
def test_getting_data_currencie(mock_get):
    api = "https://api.example.com"
    currencies = {"user_currencies": ["USD", "EUR", "GBP"]}

    mock_response = Mock()
    mock_response.json.return_value = {"data": {"USD": 1.0, "EUR": 2.0, "GBP": 3.0}}
    mock_get.return_value = mock_response

    result = getting_data_currencies(api, currencies)
    assert isinstance(result, list)
    assert len(result) == 3
    for item in result:
        assert isinstance(item, dict)
        assert "currency" in item
        assert "rate" in item


@patch("requests.get")
def test_getting_data_currencie_error(mock_get):
    api = "https://api.example.com"
    currencies = {"user_currencies": ["USD", "EUR"]}

    import requests

    mock_get.side_effect = requests.exceptions.RequestException

    result = getting_data_currencies(api, currencies)
    assert result == []


def test_getting_data_stock_prices_success():
    api = "https://api.example.com/stock/prices"
    stocks = {"user_stocks": ["AAPL", "GOOG", "MSFT"]}

    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.json.return_value = {"c": 100.0}
        mock_get.return_value = mock_response

        result = getting_data_stock_prices(api, stocks)

        assert len(result) == 3
        assert result[0]["stock"] == "AAPL"
        assert result[0]["price"] == 100.0
        assert result[1]["stock"] == "GOOG"
        assert result[1]["price"] == 100.0
        assert result[2]["stock"] == "MSFT"
        assert result[2]["price"] == 100.0


@patch("requests.get")
def test_getting_data_stock_prices_error(mock_get):
    api = "https://api.example.com"
    currencies = {"user_stocks": ["AAPL", "AMZN", "GOOGL"]}

    import requests

    mock_get.side_effect = requests.exceptions.RequestException

    result = getting_data_stock_prices(api, currencies)
    assert result == []
