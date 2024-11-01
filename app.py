import streamlit as st
import pandas as pd
import openai

# Load the stock data from the Excel file
data = pd.read_excel("1730317423-merged_stock_data_with_categories - Copy.xlsx")

# Define function to query the LLM
def query_llm(user_query):
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

    User Query: "{user_query}"

    Based on the criteria above, provide a list of stocks that match.
    Response in a simple format with stock symbols and their respective data.
    """

    # Initialize the OpenAI API client with your API key
    openai.api_key = "your-api-key-here"  # Replace with your actual OpenAI API key

    # Send to OpenAI for completion
    full_prompt = prompt_template.format(user_query=user_query)
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # Use appropriate model name
            prompt=full_prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# Set up Streamlit page
st.title("Stock Filter & Strategy Builder")
st.write("Filter stocks based on parameters like low beta, high dividend yield, low P/E ratio, and other criteria.")

# Streamlit Input for User Query
st.write("### Enter your filter criteria (example: 'low beta, high dividend yield, low P/E ratio'):")
user_query = st.text_input("User Query")

# Button to Submit Query
if st.button("Get Stock List"):
    if user_query:
        # Query the LLM for stock filtering
        response = query_llm(user_query)
        
        # Display the results from the LLM
        st.write("### Stocks that match your criteria:")
        st.write(response)
    else:
        st.write("Please enter a query to filter stocks.")

# Option to Display the Full Dataset (for reference)
if st.checkbox("Show Full Dataset"):
    st.write(data)
