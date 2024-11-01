import streamlit as st
import pandas as pd

# Load the stock data from the Excel file
data = pd.read_excel("1730317423-merged_stock_data_with_categories - Copy.xlsx")

# Set up Streamlit page
st.title("Stock Filter & Strategy Builder")
st.write("Filter stocks based on parameters like low beta, high dividend yield, low P/E ratio, and other criteria.")

# Streamlit Input for User Query
st.write("### Enter your filter criteria (e.g., 'low beta, high dividend yield, low P/E ratio'):")
user_query = st.text_input("User Query")

# Define function to filter stocks based on user criteria
def filter_stocks(data, user_query):
    filters = user_query.lower().split(",")
    filtered_data = data.copy()
    
    for filter_str in filters:
        filter_str = filter_str.strip()
        if "low beta" in filter_str:
            filtered_data = filtered_data[filtered_data['beta'] < 1]
        if "high dividend yield" in filter_str:
            filtered_data = filtered_data[filtered_data['fiveYearAvgDividendYield'] > 3]  # Example threshold
        if "low p/e ratio" in filter_str:
            filtered_data = filtered_data[filtered_data['P/E Ratio'] < 15]  # Example threshold
        # Add more filtering conditions as needed

    return filtered_data

# Button to Submit Query
if st.button("Get Stock List"):
    if user_query:
        # Filter the stocks based on user query
        filtered_stocks = filter_stocks(data, user_query)

        # Display the results
        if not filtered_stocks.empty:
            st.write("### Stocks that match your criteria:")
            st.write(filtered_stocks)
        else:
            st.write("No stocks match your criteria.")
    else:
        st.write("Please enter a query to filter stocks.")

# Option to Display the Full Dataset (for reference)
if st.checkbox("Show Full Dataset"):
    st.write(data)
