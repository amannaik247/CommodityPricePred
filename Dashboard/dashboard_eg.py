import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")

# Set page config
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# # Update the folder_path definition
# folder_path = os.path.join(
#     os.path.dirname(os.path.dirname(__file__)), "Dashboard\download"
# )

folder_path = "Dashboard/download"


def get_csv_from_folder(folder_path):
    print("folder_path: ", folder_path)
    # Create folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out the CSV files
    csv_files = [file for file in files if file.endswith(".csv")]

    # Check if there are any CSV files
    if len(csv_files) == 0:
        st.warning("No CSV file found in the folder. Please upload a CSV file.")

        # Add file uploader
        uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])
        if uploaded_file is not None:
            # Save the uploaded file
            file_path = os.path.join(folder_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            return file_path
        return None

    # Return the full path of the first CSV file
    return os.path.join(folder_path, csv_files[0])


def main():
    try:
        # Get CSV file
        file = get_csv_from_folder(folder_path)

        if file is None:
            st.info("Please upload a CSV file to continue.")
            return

        # Read CSV file with specific options to avoid warnings
        df = pd.read_csv(file, storage_options=None)
        # Convert date column to datetime with errors='coerce'
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])  # Remove rows with invalid dates

        st.header("Dashboard")

        # Add custom CSS for the metrics box
        st.markdown(
            """
        <style>
        div[data-testid="stHorizontalBlock"] {
            background: linear-gradient(to bottom right, #1e3799, #0c2461);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        div[data-testid="metric-container"] {
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
        }
        div[data-testid="metric-container"] label {
            color: white !important;
        }
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: white !important;
        }
        div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
            color: white !important;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

        st.header("Key Metrics", divider="rainbow")

        # Calculate key metrics
        current_price = df["value"].iloc[-1]
        previous_price = df["value"].iloc[-2]
        daily_change = ((current_price - previous_price) / previous_price) * 100

        # Monthly calculations
        last_30_days = df.tail(30)
        monthly_avg = last_30_days["value"].mean()

        # YTD calculations
        current_year = pd.Timestamp.now().year
        ytd_data = df[df["date"].dt.year == current_year]
        ytd_high = ytd_data["value"].max()
        ytd_low = ytd_data["value"].min()

        # Rolling average and volatility
        rolling_7day_avg = df["value"].rolling(window=7).mean().iloc[-1]
        price_volatility = df["value"].std()

        # Percentage difference from monthly average
        pct_diff_monthly = ((current_price - monthly_avg) / monthly_avg) * 100

        # Display metrics in columns
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Current Price", f"₹{current_price:.2f}")
            st.metric("Daily Change", f"{daily_change:.2f}%")

        with col2:
            st.metric("Monthly Average", f"₹{monthly_avg:.2f}")
            st.metric("% Diff from Monthly Avg", f"{pct_diff_monthly:.2f}%")

        with col3:
            st.metric("YTD High", f"₹{ytd_high:.2f}")
            st.metric("YTD Low", f"₹{ytd_low:.2f}")

        with col4:
            st.metric("7-Day Average", f"₹{rolling_7day_avg:.2f}")
            st.metric("Price Volatility", f"₹{price_volatility:.2f}")
        # # Close the metrics box div
        # st.markdown("</div>", unsafe_allow_html=True)

        # Check if required columns exist
        if "date" in df.columns and "value" in df.columns:

            ### Date Range Filter ###
            st.subheader("Select Date Range")
            col1, col2 = st.columns(2)

            # Set default dates
            min_date = df["date"].min()
            max_date = df["date"].max()
            default_start = pd.to_datetime("2014-01-01")
            default_end = pd.to_datetime("2018-12-31")

            with col1:
                start_date = st.date_input(
                    "Start Date",
                    value=default_start,
                    min_value=min_date.date(),
                    max_value=max_date.date(),
                )

            with col2:
                end_date = st.date_input(
                    "End Date",
                    value=default_end,
                    min_value=min_date.date(),
                    max_value=max_date.date(),
                )

            if start_date <= end_date:
                mask = (df["date"].dt.date >= start_date) & (
                    df["date"].dt.date <= end_date
                )
                df_filtered = df[mask]

                st.subheader(f"Filtered Data from {start_date} to {end_date}")
                st.dataframe(df_filtered)

                if not df_filtered.empty:
                    ### Visualizations ###
                    st.subheader("Interactive Line Chart")
                    line_fig = px.line(
                        df_filtered,
                        x="date",
                        y="value",
                        title="Value Over Time",
                        labels={"date": "Date", "value": "Value"},
                        template="plotly_dark",
                    )
                    st.plotly_chart(line_fig)

                    st.subheader("Interactive Bar Chart")
                    bar_fig = px.bar(
                        df_filtered,
                        x="date",
                        y="value",
                        title="Value Distribution",
                        labels={"date": "Date", "value": "Value"},
                        color="value",
                        color_continuous_scale="Viridis",
                        template="plotly_dark",
                    )
                    st.plotly_chart(bar_fig)

                    st.subheader("Interactive Scatter Plot")
                    scatter_fig = px.scatter(
                        df_filtered,
                        x="date",
                        y="value",
                        size="value",
                        title="Scatter Plot of Value",
                        labels={"date": "Date", "value": "Value"},
                        color="value",
                        color_continuous_scale="Plasma",
                        template="plotly_dark",
                    )
                    st.plotly_chart(scatter_fig)
                else:
                    st.warning("No data available for the selected date range.")
            else:
                st.error("Error: End date must be after start date")
        else:
            st.error(
                f"Required columns (date, value) not found. Available columns: {df.columns.tolist()}"
            )

    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        import traceback

        st.error(f"Detailed error: {traceback.format_exc()}")


if __name__ == "__main__":
    main()
