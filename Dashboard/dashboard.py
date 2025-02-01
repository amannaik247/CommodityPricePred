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
        if len(df) < 12:
            st.error("Not enough data available for predictions.")
            return

        # Extract key metrics
        current_price = df["value"].iloc[-1]  # Current price
        one_month_prediction = df["value"].iloc[-12]  # 1 month prediction
        six_month_prediction = df["value"].iloc[-6]  # 6 month prediction
        one_year_prediction = df["value"].iloc[-1]  # 1 year prediction (latest available)

        # Calculate highest price in the last year and the corresponding month
        last_year_data = df[-12:]
        highest_price = last_year_data['value'].max()
        highest_price_date = last_year_data['value'].idxmax()  # Get the date of the highest price
        highest_price_month = highest_price_date.strftime("%B %Y")  # Get the month name

        ytd_high = df['value'].max()  # YTD high
        ytd_low = df['value'].min()  # YTD low
        seven_day_average = df['value'].rolling(window=7).mean().iloc[-1]  # 7-day average

        # Combine metrics into a single bounding box
        metrics_content = f"""
        <div style="background: linear-gradient(to right, #1e3c72, #2a5298); padding: 20px; border-radius: 10px; color: white;">
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding: 20px;">
                <div style="text-align: left;">
                    <h4 style="font-size: 18px; margin: 0;">Current Price</h4>
                    <p style="font-size: 36px; margin: 0;">₹{current_price:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 18px; margin: 0;">1 Month Prediction</h4>
                    <p style="font-size: 36px; margin: 0;">₹{one_month_prediction:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 18px; margin: 0;">6 Month Prediction</h4>
                    <p style="font-size: 36px; margin: 0;">₹{six_month_prediction:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 18px; margin: 0;">1 Year Prediction</h4>
                    <p style="font-size: 36px; margin: 0;">₹{one_year_prediction:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 18px; margin: 0;">Highest Price ({highest_price_month})</h4>
                    <p style="font-size: 36px; margin: 0;">₹{highest_price:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 18px; margin: 0;">YTD High</h4>
                    <p style="font-size: 36px; margin: 0;">₹{ytd_high:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 18px; margin: 0;">YTD Low</h4>
                    <p style="font-size: 36px; margin: 0;">₹{ytd_low:.2f}</p>
                </div>
                <div style="text-align: left;">
                    <h4 style="font-size: 18px; margin: 0;">7-Day Average</h4>
                    <p style="font-size: 36px; margin: 0;">₹{seven_day_average:.2f}</p>
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
