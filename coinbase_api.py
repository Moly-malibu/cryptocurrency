import streamlit as st
import os
from coinbase.wallet.client import Client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class CoinbaseAPI:
    def __init__(self):
        # Load API keys from environment variables
        self.api_key = os.getenv('COINBASE_API_KEY')
        self.api_secret = os.getenv('COINBASE_API_SECRET')

        # Check if API key and secret are loaded correctly
        if not self.api_key or not self.api_secret:
            raise ValueError("Missing API key or secret.")

        self.client = Client(self.api_key, self.api_secret)

    def get_accounts(self):
        """Fetch account information."""
        accounts = self.client.get_accounts()
        return accounts.data

    def get_exchange_rates(self):
        """Fetch current exchange rates."""
        return self.client.get_exchange_rates()

