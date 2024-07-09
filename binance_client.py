from binance.client import Client
from config import load_api_keys

api_key, api_secret = load_api_keys()
client = Client(api_key, api_secret)
