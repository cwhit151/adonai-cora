import streamlit as st
from utils.db import init_db
from utils.seed import seed_data
from utils.helpers import set_page_config

# Initialize DB and Seed Data on first load
init_db()
seed_data()

set_page_config(page_title="Home")

st.title("☕️ Welcome to CORA")
st.markdown("### Coffee Operations + Reporting Assistant")

st.info("👈 Select a page from the sidebar to get started.")

st.markdown("""
---
**Project Status:** MVP Demo
- ✅ Database connected (SQLite)
- ✅ AI placeholder ready
- ✅ Marketing calendar active

*Built for Adonai Coffee.*
""")
