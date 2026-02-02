import streamlit as st
import pandas as pd
from datetime import datetime
from utils.db import run_query
from utils.helpers import set_page_config, render_status_badge

set_page_config(page_title="Calendar")

st.title("🗓️ Content Calendar")

# Filters
col1, col2 = st.columns(2)
with col1:
    filter_status = st.multiselect(
        "Filter by Status",
        ["Draft", "Approved", "Scheduled", "Posted", "Failed"],
        default=["Scheduled", "Posted", "Approved"]
    )
with col2:
    filter_platform = st.multiselect(
        "Filter by Platform",
        ["Instagram", "Facebook", "Both"],
        default=["Instagram", "Facebook", "Both"]
    )

# Build Query
query = "SELECT * FROM posts WHERE 1=1"
params = []

if filter_status:
    placeholders = ",".join("?" * len(filter_status))
    query += f" AND status IN ({placeholders})"
    params.extend(filter_status)

if filter_platform:
    placeholders = ",".join("?" * len(filter_platform))
    query += f" AND platform IN ({placeholders})"
    params.extend(filter_platform)

query += " ORDER BY scheduled_at ASC"

# Fetch Data
posts = run_query(query, tuple(params))

if not posts.empty:
    posts['scheduled_at'] = pd.to_datetime(posts['scheduled_at'])
    
    # Group by Date
    posts['date'] = posts['scheduled_at'].dt.date
    unique_dates = sorted(posts['date'].dropna().unique())
    
    for date_obj in unique_dates:
        st.subheader(date_obj.strftime("%A, %B %d, %Y"))
        
        day_posts = posts[posts['date'] == date_obj]
        
        for _, row in day_posts.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
                with c1:
                    st.text(row['scheduled_at'].strftime("%H:%M"))
                with c2:
                    st.markdown(f"**{row['title']}**")
                    if row['caption']:
                        st.caption(row['caption'][:60] + "...")
                with c3:
                    render_status_badge(row['status'])
                    st.caption(row['platform'])
                with c4:
                    if st.button("Edit", key=f"edit_{row['id']}"):
                        st.session_state['edit_post_id'] = row['id']
                        st.switch_page("pages/3_Post_Editor.py")
                st.divider()

    # unscheduled
    unscheduled = posts[posts['scheduled_at'].isna()]
    if not unscheduled.empty:
        st.subheader("Unscheduled / Drafts")
        for _, row in unscheduled.iterrows():
            with st.container():
                c1, c2, c3, c4 = st.columns([1, 4, 2, 2])
                with c1:
                    st.text("--:--")
                with c2:
                    st.markdown(f"**{row['title']}**")
                with c3:
                    render_status_badge(row['status'])
                with c4:
                     if st.button("Edit", key=f"edit_uns_{row['id']}"):
                        st.session_state['edit_post_id'] = row['id']
                        st.switch_page("pages/3_Post_Editor.py")
                st.divider()

else:
    st.info("No posts found matching filters.")
