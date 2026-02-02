import streamlit as st

def set_page_config(page_title="CORA"):
    """Sets the page configuration for standard look and feel."""
    st.set_page_config(
        page_title=f"{page_title} | Adonai CORA",
        page_icon="☕️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        .stApp {
            background-color: #FAFAF9;
        }
        .main-header {
            font-family: 'Helvetica Neue', sans-serif;
            color: #4A3B32;
        }
        .metric-card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center;
        }
        .status-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.8em;
        }
        </style>
    """, unsafe_allow_html=True)

def status_color(status):
    """Returns a color code for a given status."""
    colors = {
        "Draft": "#E0E0E0",       # Grey
        "Approved": "#FFF3CD",    # Yellow/Orange
        "Scheduled": "#D1E7DD",   # Green
        "Posted": "#CFE2FF",      # Blue
        "Failed": "#F8D7DA"       # Red
    }
    return colors.get(status, "#FFFFFF")

def render_status_badge(status):
    """Renders a status badge in Streamlit."""
    color = status_color(status)
    text_color = "#000000"
    
    st.markdown(
        f'<span style="background-color: {color}; color: {text_color}; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: 600;">{status}</span>',
        unsafe_allow_html=True
    )
