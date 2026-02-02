import streamlit as st
from datetime import datetime
from utils.db import run_query, execute_command
from utils.helpers import set_page_config

set_page_config(page_title="Post Editor")

st.title("✍️ Post Editor")

# Check if editing existing post
post_id = st.session_state.get('edit_post_id', None)
post_data = None

if post_id:
    df = run_query("SELECT * FROM posts WHERE id = ?", (post_id,))
    if not df.empty:
        post_data = df.iloc[0]
        st.info(f"Editing Post: {post_data['title']}")
        if st.button("Clear Selection (Create New)"):
            del st.session_state['edit_post_id']
            st.rerun()

# Form Inputs
with st.form("post_form"):
    title = st.text_input("Internal Title", value=post_data['title'] if post_data is not None else "")
    
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox(
            "Platform", 
            ["Instagram", "Facebook", "Both"], 
            index=["Instagram", "Facebook", "Both"].index(post_data['platform']) if post_data is not None else 0
        )
    with col2:
        status = st.selectbox(
            "Status", 
            ["Draft", "Approved", "Scheduled", "Posted", "Failed"],
            index=["Draft", "Approved", "Scheduled", "Posted", "Failed"].index(post_data['status']) if post_data is not None else 0
        )

    scheduled_at = st.date_input("Scheduled Date", value=datetime.today() if post_data is None or pd.isna(post_data['scheduled_at']) else pd.to_datetime(post_data['scheduled_at']))
    scheduled_time = st.time_input("Scheduled Time", value=datetime.now().time() if post_data is None or pd.isna(post_data['scheduled_at']) else pd.to_datetime(post_data['scheduled_at']).time())

    caption = st.text_area("Caption", height=150, value=post_data['caption'] if post_data is not None else "")
    hashtags = st.text_input("Hashtags", value=post_data['hashtags'] if post_data is not None else "")
    
    # Media (Simplified for MVP)
    media_path = st.text_input("Media Path (Manual for MVP)", value=post_data['media_path'] if post_data is not None and post_data['media_path'] else "assets/sample_images/")

    submitted = st.form_submit_button("Save Post")

    if submitted:
        # Validation
        if not title:
            st.error("Title is required.")
        elif status == "Scheduled" and not scheduled_at:
             st.error("Scheduled posts must have a date.")
        else:
            final_schedule = f"{scheduled_at} {scheduled_time}"
            
            if post_id:
                # Update
                execute_command('''
                    UPDATE posts 
                    SET title=?, platform=?, scheduled_at=?, caption=?, hashtags=?, media_path=?, status=?, updated_at=CURRENT_TIMESTAMP
                    WHERE id=?
                ''', (title, platform, final_schedule, caption, hashtags, media_path, status, post_id))
                st.success("Post updated successfully!")
            else:
                # Create
                execute_command('''
                    INSERT INTO posts (title, platform, scheduled_at, caption, hashtags, media_path, status)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (title, platform, final_schedule, caption, hashtags, media_path, status))
                st.success("Post created successfully!")
                
            # Clear state
            if 'edit_post_id' in st.session_state:
                del st.session_state['edit_post_id']

# Delete Option
if post_id:
    st.divider()
    if st.button("🗑️ Delete Post", type="primary"):
        execute_command("DELETE FROM posts WHERE id=?", (post_id,))
        del st.session_state['edit_post_id']
        st.warning("Post deleted.")
        st.rerun()
