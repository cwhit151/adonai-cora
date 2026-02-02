import streamlit as st
import pandas as pd
from utils.db import run_query, execute_command
from utils.helpers import set_page_config
import os

set_page_config(page_title="Library")

st.title("📂 Media Library")

# Upload
with st.expander("Upload New Media"):
    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png', 'jpeg'])
    if uploaded_file is not None:
        # In a real app we'd save it. For demo, we just pretend.
        tags = st.text_input("Tags (comma separated)", "user_upload")
        if st.button("Save to Library"):
            # fake save
            fake_path = f"assets/sample_images/{uploaded_file.name}"
            execute_command(
                "INSERT INTO media_assets (media_path, source, tags) VALUES (?, 'manual', ?)",
                (fake_path, tags)
            )
            st.success(f"Saved {uploaded_file.name} to library!")
            st.rerun()

st.markdown("---")

# Gallery
assets = run_query("SELECT * FROM media_assets ORDER BY created_at DESC")

if not assets.empty:
    # Display in grid
    cols = st.columns(3)
    for idx, row in assets.iterrows():
        col = cols[idx % 3]
        with col:
            # Check if file exists properly (for demo avoid errors if missing)
            if os.path.exists(row['media_path']):
                st.image(row['media_path'], use_column_width=True)
            else:
                st.warning(f"File missing: {row['media_path']}")
            
            st.caption(f"ID: {row['id']} | {row['source']}")
            st.text(f"Tags: {row['tags']}")
            if st.button("Delete", key=f"del_{row['id']}"):
                execute_command("DELETE FROM media_assets WHERE id=?", (row['id'],))
                st.rerun()
else:
    st.info("No media assets found.")
