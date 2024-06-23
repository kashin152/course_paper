import json

from src.services import list_transactions_sort_search
from src.utils import data_transaction


def test_list_transactions_sort_search(sort_search):
    result = list_transactions_sort_search(data_transaction, "Онлайн-кинотеатры")
    assert result == json.dumps(sort_search, sort_keys=False, ensure_ascii=False)


def test_list_transactions_sort(transactions):
    search_bar = "Игорь Б."
    result = list_transactions_sort_search(transactions, search_bar)
    expected_result = json.dumps([transactions[0], transactions[1]], ensure_ascii=False)
    assert result == expected_result

    search_bar = "Переводы"
    result = list_transactions_sort_search(transactions, search_bar)
    expected_result = json.dumps([transactions[0], transactions[1]], ensure_ascii=False)
    assert result == expected_result

    search_bar = "Non-existent string"
    result = list_transactions_sort_search(transactions, search_bar)
    expected_result = json.dumps([], ensure_ascii=False)
    assert result == expected_result

    search_bar = ""
    result = list_transactions_sort_search(transactions, search_bar)
    expected_result = json.dumps(transactions, ensure_ascii=False)
    assert result == expected_result
