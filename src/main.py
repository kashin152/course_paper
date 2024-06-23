from src.config import date
from src.reports import spending_by_category
from src.services import list_transactions_sort_search
from src.utils import data_transaction
from src.views import main

print(main(date))
print(spending_by_category(data_transaction, "Переводы", date))
search = input("Введите слово для поиска: ").title()
print(list_transactions_sort_search(data_transaction, search))
