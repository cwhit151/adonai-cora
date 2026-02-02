import streamlit as st
import pandas as pd

from utils.db import run_query, execute_command
from utils.helpers import set_page_config
from utils.assets import show_image_safely

set_page_config(page_title="Library")

st.title("📁 Media Library")

# ----------------------------
# Upload (MVP demo behavior)
# ----------------------------
with st.expander("Upload New Media"):
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["png", "jpg", "jpeg", "webp", "gif"],
    )

    tags = st.text_input("Tags (comma separated)", value="", key="user_upload_tags")

    if uploaded_file is not None:
        st.info("MVP Demo: This currently stores a demo path (not the real uploaded file).")

        if st.button("Save to Library"):
            # Demo path (existing behavior)
            fake_path = f"assets/sample_images/{uploaded_file.name}"

            execute_command(
                "INSERT INTO media_assets (media_path, source, tags) VALUES (?, ?, ?)",
                (fake_path, "manual", tags),
            )

            st.success(f"Saved {uploaded_file.name} to library!")
            st.rerun()

st.divider()

# ----------------------------
# Gallery
# ----------------------------
assets = run_query("SELECT * FROM media_assets ORDER BY created_at DESC")

if assets is None or (isinstance(assets, pd.DataFrame) and assets.empty):
    st.info("No media assets found.")
else:
    # Ensure we have a DataFrame (depending on your db helper)
    if not isinstance(assets, pd.DataFrame):
        assets = pd.DataFrame(assets)

    cols = st.columns(3)

    for idx, row in assets.iterrows():
        col = cols[idx % 3]

        with col:
            show_image_safely(
                row.get("media_path"),
                caption=f"{row.get('source', 'source')} • {row.get('tags', '')}",
            )

            st.caption(f"ID: {row.get('id')}")

            if st.button("Delete", key=f"del_{row.get('id')}"):
                execute_command(
                    "DELETE FROM media_assets WHERE id=?",
                    (row.get("id"),),
                )
                st.rerun()
