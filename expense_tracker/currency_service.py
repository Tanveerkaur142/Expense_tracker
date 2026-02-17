# currency_service.py

import requests

# Define your API URL and key if needed
API_URL = 'https://api.exchangerate-api.com/v4/latest/USD'  # Replace with your chosen API's URL

def get_exchange_rates():
    """Fetch exchange rates from the API."""
    response = requests.get(API_URL)
    data = response.json()
    return data['rates']

def convert_currency(amount, from_currency, to_currency):
    """Convert amount from one currency to another."""
    rates = get_exchange_rates()
    
    if from_currency == to_currency:
        return amount

    if from_currency != 'USD':
        amount /= rates[from_currency]
    
    converted_amount = round(amount * rates[to_currency], 2)
    return converted_amount
