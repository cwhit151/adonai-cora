from datetime import datetime, date, time

import pandas as pd
import streamlit as st

from utils.db import run_query, execute_command
from utils.helpers import set_page_config

set_page_config(page_title="Post Editor")

st.title("✍️ Post Editor")

# ----------------------------
# Load posts for selection
# ----------------------------
posts = run_query("SELECT * FROM posts ORDER BY created_at DESC")

if posts is None or (isinstance(posts, pd.DataFrame) and posts.empty):
    st.info("No posts found. Create one below.")
    selected_id = None
else:
    if not isinstance(posts, pd.DataFrame):
        posts = pd.DataFrame(posts)

    # Build selector labels
    posts["label"] = posts["title"].fillna("Untitled") + " (" + posts["status"].fillna("draft") + ")"
    selected_label = st.selectbox("Select a post to edit", options=["Create New"] + posts["label"].tolist())

    if selected_label == "Create New":
        selected_id = None
    else:
        selected_id = int(posts.loc[posts["label"] == selected_label, "id"].iloc[0])

# Clear selection button
if st.button("Clear Selection (Create New)"):
    selected_id = None
    st.rerun()

# ----------------------------
# Load selected post data
# ----------------------------
post_data = None
if selected_id is not None:
    df = run_query("SELECT * FROM posts WHERE id = ?", (selected_id,))
    if isinstance(df, pd.DataFrame) and not df.empty:
        post_data = df.iloc[0]

# Defaults
default_title = "" if post_data is None else (post_data.get("title") or "")
default_platform = "Instagram" if post_data is None else (post_data.get("platform") or "Instagram")
default_status = "Draft" if post_data is None else (post_data.get("status") or "Draft")

# scheduled_at can be null/empty
if post_data is None or pd.isna(post_data.get("scheduled_at")):
    default_date = date.today()
    default_time = time(12, 0)
else:
    dt = pd.to_datetime(post_data.get("scheduled_at"))
    default_date = dt.date()
    default_time = dt.time().replace(second=0, microsecond=0)

default_caption = "" if post_data is None else (post_data.get("caption") or "")
default_hashtags = "" if post_data is None else (post_data.get("hashtags") or "")
default_media_path = "" if post_data is None else (post_data.get("media_path") or "")

st.caption(f"{'Editing Post ID: ' + str(selected_id) if selected_id else 'Creating New Post'}")

# ----------------------------
# Form (must include submit button)
# ----------------------------
with st.form("post_editor_form"):
    title = st.text_input("Internal Title", value=default_title)

    c1, c2 = st.columns(2)
    with c1:
        platform = st.selectbox("Platform", ["Instagram", "Facebook", "LinkedIn"], index=["Instagram", "Facebook", "LinkedIn"].index(default_platform) if default_platform in ["Instagram", "Facebook", "LinkedIn"] else 0)

    with c2:
        status = st.selectbox("Status", ["Draft", "Approved", "Scheduled", "Posted"], index=["Draft", "Approved", "Scheduled", "Posted"].index(default_status.title()) if isinstance(default_status, str) else 0)

    scheduled_date = st.date_input("Scheduled Date", value=default_date)
    scheduled_time = st.time_input("Scheduled Time", value=default_time)

    caption = st.text_area("Caption", value=default_caption, height=140)
    hashtags = st.text_input("Hashtags", value=default_hashtags)
    media_path = st.text_input("Media Path (Manual for MVP)", value=default_media_path, placeholder="assets/sample_images/latte.png")

    submitted = st.form_submit_button("Save Post")

# ----------------------------
# Save logic
# ----------------------------
if submitted:
    if not title.strip():
        st.error("Title is required.")
    else:
        scheduled_at = datetime.combine(scheduled_date, scheduled_time).isoformat()

        if selected_id is None:
            execute_command(
                """
                INSERT INTO posts (title, platform, status, scheduled_at, caption, hashtags, media_path)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (title, platform, status.lower(), scheduled_at, caption, hashtags, media_path),
            )
            st.success("Post created!")
        else:
            execute_command(
                """
                UPDATE posts
                SET title=?, platform=?, status=?, scheduled_at=?, caption=?, hashtags=?, media_path=?
                WHERE id=?
                """,
                (title, platform, status.lower(), scheduled_at, caption, hashtags, media_path, selected_id),
            )
            st.success("Post updated!")

        st.rerun()
