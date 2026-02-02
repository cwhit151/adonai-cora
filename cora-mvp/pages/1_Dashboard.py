"""
import streamlit as st
from datetime import datetime, timedelta
from utils import helpers

def render():
    st.title("Dashboard")
    st.markdown("Plan and manage social content for Adonai Coffee — demo mode")

    # Stats cards
    col1, col2, col3, col4 = st.columns(4)
    stats = helpers.get_post_stats()
    col1.metric("Drafts", stats.get("Draft", 0))
    col2.metric("Approved", stats.get("Approved", 0))
    col3.metric("Scheduled", stats.get("Scheduled", 0))
    col4.metric("Posted", stats.get("Posted", 0))

    st.markdown("---")
    # Upcoming posts next 7 days
    st.subheader("Upcoming posts (next 7 days)")
    today = datetime.utcnow().date()
    upcoming = helpers.get_upcoming_posts(days=7)
    if not upcoming:
        st.info("No upcoming posts. Use 'Create / Edit Post' or 'AI Studio' to add content.")
    else:
        for p in upcoming:
            scheduled = p.scheduled_at.strftime("%Y-%m-%d %H:%M") if p.scheduled_at else "—"
            st.markdown(f"**{p.title}** • {p.platform} • {p.status} • {scheduled}")
            st.caption(p.caption[:160] + ("…" if len(p.caption or "") > 160 else ""))

    st.markdown("---")
    c1, c2 = st.columns(2)
    if c1.button("Create Post"):
        st.session_state["page"] = "Create / Edit Post"
        st.experimental_rerun()
    if c2.button("Generate AI Post"):
        st.session_state["page"] = "AI Studio"
        st.experimental_rerun()
"""
