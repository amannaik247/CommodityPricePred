import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit.errors import StreamlitAPIException
import os
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

# Set page config
st.set_page_config(page_title="Commodity Dashboard", page_icon="📊", layout="wide")

# Define commodities
commodities = {
    "Onion": "🧅",
    "Potato": "🥔",
    "Tomato": "🍅",
    "Rice": "🍚",
    "Urad Dal": "🌾"
}

# Function to display commodity selection
def display_commodity_selection():
    st.title("Select a Commodity")

    st.markdown(
        """
        <style>
            .stButton>button {
                width: 100%;
                height: 60px;
                font-size: 50px;
                border-radius: 10px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    commodities_list = list(commodities.items())

    # First row (3 buttons)
    cols = st.columns(3)
    for idx in range(3):
        with cols[idx]:
            commodity, icon = commodities_list[idx]
            if st.button(f"{icon} {commodity}", key=f"{commodity}_{idx}"):
                st.session_state.selected_commodity = commodity

    # Second row (2 buttons, left-aligned)
    cols = st.columns(3)  # Keep the same column structure
    for idx in range(3, 5):
        with cols[idx - 3]:  # Start from the first column to left-align
            commodity, icon = commodities_list[idx]
            if st.button(f"{icon} {commodity}", key=f"{commodity}_{idx}"):
                st.session_state.selected_commodity = commodity



# Function to display the dashboard for the selected commodity
def display_dashboard():
    commodity = st.session_state.selected_commodity
    
    st.title(f"{commodity} Dashboard")

    # Load the corresponding CSV file for the selected commodity
    file_path = f"Dashboard/download/{commodity.lower().replace(' ', '_')}_future.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, index_col=0, parse_dates=True)  # Set the first column as index and parse dates
        df = df.dropna()  # Remove rows with NaN values

        # Check if the DataFrame has enough data
        if len(df) < 14:
            st.error("Not enough data available for predictions.")
            return

        # Extract key metrics
        current_price = df["value"].iloc[-13]  # Current price
        one_month_prediction = df["value"].iloc[-12]  # 1 month prediction
        six_month_prediction = df["value"].iloc[-6]  # 6 month prediction
        one_year_prediction = df["value"].iloc[-1]  # 1 year prediction (latest available)

        # Calculate highest price in the last year and the corresponding month
        last_year_data = df[-12:]
        highest_price = last_year_data['value'].max()
        highest_price_date = last_year_data['value'].idxmax()  # Get the date of the highest price
        highest_price_month = highest_price_date.strftime("%B %Y")  # Get the month name

        # Calculate lowest price in the last year and the corresponding month
        last_year_data = df[-12:]
        lowest_price = last_year_data['value'].min()
        lowest_price_date = last_year_data['value'].idxmin()  # Get the date of the lowest price
        lowest_price_month = lowest_price_date.strftime("%B %Y")  # Get the month name

        # Calculate percentage change from previous month to current month
        previous_month_price = df["value"].iloc[-14]  # Price from two months ago
        percentage_change = ((current_price - previous_month_price) / previous_month_price) * 100
        
        # Calculate average price for the whole 1 year prediction
        average_price_this_year = df["value"].iloc[-12:].mean()  # Average price for the last year

        # Combine metrics into a single bounding box
        metrics_content = f"""
        <div style="background: linear-gradient(to right, #1e3c72, #2a5298); padding: 20px; border-radius: 10px; color: white;">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding: 20px;">
                <div style="text-align: left;">
                    <h4 style="font-size: 12px; margin: -10;">Current Price</h4>
                    <p style="font-size: 36px; margin: -10;">₹{current_price:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 12px; margin: -10;">1 Month Prediction</h4>
                    <p style="font-size: 36px; margin: -10;">₹{one_month_prediction:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 12px; margin: -10;">6 Month Prediction</h4>
                    <p style="font-size: 36px; margin: -10;">₹{six_month_prediction:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 12px; margin: -10;">1 Year Prediction</h4>
                    <p style="font-size: 36px; margin: -10;">₹{one_year_prediction:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 12px; margin: -10;">Highest Price ({highest_price_month})</h4>
                    <p style="font-size: 36px; margin: -10;">₹{highest_price:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 12px; margin: -10;">Lowest Price ({lowest_price_month})</h4>
                    <p style="font-size: 36px; margin: -10;">₹{lowest_price:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 12px; margin: -10;">% Change from Previous Month</h4>
                    <p style="font-size: 36px; margin: -10;">{percentage_change:.2f}%</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 12px; margin: -10;">Average Price (225)</h4>
                    <p style="font-size: 36px; margin: -10;">₹{average_price_this_year:.2f}</p>
                </div>
            </div>
        </div>
        """

        # Display the combined metrics content
        st.markdown(metrics_content, unsafe_allow_html=True)

        # Visualizations
        st.subheader("Price Over Time")
        line_fig = px.line(df, x=df.index, y="value", title=f"{commodity} Price Over Time")  # Use index for x-axis
        st.plotly_chart(line_fig)

        # Display the last 12 months of data
        st.subheader("Last 12 Months of Data")
        last_12_months_df = df.last('12M')  # Get the last 12 months of data

        # Format the index to show only year, month, and day
        last_12_months_df.index = last_12_months_df.index.strftime('%Y-%m-%d')

        # Style the DataFrame for better presentation
        styled_df = last_12_months_df.style.format({"value": "₹{:.2f}"}) \
            .set_table_attributes('style="width: 100%; border-collapse: collapse;"') \
            .set_properties(**{'text-align': 'left', 'font-size': '14px'}) \
            .set_table_styles([{
                'selector': 'th',
                'props': [('background-color', '#1e3c72'), ('color', 'white'), ('font-size', '16px')]
            }, {
                'selector': 'td',
                'props': [('border', '1px solid #ddd'), ('padding', '8px')]
            }])

        st.dataframe(styled_df)  # Display the styled DataFrame

        # Provide a download option for the DataFrame
        csv = last_12_months_df.to_csv(index=True).encode('utf-8')
        st.download_button(
            label="Download Last 12 Months Data",
            data=csv,
            file_name=f"{commodity.lower().replace(' ', '_')}_last_12_months.csv",
            mime="text/csv",
        )

    else:
        st.error(f"No data available for {commodity}.")

def main():
    if "selected_commodity" not in st.session_state:
        st.session_state.selected_commodity = None

    if st.session_state.selected_commodity:
        display_commodity_selection()
        display_dashboard()
        if st.button("Back to Selection"):
            st.session_state.selected_commodity = None
    else:
        display_commodity_selection()

if __name__ == "__main__":
    main()
