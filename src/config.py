import json
import os

from dotenv import load_dotenv

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
