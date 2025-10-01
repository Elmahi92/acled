import streamlit as st
import os

st.title("Test App")
st.write("Hello World!")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
