import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import time
from ACLED.elements.utils import fetch_acled_data
from streamlit.components.v1 import annotated_text
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from streamlit_gallery import apps, components
from streamlit_gallery.utils.page import page_group


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

# Title and Date Calculations
st.title("Echoes of Hope 🕊️")

# Calculate the difference in days and hours since April 13, 2023
start_date = date(2023, 4, 13)
current_date = date.today()
days_difference = (current_date - start_date).days
hours_difference = (current_date - start_date).total_seconds() / 3600

# Display days and hours with typing effect
from annotated_text import annotated_text

from annotated_text import annotated_text
import streamlit as st


# Annotate the message
annotated_text(
    "A war forgotten, and struggle lost to time \nbut as Bob Marley once said... ",
    ("“You just can't live that negative way. Make way for the positive day.”", "quote"),
    "\nEven amidst the chaos, ",
    ("hope", "noun"),
    " is our only anchor."
)

message = f"HOPE is our noun..."
typing_effect = st.empty()

for i in range(len(message) + 1):
    typing_effect.text(message[:i])
    time.sleep(0.05)  # Adjust the speed of the typing effect

st.divider()
st.subheader("The War's Impact")
# Display metrics
col1, col2, col3,col4 = st.columns(4)
col1.metric("Days Since War Started", f"{days_difference} days", f"{int(hours_difference)} hours", delta_color="off")
col2.metric("Total Fatalities", f"{total_fatalities}", f"{total_incidents} incidents", delta_color="off")
col3.metric("Total States affected", f"{states_affected}", f"{localties_affected} locality", delta_color="off")
col4.metric("Fatalities this month", f"{fatalities_latest_month}", f"{fatalities_percentage_change}% last month", delta_color="inverse")

st.divider()
# Display metrics
col1, col2, col3,col4 = st.columns(4)
col1.metric("Battles", f"{total_battles}")
col2.metric("Explosions/Remote violence", f"{total_Explosions_Remote_violence}")
col3.metric("Strategic developments", f"{total_Strategic_developments}")
col4.metric("Violence against civilians", f"{total_Violence_against_civilians}")


st.divider()
st.subheader("The War's Timeline numbers of Fatalities") 
# Create a Plotly figure
fig = go.Figure()

# Add a line plot to the figure
fig.add_trace(go.Scatter(
    x=monthly_fatalities['month_year'].astype(str),
    y=monthly_fatalities['fatalities'],
    mode='lines+markers',
    marker=dict(color='white'),  # Set marker color to white
    line=dict(color='white'),     # Set line color to white
))

# Update layout to remove grid lines and set background transparency
fig.update_layout(
    #title='Fatalities by Month-Year',
    #title_font_color='white',  # Set title color to white
    #xaxis_title='Month-Year',
    #yaxis_title='Fatalities',
    xaxis=dict(
        tickangle=0,
        tickfont=dict(color='white'),  # Set x-axis tick labels to white
        showgrid=False,  # Remove grid lines
        zeroline=False   # Remove the zero line
    ),
    yaxis=dict(
        tickfont=dict(color='white'),  # Set y-axis tick labels to white
        showgrid=False,  # Remove grid lines
        zeroline=False   # Remove the zero line
    ),
    plot_bgcolor='rgba(0, 0, 0, 0)',  # Transparent plot background
    paper_bgcolor='rgba(0, 0, 0, 0)'   # Transparent paper background
)

# Display the Plotly figure in Streamlit
st.plotly_chart(fig, use_container_width=True)