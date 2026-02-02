import streamlit as st

def set_page_config(**kwargs):
    """
    Safe wrapper around Streamlit's native set_page_config.

    Allows passing any valid Streamlit config options like:
    - page_title
    - page_icon
    - layout
    - initial_sidebar_state
    """
    st.set_page_config(**kwargs)
