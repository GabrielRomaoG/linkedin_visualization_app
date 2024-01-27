import streamlit as st


class StreamlitRunner:
    def run():
        st.set_page_config(
            page_title="LinkedIn Data Visualization App",
            page_icon="src/presentation/assets/linkedin_icon.png",
        )
        col1, mid, col2 = st.columns([1, 1, 20])
        with col1:
            st.image("src/presentation/assets/linkedin_icon.png", width=62)
        with col2:
            st.write("# LinkedIn Data Visualization App")
