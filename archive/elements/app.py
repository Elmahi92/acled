import json
import streamlit as st
from pathlib import Path
from streamlit import session_state as state
from streamlit_elements import elements, sync, event
from types import SimpleNamespace
from streamlit_elements import mui
from streamlit_extras.metric_cards import style_metric_cards
from dashboard import Dashboard, HeaderCard, Editor, KPI_Card, DataGrid, Radar, Pie, Player

width = 350
height = 300

def main():
    st.write("✨ Streamlit Elements Demo ✨")
    st.title("Responsive KPI Dashboard")

    if "w" not in state:
        board = Dashboard()

        # Define six KPI cards with placeholder content
        w = SimpleNamespace(
            dashboard=board,
            #def __init__(self, board, x, y, w, h, **item_props):
            card1=KPI_Card(board, 1, 1, 3, 4, minW=1, minH=1),
            card2=KPI_Card(board, 1, 0, 1, 1, minW=1, minH=1),
            card3=KPI_Card(board, 2, 0, 1, 1, minW=1, minH=1),
            card4=KPI_Card(board, 0, 1, 1, 1, minW=1, minH=1),
            card5=KPI_Card(board, 1, 1, 1, 1, minW=1, minH=1),
            card6=KPI_Card(board, 2, 1, 1, 1, minW=1, minH=1),
            radar=Radar(board, 12, 7, 3, 7, minW=2, minH=4),
            editor=Editor(board, 0, 0, 6, 11, minW=3, minH=3),
        )

        # Assign to state.w to persist
        state.w = w
        w.editor.add_tab("Radar chart", json.dumps(Radar.DEFAULT_DATA, indent=2), "json")

    else:
        w = state.w

    with elements("demo"):
        event.Hotkey("ctrl+s", sync(), bindInputs=True, overrideDefault=True)
        # Row 1
        w.card1(
            content="This is content for Card 1",
            title="KPI Title 1",
            subheader="Period: Q1 2024",
            value="15,000",
            trend="up",
            width=width,
            height=height,
            top="100px",          # Adjust this for vertical positioning within the Box
            left="50px",   
        )
        w.card2(
            content="This is content for Card 2",
            title="KPI Title 2",
            subheader="Period: Q1 2024",
            value="22,000",
            trend="down",
            width=width,
            height=height,
            top="100px",          # Adjust this for vertical positioning within the Box
            left="430px", 
        )
        w.card3(
            content="This is content for Card 2",
            title="KPI Title 2",
            subheader="Period: Q1 2024",
            value="22,000",
            trend="down",
            width=width,
            height=height,
            top="100px",          # Adjust this for vertical positioning within the Box
            left="810px", 
        )
        w.card4(
            content="This is content for Card 2DJWKBWJCHVWDHJCVWDHGCV",
            title="KPI Title 2",
            subheader="Period: Q1 2024",
            value="22,000",
            trend="down",
            width=1110,
            height=190,
            top="430px",          # Adjust this for vertical positioning within the Box
            left="50px", 
        )
        w.card5(
            content="This is content for Card 2",
            title="KPI Title 2",
            subheader="Period: Q1 2024",
            value="22,000",
            trend="down",
            width=300,
            height=520,
            top="100px",          # Adjust this for vertical positioning within the Box
            left="1200px", 
        )
        w.radar(w.editor.get_content("Radar chart"))
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    main()
