import streamlit as st
import pandas as pd

# Sample stock data with additional columns
data = pd.DataFrame({
    'payoutRatio': [10, 30, 60],
    'fiveYearAvgDividendYield': [1.5, 3, 5],
    'beta': [0.7, 1.0, 1.5],
    'volume': [500000, 5000000, 15000000],
    'regularMarketVolume': [500000, 2000000, 12000000],
    'averageVolume': [800000, 2000000, 12000000],
    'averageVolume10days': [500000, 5000000, 12000000],
    'averageDailyVolume10Day': [600000, 1500000, 15000000],
    'twoHundredDayAverage': [0.95, 1.0, 1.1],
    'trailingAnnualDividendRate': [1.5, 3.5, 5],
    # Add other columns for remaining parameters as needed
})

# Define function to categorize based on provided thresholds
def categorize(value, low, medium, high, category_type='numeric'):
    if category_type in ['numeric', 'percent', 'volume']:
        if value < low:
            return 'Low'
        elif low <= value <= high:
            return 'Medium'
        else:
            return 'High'
    elif category_type == 'moving_average':
        if value < low:
            return 'Below Average'
        elif low <= value <= high:
            return 'Within Average'
        else:
            return 'Above Average'

# Apply categorization for each parameter based on thresholds
data['payoutRatio_Category'] = data['payoutRatio'].apply(lambda x: categorize(x, 20, 50, 100, 'numeric'))
data['fiveYearAvgDividendYield_Category'] = data['fiveYearAvgDividendYield'].apply(lambda x: categorize(x, 2, 4, 10, 'percent'))
data['beta_Category'] = data['beta'].apply(lambda x: categorize(x, 0.8, 1.2, 2, 'numeric'))
data['volume_Category'] = data['volume'].apply(lambda x: categorize(x, 1_000_000, 10_000_000, 20_000_000, 'volume'))
data['regularMarketVolume_Category'] = data['regularMarketVolume'].apply(lambda x: categorize(x, 1_000_000, 10_000_000, 20_000_000, 'volume'))
data['averageVolume_Category'] = data['averageVolume'].apply(lambda x: categorize(x, 1_000_000, 10_000_000, 20_000_000, 'volume'))
data['averageVolume10days_Category'] = data['averageVolume10days'].apply(lambda x: categorize(x, 1_000_000, 10_000_000, 20_000_000, 'volume'))
data['averageDailyVolume10Day_Category'] = data['averageDailyVolume10Day'].apply(lambda x: categorize(x, 1_000_000, 10_000_000, 20_000_000, 'volume'))
data['twoHundredDayAverage_Category'] = data['twoHundredDayAverage'].apply(lambda x: categorize(x, 0.95, 1.05, 1.2, 'moving_average'))
data['trailingAnnualDividendRate_Category'] = data['trailingAnnualDividendRate'].apply(lambda x: categorize(x, 2, 4, 10, 'percent'))

# Set up Streamlit page
st.title("Stock Filter & Strategy Builder")
st.write("Filter stocks based on parameters like low beta, high dividend yield, low P/E ratio, and other criteria.")

# Streamlit Input for User Query
st.write("### Enter your filter criteria (comma separated):")
user_input = st.text_area("Example: 'low beta, high dividend yield, low P/E ratio'")

# Function to filter stocks based on user input conditions
def filter_stocks(df, conditions):
    mask = pd.Series([True] * len(df))  # Start with all True (no filtering)

    for condition in conditions:
        condition = condition.strip().lower()  # Clean up condition input
        
        if "low beta" in condition:
            mask &= (df['beta'] < 1)
        elif "high dividend yield" in condition:
            mask &= (df['fiveYearAvgDividendYield'] > 4)
        elif "low p/e ratio" in condition:
            mask &= (df['payoutRatio'] < 15)
        elif "low volatility" in condition:
            mask &= (df['volume'] < 1_000_000)
        elif "high return on investment" in condition:
            mask &= (df['trailingAnnualDividendRate'] > 3)
        # Add more conditions based on user input as needed

    return df[mask]

# Button to Submit Query
if st.button("Get Stock List"):
    if user_input:
        conditions = [cond.strip().lower() for cond in user_input.split(',')]
        filtered_stocks = filter_stocks(data, conditions)
        
        if not filtered_stocks.empty:
            st.write("### Stocks that match your criteria:")
            st.dataframe(filtered_stocks)
        else:
            st.write("No stocks match the selected criteria.")
    else:
        st.write("Please enter a query to filter stocks.")

# Option to Display the Full Dataset (for reference)
if st.checkbox("Show Full Dataset"):
    st.write(data)
