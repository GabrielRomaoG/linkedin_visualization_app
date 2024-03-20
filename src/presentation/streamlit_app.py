import streamlit as st
from st_pages import Page, show_pages


st.set_page_config(
    page_title="LinkedIn Data Visualization App",
    page_icon="src/presentation/assets/linkedin_icon.png",
)

col1, mid, col2 = st.columns([1, 1, 20])
with col1:
    st.image("src/presentation/assets/linkedin_icon.png", width=62)
with col2:
    st.write("# LinkedIn Data Visualization App")

show_pages(
    [
        Page("src/presentation/streamlit_app.py", "home", "🏠"),
        Page("src/presentation/streamlit_pages/connections.py", "Connections", "🧑‍💻"),
        Page("src/presentation/streamlit_pages/shares.py", "Shares", "🚩"),
    ]
)
