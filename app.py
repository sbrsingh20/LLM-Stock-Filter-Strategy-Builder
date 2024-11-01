import streamlit as st
import pandas as pd
import openai

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

# Define the LLM Prompt Template
prompt_template = """
You are a financial assistant with access to a large stock dataset.
Users will input parameters to filter stocks and build strategies.

Available parameters for filtering include:
- Low Beta (Beta < 1)
- High Dividend Yield
- Low P/E Ratio
- Low Volatility
- High Return on Investment
- Payout Ratio
- Five-Year Average Dividend Yield
- Volume
- Regular Market Volume
- Average Volume
- Average Volume (10 days)
- Average Daily Volume (10 days)
- 200-Day Moving Average
- Trailing Annual Dividend Rate

Columns in the dataset: {columns}

User Query: "{user_query}"

Response:
"""

# Initialize the OpenAI API client with your API key
openai.api_key = "your-api-key-here"  # Replace with your actual OpenAI API key

# Function to Query the LLM
def query_llm(user_query):
    columns = ", ".join(data.columns)
    full_prompt = prompt_template.format(columns=columns, user_query=user_query)

    # Send to OpenAI for completion
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use appropriate model name
            prompt=full_prompt,
            max_tokens=150,
            temperature=0.7
        )
        # Extract the response text
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit Input for User Query
st.write("### Enter your filter criteria:")
user_query = st.text_input("Example: 'List low beta stocks with high dividend yield and low P/E ratio'")

# Button to Submit Query
if st.button("Get Stock List"):
    if user_query:
        response = query_llm(user_query)
        st.write("### Stocks that match your criteria:")
        st.write(response)
    else:
        st.write("Please enter a query to filter stocks.")

# Option to Display the Full Dataset (for reference)
if st.checkbox("Show Full Dataset"):
    st.write(data)
