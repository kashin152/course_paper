import os
from datetime import datetime, timedelta

import pandas as pd

from src.reports import my_decorator, spending_by_category, write_to_file_params


def test_log_file_params(transactions_data):
    @write_to_file_params("function_report.txt")
    def spending_category(transactions, category, date):

        if date is None:
            selected_date = datetime.today().strftime("%Y-%m-%d")
        else:
            selected_date = pd.to_datetime(date, dayfirst=True)
        pd_transactions = pd.DataFrame(transactions)
        three_months_ago = selected_date - timedelta(days=90)
        filtered_transactions = pd_transactions[
            (pd_transactions["Category"] == category)
            & (pd.to_datetime(pd_transactions["Date_operation"], dayfirst=True) >= three_months_ago)
            & (pd.to_datetime(pd_transactions["Date_operation"], dayfirst=True) <= selected_date)
        ]
        spending = filtered_transactions.groupby("Date_operation")["amount"].sum().reset_index()
        return spending

    spending_by_category(transactions_data, "Переводы", "27.08.2019 11:28:58")

    with open(os.path.join("function_report.txt"), "r") as file:
        log_content = file.read().split()
        print(log_content)

        assert log_content == ["Date_operation", "amount", "0", "27.08.2019", "11:28:58", "200.0"]


def test_log_file(transactions_data):
    @my_decorator
    def spending_category(transactions, category, date):

        if date is None:
            selected_date = datetime.today().strftime("%Y-%m-%d")
        else:
            selected_date = pd.to_datetime(date, dayfirst=True)
        pd_transactions = pd.DataFrame(transactions)
        three_months_ago = selected_date - timedelta(days=90)
        filtered_transactions = pd_transactions[
            (pd_transactions["Category"] == category)
            & (pd.to_datetime(pd_transactions["Date_operation"], dayfirst=True) >= three_months_ago)
            & (pd.to_datetime(pd_transactions["Date_operation"], dayfirst=True) <= selected_date)
        ]
        spending = filtered_transactions.groupby("Date_operation")["amount"].sum().reset_index()
        return spending

    spending_by_category(transactions_data, "Переводы", "27.08.2019 11:28:58")

    with open(os.path.join("function_report.txt"), "r") as file:
        log_content = file.read().split()
        print(log_content)

        assert log_content == ["Date_operation", "amount", "0", "27.08.2019", "11:28:58", "200.0"]


def test_spending_by_category(transactions_data):

    result = spending_by_category(transactions_data, "Красота", "01.01.2018 20:27:51")
    assert result.shape[0] == 1
    assert result["amount"].sum() == -316.0

    result = spending_by_category(transactions_data, "Переводы", "27.08.2019 11:28:58")
    assert result.shape[0] == 1
    assert result["amount"].sum() == 200.0

    result = spending_by_category(transactions_data, "Супермаркеты", "31.12.2021 16:44")
    assert result.shape[0] == 0
