# Проект "Анализ транзакций в мобильном приложении Банка"

## Описание:

Проект "Анализ транзакций в мобильном приложении Банка" - это новая фича для личного кабинета клиента Банка. Это виджет, который позволяет генерирование JSON-данных для веб-страниц, формировать Excel-отчеты, а также предоставлять другие сервисы.

## Установка
1. Склонируйте репозиторий на локальную машину:
```
git@github.com:kashin152/course_paper.git
```
2. Установите необходимые зависимости:
```
poetry install
```

## Модуль views.py
Модуль формирует данные для страницы "Главная". Функция views принимает на вход строку с датой и временем в формате
YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ со следующими данными:
    Приветствие в формате "???", где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи» в зависимости от текущего времени.
    По каждой карте:
        последние 4 цифры карты;
        общая сумма расходов;
        кешбэк (1 рубль на каждые 100 рублей).
    Топ-5 транзакций по сумме платежа.
    Курс валют.
    Стоимость акций из S&P500.

### Пример использования
```python
{
    "greeting": "Добрый день", 
    "cards": [
        {
            "last_digits": "*7197", 
            "total_spent": -23562.64, 
            "cashback": 0
        }, 
        {"last_digits": "*5091", 
         "total_spent": -12742.92, 
         "cashback": 0
         }, 
        {"last_digits": "Неизвестная карта", 
         "total_spent": -55046.56, 
         "cashback": 0
         }, 
        {"last_digits": "*4556", 
         "total_spent": 198770.3, 
         "cashback": 181.0
         }
    ], 
    "top_transactions": [
        {
            "date": "30.12.2021", 
            "amount": 174000.0, 
            "category": "Пополнения", 
            "description": "Пополнение через Газпромбанк"
        }, 
        {
            "date": "22.12.2021", 
            "amount": -28001.94, 
            "category": "Переводы", 
            "description": "Перевод Кредитная карта. ТП 10.2 RUR"
        }, 
        {
            "date": "22.12.2021", 
            "amount": 28001.94, "category": 
            "Переводы", "description": 
            "Перевод Кредитная карта. ТП 10.2 RUR"
        }, 
        {
            "date": "23.12.2021", 
            "amount": 20000.0, 
            "category": "Другое", 
            "description": "Иван С."
        }, 
        {
            "date": "30.12.2021", 
            "amount": -20000.0, 
            "category": "Переводы", 
            "description": "Константин Л."
        }
    ], 
    "currency_rates": [
        {
            "currency": "USD", 
            "rate": "64.1824"
        }, 
        {
            "currency": "EUR", 
            "rate": "69.244"
        }
    ], 
    "stock_prices": [
        {
            "stock": "AAPL", 
            "price": 207.49
        }, 
        {
            "stock": "AMZN", 
            "price": 189.08
        }, 
        {
            "stock": "GOOGL", 
            "price": 179.63
        },
        {
            "stock": "MSFT",
            "price": 449.78
        }, 
        {
            "stock": "TSLA",
            "price": 183.01
        }
    ]
}
```

## Модуль utils.py
Модуль utils содержит вспомогательные функции, необходимые для работы функции страницы «Главная»

### Функция getting_data_account
Функция, которая считывает данные из файла XLSX и преобразовывает в список словарей.

### Пример использования
```python
[
  {
  'Date_operation': '03.01.2018 14:55:21', 'Payment_date': '05.01.2018', 'Card_numbers': '*7197', 'Status': 'OK', 
  'amount': -21.0, 'currency': 'RUB', 'Payment amount': -21.0, 'Payment currency': 'RUB', 'Cashback': nan, 
  'Category': 'Красота', 'MCC': 5977.0, 'Description': 'OOO Balid', 'Bonuses': 0, 'Rounding_investment_bank': 0, 
  'Amount_rounding_operation': 21.0}, 
 {'Date_operation': '01.01.2018 20:27:51', 'Payment_date': '04.01.2018', 'Card_numbers': '*7197', 'Status': 'OK', 
  'amount': -316.0, 'currency': 'RUB', 'Payment amount': -316.0, 'Payment currency': 'RUB', 'Cashback': nan, 
  'Category': 'Красота', 'MCC': 5977.0, 'Description': 'OOO Balid', 'Bonuses': 6, 'Rounding_investment_bank': 0, 
  'Amount_rounding_operation': 316.0}, 
 {'Date_operation': '01.01.2018 12:49:53', 'Payment_date': '01.01.2018', 'Card_numbers': nan, 'Status': 'OK',
  'amount': -3000.0, 'currency': 'RUB', 'Payment amount': -3000.0, 'Payment currency': 'RUB', 'Cashback': nan, 
  'Category': 'Переводы', 'MCC': nan, 'Description': 'Линзомат ТЦ Юность', 'Bonuses': 0, 'Rounding_investment_bank': 0, 
  'Amount_rounding_operation': 3000.0
  }
 ]
```
### Функция get_greeting
Функция возвращает приветствие в зависимости от времени дня.

### Пример использования
```python
"Доброй ночи"
```

### Функция get_response
Главная функция, которая передает указаннаю дату и возвращает привествие.

### Пример использования
```python
"Добрый вечер"
```
### Функция filter_by_period
Функция, которая фильтрует список словарей за период с начала месяца до указанной даты.

### Пример использования
```python
[
    {
     'Date_operation': '02.12.2021 16:26:02', 'Payment_date': '02.12.2021', 'Card_numbers': '*5091', 'Status': 'OK', 
     'amount': -5510.8, 'currency': 'RUB', 'Payment amount': -5510.8, 'Payment currency': 'RUB', 'Cashback': nan, 
     'Category': 'Каршеринг', 'MCC': 7512.0, 'Description': 'Ситидрайв', 'Bonuses': 275, 
     'Rounding_investment_bank': 0, 'Amount_rounding_operation': 5510.8}, 
    {'Date_operation': '02.12.2021 15:18:26', 'Payment_date': '02.12.2021', 'Card_numbers': '*7197', 'Status': 'OK', 
     'amount': -496.51, 'currency': 'RUB', 'Payment amount': -496.51, 'Payment currency': 'RUB', 'Cashback': nan, 
     'Category': 'Супермаркеты', 'MCC': 5411.0, 'Description': 'Магнит', 'Bonuses': 9, 'Rounding_investment_bank': 0, 
     'Amount_rounding_operation': 496.51}, 
    {'Date_operation': '02.12.2021 14:41:17', 'Payment_date': '02.12.2021', 'Card_numbers': '*7197', 'Status': 'OK', 
     'amount': -15.0, 'currency': 'RUB', 'Payment amount': -15.0, 'Payment currency': 'RUB', 'Cashback': nan, 
     'Category': 'Связь', 'MCC': 7379.0, 'Description': 'Devajs Servis.', 'Bonuses': 0, 'Rounding_investment_bank': 0, 
     'Amount_rounding_operation': 15.0
     }
]
```
### Функция information_cards
Функция, которая выводит общую сумму расходов и кэшбек по каждой карте.

### Пример использования
```python
{
    "cards": [
        {
            "last_digits": "*7197", 
            "total_spent": -23562.64, 
            "cashback": 0
        }, 
        {"last_digits": "*5091", 
         "total_spent": -12742.92, 
         "cashback": 0
         }, 
        {"last_digits": "Неизвестная карта", 
         "total_spent": -55046.56, 
         "cashback": 0
         }, 
        {"last_digits": "*4556", 
         "total_spent": 198770.3, 
         "cashback": 181.0
         }
    ]
}
```

### Функция getting_top_specified_period
Фукнция, котораая возвращает топ-5 транзакций по сумме платежа.

### Пример использования
```python
{
    "top_transactions": [
        {
            "date": "30.12.2021", 
            "amount": 174000.0, 
            "category": "Пополнения", 
            "description": "Пополнение через Газпромбанк"
        }, 
        {
            "date": "22.12.2021", 
            "amount": -28001.94, 
            "category": "Переводы", 
            "description": "Перевод Кредитная карта. ТП 10.2 RUR"
        }, 
        {
            "date": "22.12.2021", 
            "amount": 28001.94, "category": 
            "Переводы", "description": 
            "Перевод Кредитная карта. ТП 10.2 RUR"
        }, 
        {
            "date": "23.12.2021", 
            "amount": 20000.0, 
            "category": "Другое", 
            "description": "Иван С."
        }, 
        {
            "date": "30.12.2021", 
            "amount": -20000.0, 
            "category": "Переводы", 
            "description": "Константин Л."
        }
    ]
}
```
### Функция getting_data_currencies
Функция, которая получает данные о курсе валют из указанного API для заданной валюты.

### Пример использования
```python
{
    "currency_rates": [
        {
            "currency": "USD", 
            "rate": "64.1824"
        }, 
        {
            "currency": "EUR", 
            "rate": "69.244"
        }
    ]
}
```
### Функция getting_data_stock_prices
Функция, которая получает данные о ценах акции из указанного API для заданной акции.

### Пример использования
```python
{
    "stock_prices": [
        {
            "stock": "AAPL", 
            "price": 207.49
        }, 
        {
            "stock": "AMZN", 
            "price": 189.08
        }, 
        {
            "stock": "GOOGL", 
            "price": 179.63
        },
        {
            "stock": "MSFT",
            "price": 449.78
        }, 
        {
            "stock": "TSLA",
            "price": 183.01
        }
    ]
}
```

## Модуль reports.py
Модуль reports содержит функцию, в которую пользователь передает строку для поиска ивозвращается JSON-ответ со всеми транзакциями, содержащими запрос.

### Пример использования
```python
Введите слово для поиска: перевод

[
    {"Date_operation": "10.01.2018 12:41:24", "Payment_date": "10.01.2018", "Card_numbers": "*5441", "Status": "FAILED", 
     "amount": -87068.0, "currency": "RUB", "Payment amount": -87068.0, "Payment currency": "RUB", "Cashback": NaN, 
     "Category": NaN, "MCC": NaN, "Description": "Перевод с карты", "Bonuses": 0, "Rounding_investment_bank": 0, 
     "Amount_rounding_operation": 87068.0}, 
    {"Date_operation": "01.01.2018 12:49:53", "Payment_date": "01.01.2018", "Card_numbers": NaN, "Status": "OK", 
     "amount": -3000.0, "currency": "RUB", "Payment amount": -3000.0, "Payment currency": "RUB", "Cashback": NaN, 
     "Category": "Переводы", "MCC": NaN, "Description": "Линзомат ТЦ Юность", "Bonuses": 0, 
     "Rounding_investment_bank": 0, "Amount_rounding_operation": 3000.0}]
```

## Модуль services.py
Модуль services содержить фцункцию, возвращает траты по заданной категории за последние три месяца (от переданной даты). Также в данном модуле содержаться декораты, которые записывают в файл function_report.txt результат, который возвращает функция, формирующая отчет.

### Пример использования
```python
         Date_operation     amount
0   08.10.2021 11:53:58    -500.00
1   09.12.2021 01:07:48    -100.00
2   13.11.2021 18:12:17   -2000.00
3   14.10.2021 18:05:04  -10000.00
4   14.12.2021 11:04:32   -5000.00
5   16.10.2021 15:16:16     -50.00
6   16.12.2021 15:30:16    -500.00
7   17.11.2021 16:38:23  -50000.00
8   18.12.2021 17:21:34    -200.00
9   19.12.2021 18:38:09    -186.00
10  21.12.2021 12:39:50   -1198.23
11  21.12.2021 12:39:51    1198.23
12  22.10.2021 12:33:57  -63021.01
13  22.10.2021 12:33:58   63021.01
14  22.11.2021 15:02:11   -8100.00
15  22.11.2021 15:02:12    8100.00
16  22.11.2021 22:02:00   50000.08
17  22.11.2021 22:05:41 -126105.03
18  22.11.2021 22:05:42  126105.03
19  22.12.2021 23:30:44  -28001.94
20  22.12.2021 23:30:45   28001.94
21  23.12.2021 16:14:59  -10000.00
22  23.12.2021 21:01:32   -2000.00
23  24.12.2021 15:44:07   -2000.00
24  30.12.2021 22:22:03  -20000.00
25  31.10.2021 18:20:28  -10000.00
26  31.12.2021 00:12:53    -800.00

```

## Модуль main.py
Модуль main содержит вызовы результатов из всех моделей. Модуль отвечает за основную логику проекта и связывает функциональности.
### Пример использования
```python
print(main(date))
print(spending_by_category(data_transaction, "Переводы", date))
search = input("Введите слово для поиска: ").title()
print(list_transactions_sort_search(data_transaction, search))
```

## Модуль config.py
Модуль config содержит все необходимые для работы переменные.
### Пример использования
```python
url_stocks = "https://finnhub.io/api/v1/quote"

url = "https://currate.ru/api/"

current_dir = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_dir, "../user_settings.json")
with open(json_file_path, "r") as f:
    data_json = json.load(f)


date = "31-12-2021 16:44:00"

currency = "RUB"

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_STOCKS = os.getenv("API_KEY_STOCKS")

```

# Логирование
В проекте было разработано добавление логов у модулей. Логи перезаписываются в папку logs при каждом запуске функций.
### Пример использования
```python
2024-06-23 22:32:35,768 - reports - INFO - Преобразование в datetime заданой даты
2024-06-23 22:32:35,771 - reports - INFO - Преобразование списка транзакций в DataFrame
2024-06-23 22:32:35,791 - reports - INFO - Находим отчетную дату за 3 месяца
2024-06-23 22:32:35,791 - reports - INFO - Фильтруем транзакции по категории и за период последних 3-х месяцев
2024-06-23 22:32:35,885 - reports - INFO - Формируем группу отфильтрованных транзаций и выводим их сумму
2024-06-23 22:32:35,888 - reports - INFO - Выводим результат
```


# Тестирование проекта
Проект покрыт тестами на 94%. Результат был зафиксирован с помощью Code coverage.
```python
Name                     Stmts   Miss  Cover
--------------------------------------------
src\__init__.py              0      0   100%
src\config.py               14      0   100%
src\reports.py              45      2    96%
src\services.py             19      0   100%
src\utils.py               129      1    99%
src\views.py                22      0   100%
tests\__init__.py            0      0   100%
tests\conftest.py           13      1    92%
tests\test_reports.py       45     16    64%
tests\test_services.py      23      0   100%
tests\test_utils.py         85      0   100%
tests\test_views.py         24      5    79%
--------------------------------------------
TOTAL                      419     25    94%
```



## Автор
Александра Кашина

## Лицензия
Этот проект лицензирован под MIT Лицензией - см. файл LICENSE.txt для дополнительной информации.