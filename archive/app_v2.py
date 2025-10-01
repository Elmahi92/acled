import streamlit as st
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
import pandas as pd
import numpy as np

from streamlit_extras.grid import grid
from streamlit_extras.metric_cards import style_metric_cards
st.set_page_config(layout="wide")

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import time
from utils import fetch_acled_data
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# Cache the data to avoid reloading it with each interaction
@st.cache_data
def load_acled_data():
    data = fetch_acled_data()
    data['fatalities'] = pd.to_numeric(data['fatalities'], errors='coerce')
    data['event_date'] = pd.to_datetime(data['event_date'])
    data['month_year'] = data['event_date'].dt.to_period('M')
    return data

# Load data
acled_data = load_acled_data()

# Compute key metrics
total_fatalities = acled_data['fatalities'].sum()
total_incidents = acled_data.shape[0]
total_battles=acled_data.groupby('event_type')['event_id_cnty'].count().reset_index().loc[lambda x: x['event_type'] == "Battles", 'event_id_cnty'][0]
total_Explosions_Remote_violence=acled_data.groupby('event_type')['event_id_cnty'].count().reset_index().loc[lambda x: x['event_type'] == "Explosions/Remote violence", 'event_id_cnty'][1]
total_Strategic_developments=acled_data.groupby('event_type')['event_id_cnty'].count().reset_index().loc[lambda x: x['event_type'] == "Strategic developments", 'event_id_cnty'][4]
total_Violence_against_civilians=acled_data.groupby('event_type')['event_id_cnty'].count().reset_index().loc[lambda x: x['event_type'] == "Violence against civilians", 'event_id_cnty'][5]
latest_month = acled_data['month_year'].max()
states_affected = acled_data['admin1'].nunique()
localties_affected = acled_data['admin2'].nunique()
previous_month = latest_month - 1

# Get fatalities for the latest and previous months
fatalities_latest_month = acled_data[acled_data['month_year'] == latest_month]['fatalities'].sum()
fatalities_previous_month = acled_data[acled_data['month_year'] == previous_month]['fatalities'].sum()
# Group by month_year and sum fatalities
monthly_fatalities = acled_data.groupby('month_year')['fatalities'].sum().reset_index()
# Calculate month-over-month fatalities percentage change
fatalities_percentage_change = ((fatalities_latest_month - fatalities_previous_month) / fatalities_previous_month) * 100
fatalities_percentage_change = round(fatalities_percentage_change, 2)



# Calculate the difference in days and hours since April 13, 2023
start_date = date(2023, 4, 13)
current_date = date.today()
days_difference = (current_date - start_date).days
hours_difference = (current_date - start_date).total_seconds() / 3600

# Title and Date Calculations
st.title("Echoes of Hope 🕊️")
st.title("Sudan’s Descent: A Nation Torn by War and Unyielding Despair")
st.divider()
st.markdown("""
What would it feel like to wake up one morning and find your world turned upside down, your streets engulfed in chaos,
and your future uncertain? This is the reality for the civilians of Sudan, who, in :red[April 2023], opened their eyes to a
nightmare they could scarcely imagine. Two powerful generals—leaders of the :orange[Rapid Support Forces] and the :green[Sudanese
Armed Forces]—had plunged the nation into a brutal struggle for power, and ordinary lives became collateral damage.

Imagine being forced from your home, your family scattered, with nothing left but fear and survival instincts. Where do
you turn when millions are displaced, food is scarce, and disease lurks in every corner? How do you hold onto hope
when famine begins to tighten its grip, and the familiar rhythms of life are replaced by desperation?

This is the haunting reality of Sudan today—a nation caught in the relentless grip of conflict, left to wonder what
tomorrow might bring.
""")

st.subheader("The Numbers Behind the Crisis")

def style_metric_cards():
    st.markdown("""
    <style>
    div.stMetric {
        position: relative; /* Enable positioning for child elements */
        background-color: #2B2B2B; /* Card background color */
        padding: 20px; /* Padding inside the card */
        border-radius: 12px; /* Rounded corners */
        box-shadow: 2px 2px 8px rgba(0, 0, 0, ); /* Shadow effect */
        margin: auto; /* Center the card in the column */
        width: auto; /* Set card width */
        text-align: center; /* Center align text */
    }
    div.stMetric .icon-container {
        position: absolute; /* Position the icon relative to the card */
        top: 10px; /* Adjust vertical position */
        right: 10px; /* Adjust horizontal position */
        width: 24px; /* Icon width */
        height: 24px; /* Icon height */
    }
    div.stMetric .icon-container svg {
        width: 100%; /* Scale the icon to fit the container */
        height: auto;
        fill: white; /* Change icon color to white */
    }
    div[data-testid="stMetricValue"] {
        font-size: 36px; /* Main value font size */
        font-weight: bold;
        color: white;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px; /* Label font size */
        color: lightgray;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 16px; /* Delta font size */
        font-weight: bold;
        color: #FF4B4B; /* Red for positive percentage */
    }
    </style>
    """, unsafe_allow_html=True)

# Create the Dashboard Layout
def dashboard():
    # Row 1
    col1, col2, col3, col4 = st.columns(4)
    # Card with Icon Example
    with col1:
        # Card 1
        st.markdown(f"""
        <div class="stMetric" style="margin-bottom: 20px;"> <!-- Adds margin between cards -->
            <div class="icon-container">
                <!-- SVG Icon -->
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="currentColor">
                    <path d="M464 256c0-114.87-93.13-208-208-208S48 141.13 48 256s93.13 208 208 208 208-93.13 208-208zm-324.45 32H80c-4.42 0-8-3.58-8-8v-16c0-4.42 3.58-8 8-8h59.55C127.93 241.36 120 222.84 120 203.11c0-44.11 35.89-80 80-80 26.47 0 49.93 12.9 64.55 32.8 14.62-19.9 38.08-32.8 64.55-32.8 44.11 0 80 35.89 80 80 0 19.74-7.93 38.26-19.55 52.89H448c4.42 0 8 3.58 8 8v16c0 4.42-3.58 8-8 8h-59.55C400.07 302.64 408 321.16 408 340.89c0 44.11-35.89 80-80 80-26.47 0-49.93-12.9-64.55-32.8-14.62 19.9-38.08 32.8-64.55 32.8-44.11 0-80-35.89-80-80 0-19.74 7.93-38.26 19.55-52.89z"/>
                </svg>
            </div>
            <div>
                <div data-testid="stMetricLabel">Number of Fatalities</div>
                <div data-testid="stMetricValue">{total_fatalities}</div>
                <div data-testid="stMetricDelta"> {fatalities_percentage_change} MoM</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # bottom long cart element 1
        st.markdown(f"""
        <div class="stMetric" style="width: 350px; height: 150px;"> <!-- Card size -->
            <div>
                <div data-testid="stMetricLabel">Total Battles Recorded</div>
                <div data-testid="stMetricValue">{total_battles}</div>
                <div data-testid="stMetricDelta">+40% MoM</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        # Card 2
        st.markdown(f"""
        <div class="stMetric" style="margin-bottom: 20px;"> <!-- Adds margin between cards -->
            <div class="icon-container">
                <!-- SVG Icon -->
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="currentColor">
                    <path d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256s256-114.6 256-256S397.4 0 256 0zM256 464c-114.7 0-208-93.31-208-208S141.3 48 256 48s208 93.31 208 208S370.7 464 256 464zM256 112c-79.41 0-144 64.59-144 144s64.59 144 144 144s144-64.59 144-144S335.4 112 256 112zM256 352c-52.94 0-96-43.06-96-96s43.06-96 96-96s96 43.06 96 96S308.9 352 256 352zM256 208c-26.47 0-48 21.53-48 48s21.53 48 48 48s48-21.53 48-48S282.5 208 256 208z"/>
                </svg>
            </div>
            <div>
                <div data-testid="stMetricLabel">States affected</div>
                <div data-testid="stMetricValue">{states_affected}</div>
                <div data-testid="stMetricDelta"> {localties_affected} Locality</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

       # bottom long cart element 2
        st.markdown(f"""
        <div class="stMetric" style="width: 370px; height: 150px;"> <!-- Card size -->
            <div>
                <div data-testid="stMetricLabel">Explosions</div>
                <div data-testid="stMetricValue">{total_Explosions_Remote_violence}</div>
                <div data-testid="stMetricDelta">+40% MoM</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        # Card 3
        st.markdown(f"""
        <div class="stMetric" style="margin-bottom: 20px;"> <!-- Adds margin between cards -->
            <div class="icon-container">
            <!-- Time in Conflict Icon (Represents duration/hourglass) -->
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" fill="currentColor">
                <path d="M256 8C119 8 8 119 8 256s111 248 248 248 248-111 248-248S393 8 256 8zm0 448c-110.5 0-200-89.5-200-200S145.5 56 256 56s200 89.5 200 200-89.5 200-200 200zm61.8-104.4l-84.9-61.7c-3.1-2.3-4.9-5.9-4.9-9.7V116c0-6.6 5.4-12 12-12h32c6.6 0 12 5.4 12 12v141.7l66.8 48.6c5.4 3.9 6.5 11.4 2.6 16.8L334.6 349c-3.9 5.3-11.4 6.5-16.8 2.6z"/>
            </svg>
            </div>
            <div>
                <div data-testid="stMetricLabel">Time in Conflict</div>
                <div data-testid="stMetricValue">{days_difference} Days</div>
                <div data-testid="stMetricDelta">{hours_difference} Hours</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


       # bottom long cart element 3
        st.markdown(f"""
        <div class="stMetric" style="width: 300px; height: 150px;"> <!-- Card size -->
            <div>
                <div data-testid="stMetricLabel">Violence against civilians </div>
                <div data-testid="stMetricValue">{total_Violence_against_civilians}</div>
                <div data-testid="stMetricDelta">+40% MoM</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    # Side Card
    with col4:
        st.markdown("""
        <div class="stMetric" style="width: 230px; height: 315px;"> <!-- Card size -->
            <h3>Main Actors</h3>
            <p style="color:orange;font-size:24px;font-weight:bold;"><br></p>
            <p style="color:lightgreen;font-size:24px;font-weight:bold;"><br></p>
        </div>
        """, unsafe_allow_html=True)

    # Apply custom styling
    style_metric_cards()

# Run the Dashboard
dashboard()
# Add this at the end of your app.py file
if __name__ == "__main__":
    import os
    # Get port from environment variable (Cloud Run sets this)
    port = int(os.environ.get("PORT", 8080))
    
    # This is for local development - remove or comment out for Cloud Run
    # st.run()
