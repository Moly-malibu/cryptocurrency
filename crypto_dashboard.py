import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# Function to fetch cryptocurrency prices (mock data for demonstration)
def fetch_crypto_data():
    data = {
        'Name': ['Bitcoin', 'Ethereum', 'Ripple', 'Litecoin'],
        'Price': [40000, 2500, 1.2, 150],
        'Market Cap': [750000000000, 300000000000, 60000000000, 10000000000],
        'Volume': [35000000000, 20000000000, 1500000000, 500000000]
    }
    return pd.DataFrame(data)

# Fetch the data
crypto_df = fetch_crypto_data()

# Streamlit app layout
st.title("Cryptocurrency Dashboard")

# Display a selectbox for choosing a cryptocurrency
selected_crypto = st.selectbox("Select Cryptocurrency", crypto_df['Name'])

# Display selected cryptocurrency details
selected_data = crypto_df[crypto_df['Name'] == selected_crypto]
st.write("### Selected Cryptocurrency Details")
st.write(selected_data)

# Create an interactive bar chart for price comparison
fig = px.bar(crypto_df, x='Name', y='Price', title='Cryptocurrency Prices')
st.plotly_chart(fig)

# Create a line chart for historical prices (mock historical data)
historical_data = {
    'Date': pd.date_range(start='2023-01-01', periods=30),
    'Bitcoin': [40000 + i * (-100 + i % 5) for i in range(30)],
    'Ethereum': [2500 + i * (-10 + i % 2) for i in range(30)],
}

historical_df = pd.DataFrame(historical_data).melt(id_vars='Date', var_name='Cryptocurrency', value_name='Price')
line_fig = px.line(historical_df, x='Date', y='Price', color='Cryptocurrency', title='Historical Prices')
st.plotly_chart(line_fig)


import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# Function to fetch all cryptocurrencies from Coinbase
def fetch_all_cryptocurrencies():
    url = "https://api.pro.coinbase.com/currencies"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # Returns the full JSON response
    else:
        st.error("Error fetching data from Coinbase API")
        return []

# Function to fetch historical price data for a given cryptocurrency pair
def fetch_historical_data(pair):
    url = f"https://api.pro.coinbase.com/products/{pair}/candles?granularity=86400"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Convert the data into a DataFrame
        df = pd.DataFrame(data, columns=['time', 'low', 'high', 'open', 'close', 'volume'])
        df['time'] = pd.to_datetime(df['time'], unit='s')  # Convert time to datetime
        return df
    else:
        st.error("Error fetching historical data.")
        return pd.DataFrame()  # Return an empty DataFrame on error

# Fetch all cryptocurrencies
cryptocurrencies = fetch_all_cryptocurrencies()

# Create a DataFrame for easier manipulation
if not cryptocurrencies:
    st.error("No cryptocurrencies found.")
else:
    crypto_df = pd.DataFrame(cryptocurrencies)

    # Streamlit app layout
    st.title("Coinbase Cryptocurrency Dashboard")

    # Display all cryptocurrencies in a table format
    st.write("### All Available Cryptocurrencies")
    st.dataframe(crypto_df[['id', 'name', 'min_size']])

    # Select cryptocurrency pair for historical data
    selected_crypto = st.selectbox("Select Cryptocurrency", crypto_df['id'].tolist())

    if selected_crypto:
        # Fetch historical data for the selected cryptocurrency (e.g., BTC-USD)
        historical_data = fetch_historical_data(f"{selected_crypto}-USD")

        if not historical_data.empty:
            # Plotting historical prices using Plotly
            fig = px.line(historical_data, x='time', y='close', title=f'Historical Prices of {selected_crypto}')
            st.plotly_chart(fig)

            # Display additional metrics (like volume)
            st.write("### Historical Volume Data")
            st.bar_chart(historical_data.set_index('time')['volume'])

            # Optionally display more details about the selected cryptocurrency
            selected_data = crypto_df[crypto_df['id'] == selected_crypto]
            if not selected_data.empty:
                st.write("### Selected Cryptocurrency Details")
                st.write(selected_data[['id', 'name', 'min_size']])
