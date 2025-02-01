import streamlit as st
from PIL import Image
import base64


# Function to set the background image
def set_background_image(image_path):
    """Set background image for the page."""
    try:
        with open(image_path, "rb") as f:
            img_data = f.read()
        b64_img = base64.b64encode(img_data).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.5)), url('data:image/jpeg;base64,{b64_img}');
                background-size: cover;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"Error loading background image: {e}")


def set_custom_fonts():
    """Add custom font styles to the app."""
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Roboto:wght@400;500&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            font-size: 18px;
            color: white !important;
        }

        .stTitle {
            font-size: 60px;
            color: #FFD700 !important;
            font-weight: bold;
        }

        .sidebar .sidebar-content {
            font-family: 'Roboto', sans-serif;
            font-size: 20px;
            color: white !important;
        }

        h1, h2, h3 {
            font-family: 'Montserrat', sans-serif;
            color: #FFD700 !important;
        }

        .stHeader {
            font-size: 36px;
            color: #FFD700 !important;
        }

        button {
            font-size: 14px;
            font-family: 'Arial', sans-serif;
            color: white !important;
        }

        .stMarkdown {
            font-size: 20px;
            color: white !important;
        }

        p, span, div, li, .stTextInput > div > div > input {
            color: white !important;
        }

        .stMarkdown, .stText {
            color: white !important;
        }

        .stRadio > label {
            color: white !important;
        }

        .css-1d391kg, .css-1d391kg a {
            color: white !important;
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    # Set page config
    st.set_page_config(
        page_title="Agriculture Dashboard", page_icon="🌾", layout="wide"
    )

    # Set background image
    set_background_image("agriculture_background.jpg")

    # Apply custom font styles
    set_custom_fonts()

    # Title and description
    st.title("Commodity AI 🌾")
    st.markdown(
        """
        Revolutionizing commodity price tracking with AI-driven insights, forecasts, and sentiment analysis for smarter decision-making. 
        Navigate using the sidebar to use our features
        """
    )

    # Add interactive components
    st.sidebar.title("Know About Our Features")
    page = st.sidebar.radio(
        "Select One: ", ("Dashboard?", "Price Forecast?", "Sentiment Analysis?")
    )

    if page == "Dashboard?":
        st.header("📊 Dashboard")
        st.write(
            """ 
            Provides real-time updates, interactive visualizations, and historical
            data analysis for selected commodities prices.
            """
        )

    # elif page == "Price Forecast?":
    #     st.header("👥 Price Forecast")
    #     st.write(
    #         """
    #         Uses a trained LSTM multivariate model to predict future prices
    #         based on past data and seasonal trends.
    #         """
    #     )

    elif page == "Sentiment Analysis?":
        st.header("🤖 Sentiment Analysis")
        st.write(
            """
            An AI agent that fetches relevant articles and analyzes sentiment
            to predict market trends and potential price movements.
            """
        )

    # Footer
    st.sidebar.markdown("---")
    st.sidebar.markdown("Open Github for more details")


if __name__ == "__main__":  # Fixed the condition here
    main()
