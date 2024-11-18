import streamlit as st

def cache_data(func):
    """Decorator to cache data fetching."""
    def wrapper(*args, **kwargs):
        if 'coinbbase_data' not in st.session_state:
            st.session_state.crypto_data = func(*args, **kwargs)
        return st.session_state.crypto_data
    return wrapper