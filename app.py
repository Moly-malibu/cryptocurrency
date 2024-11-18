# app.py
import streamlit as st
from coinbase_api import CoinbaseAPI
from decorators import cache_data

# Initialize the Coinbase API client
coinbase_api = CoinbaseAPI()

@cache_data
def fetch_accounts():
    """Fetch accounts from Coinbase."""
    return coinbase_api.get_accounts()

@cache_data
def fetch_exchange_rates():
    """Fetch exchange rates from Coinbase."""
    return coinbase_api.get_exchange_rates()

# Streamlit app layout
st.title("Coinbase Cryptocurrency Tracker")

if st.button("Fetch Accounts"):
    try:
        accounts = fetch_accounts()
        for account in accounts:
            st.write(f"Account: {account.name}, Balance: {account.balance.amount} {account.balance.currency}")
    except Exception as e:
        st.error(f"Error fetching accounts: {e}")

if st.button("Fetch Exchange Rates"):
    try:
        rates = fetch_exchange_rates()
        st.write("Current Exchange Rates:")
        st.json(rates)
    except Exception as e:
        st.error(f"Error fetching exchange rates: {e}")
