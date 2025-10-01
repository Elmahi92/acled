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
from utils import fetch_acled_data  # Commented out - replace with your actual data loading
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
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

# Get event type counts safely
event_counts = acled_data.groupby('event_type')['event_id_cnty'].count().reset_index()

def get_event_count(event_type):
    result = event_counts[event_counts['event_type'] == event_type]['event_id_cnty']
    return result.iloc[0] if len(result) > 0 else 0

total_battles = get_event_count("Battles")
total_Explosions_Remote_violence = get_event_count("Explosions/Remote violence")
total_Strategic_developments = get_event_count("Strategic developments")
total_Violence_against_civilians = get_event_count("Violence against civilians")

# Additional metrics
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
if fatalities_previous_month > 0:
    fatalities_percentage_change = ((fatalities_latest_month - fatalities_previous_month) / fatalities_previous_month) * 100
else:
    fatalities_percentage_change = 0
fatalities_percentage_change = round(fatalities_percentage_change, 2)

# Calculate the difference in days and hours since April 13, 2023
start_date = date(2023, 4, 13)
current_date = date.today()
days_difference = (current_date - start_date).days
hours_difference = (current_date - start_date).total_seconds() / 3600

# Streamlit App Layout
st.title(" 〰️ SUDAN ACLED Data Dashboard 〰️")
st.markdown("### Armed Conflict Location & Event Data Analysis Based on acled data")

# Sidebar for filters
# st.sidebar.header("Filters")
# selected_states = st.sidebar.multiselect(
#     "Select States",
#     options=acled_data['admin1'].unique(),
#     default=acled_data['admin1'].unique()[:3]
# )

# selected_event_types = st.sidebar.multiselect(
#     "Select Event Types",
#     options=acled_data['event_type'].unique(),
#     default=acled_data['event_type'].unique()
# )

# # Filter data based on selections
# filtered_data = acled_data[
#     (acled_data['admin1'].isin(selected_states)) &
#     (acled_data['event_type'].isin(selected_event_types))
# ]

# Key Metrics Section
st.markdown("### 📊 Key Metrics")

# Create metric cards using grid
metric_grid = grid(4, vertical_align="center")

with metric_grid.container():
    st.metric(
        label="Total Fatalities",
        value=f"{total_fatalities:,}",
        delta=f"{fatalities_percentage_change}% from last month"
    )

with metric_grid.container():
    st.metric(
        label="Total Incidents",
        value=f"{total_incidents:,}",
        delta=f"{days_difference} days since start"
    )

with metric_grid.container():
    st.metric(
        label="States Affected",
        value=f"{states_affected}",
        delta=f"{localties_affected} localities"
    )

with metric_grid.container():
    st.metric(
        label="Latest Month Fatalities",
        value=f"{fatalities_latest_month:,}",
        delta=f"{latest_month}"
    )

# Style the metric cards
style_metric_cards(
    background_color="#000000",
    border_left_color="#3A3A39",
    border_color="#162129",
    box_shadow="#F71938"
)

# Event Type Breakdown
st.markdown("### 🎯 Event Type Breakdown")
event_grid = grid(4, vertical_align="center")

with event_grid.container():
    st.metric("Battles", f"{total_battles:,}")

with event_grid.container():
    st.metric("Explosions/Remote Violence", f"{total_Explosions_Remote_violence:,}")

with event_grid.container():
    st.metric("Strategic Developments", f"{total_Strategic_developments:,}")

with event_grid.container():
    st.metric("Violence Against Civilians", f"{total_Violence_against_civilians:,}")

# Charts Section
st.markdown("### 📈 Trends")

# Create two columns for charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Monthly Fatalities Trend")
    # Convert period to string for plotting
    monthly_fatalities['month_year_str'] = monthly_fatalities['month_year'].astype(str)
    
    fig_line = px.line(
        monthly_fatalities,
        x='month_year_str',
        y='fatalities',
        title='Fatalities Over Time',
        markers=True
    )
    fig_line.update_layout(xaxis_title="Month", yaxis_title="Fatalities")
    st.plotly_chart(fig_line, use_container_width=True)

with col2:
    st.subheader("Events by Type")
    fig_pie = px.pie(
        event_counts,
        values='event_id_cnty',
        names='event_type',
        title='Distribution of Event Types'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Geographic Analysis
st.markdown("### 🗺️ Geographic Analysis")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Events by State")
    state_events = acled_data.groupby('admin1').size().reset_index(name='count')
    fig_bar = px.bar(
        state_events.head(10),
        x='admin1',
        y='count',
        title='Top 10 States by Number of Events'
    )
    fig_bar.update_layout(xaxis_title="State", yaxis_title="Number of Events")
    st.plotly_chart(fig_bar, use_container_width=True)

with col4:
    st.subheader("Fatalities by State")
    state_fatalities = acled_data.groupby('admin1')['fatalities'].sum().reset_index()
    fig_bar2 = px.bar(
        state_fatalities.head(10),
        x='admin1',
        y='fatalities',
        title='Top 10 States by Fatalities'
    )
    fig_bar2.update_layout(xaxis_title="State", yaxis_title="Fatalities")
    st.plotly_chart(fig_bar2, use_container_width=True)

# Data Table
st.markdown("### 📋 Recent Events")
st.subheader("Latest 100 Events")
recent_events = acled_data.sort_values('event_date', ascending=False).head(100)
st.dataframe(
    recent_events[['event_date', 'event_type', 'admin1', 'admin2', 'fatalities']],
    use_container_width=True
)

# Summary Statistics
st.markdown("### 📊 Summary Statistics")
summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.subheader("Fatalities Statistics")
    st.write(f"**Mean fatalities per event:** {acled_data['fatalities'].mean():.2f}")
    st.write(f"**Median fatalities per event:** {acled_data['fatalities'].median():.2f}")
    st.write(f"**Max fatalities in single event:** {acled_data['fatalities'].max()}")
    st.write(f"**Standard deviation:** {acled_data['fatalities'].std():.2f}")

with summary_col2:
    st.subheader("Time Period")
    st.write(f"**Data period:** {acled_data['event_date'].min().date()} to {acled_data['event_date'].max().date()}")
    st.write(f"**Days since tracking started:** {days_difference}")
    st.write(f"**Hours since tracking started:** {hours_difference:.0f}")
    st.write(f"**Latest month change:** {fatalities_percentage_change}%")

# Footer
st.markdown("---")
st.markdown("*Data source: Armed Conflict Location & Event Data Project (ACLED)*")
st.markdown(f"*Last updated: {current_date}*")
st.markdown(f"*Showing data for {len(acled_data)} events*")

# Add this at the end of your app.py file
if __name__ == "__main__":
    import os
    # Get port from environment variable (Cloud Run sets this)
    port = int(os.environ.get("PORT", 8080))
    
    # This is for local development - remove or comment out for Cloud Run
    # st.run()
