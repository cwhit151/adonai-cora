import streamlit as st
import pandas as pd
from utils.db import run_query
from utils.helpers import set_page_config, render_status_badge

set_page_config(page_title="Dashboard")

st.title("Dashboard")

# Fetch Stats
posts = run_query("SELECT status FROM posts")
if not posts.empty:
    counts = posts['status'].value_counts()
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Drafts", counts.get("Draft", 0))
    with col2:
        st.metric("Approved", counts.get("Approved", 0))
    with col3:
        st.metric("Scheduled", counts.get("Scheduled", 0))
    with col4:
        st.metric("Posted", counts.get("Posted", 0))

st.markdown("---")

# Quick Actions
col1, col2 = st.columns(2)
with col1:
    if st.button("➕ Create Manual Post", use_container_width=True):
        st.switch_page("pages/3_Post_Editor.py")
with col2:
    if st.button("✨ Generate AI Draft", use_container_width=True):
        st.switch_page("pages/4_AI_Studio.py")

st.markdown("### Upcoming Posts (Next 7 Days)")

# Get upcoming posts
upcoming_query = """
    SELECT id, title, platform, scheduled_at, status 
    FROM posts 
    WHERE status IN ('Scheduled', 'Approved') 
    AND scheduled_at >= datetime('now')
    ORDER BY scheduled_at ASC
    LIMIT 5
"""
upcoming = run_query(upcoming_query)

if not upcoming.empty:
    for _, row in upcoming.iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
            with col1:
                st.markdown(f"**{row['title']}**")
            with col2:
                st.caption(f"{row['platform']}")
            with col3:
                st.text(row['scheduled_at'][:16] if row['scheduled_at'] else "No Date")
            with col4:
                render_status_badge(row['status'])
            st.divider()
else:
    st.info("No upcoming posts scheduled.")
