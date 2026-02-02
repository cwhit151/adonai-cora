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
from pathlib import Path
import uuid

UPLOAD_DIR = Path("assets/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

with st.expander("Upload New Media"):
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["png", "jpg", "jpeg", "webp", "gif"],
    )

    tags = st.text_input("Tags (comma separated)", value="", key="user_upload_tags")

    if uploaded_file is not None:
        # Preview immediately (works even before saving)
        from PIL import Image

img = Image.open(uploaded_file)
img.thumbnail((300, 300))

c1, c2, c3 = st.columns([1, 2, 1])

with c2:
    st.image(img, caption="Preview", width=250)


        if st.button("Save to Library"):
            # Create a safe unique filename
            ext = Path(uploaded_file.name).suffix.lower()
            safe_name = f"{uuid.uuid4().hex}{ext}"
            save_path = UPLOAD_DIR / safe_name

            # Write bytes to disk
            save_path.write_bytes(uploaded_file.getbuffer())

            # Store REAL path in DB
            execute_command(
                "INSERT INTO media_assets (media_path, source, tags) VALUES (?, ?, ?)",
                (str(save_path), "upload", tags),
            )

            st.success("Saved to library!")
            st.rerun()

# ----------------------------
# Gallery
# ----------------------------
st.divider()
st.subheader("📸 Library Grid")

assets = run_query("SELECT * FROM media_assets ORDER BY created_at DESC")

if assets is None or (isinstance(assets, pd.DataFrame) and assets.empty):
    st.info("No media assets found.")
    st.stop()

if not isinstance(assets, pd.DataFrame):
    assets = pd.DataFrame(assets)

# --- Instagram-style grid ---
cols = st.columns(3)

THUMB_SIZE = 250  # Insta-like square size

for idx, row in assets.iterrows():
    col = cols[idx % 3]

    with col:
        path = row["media_path"]

        # Square thumbnail preview
        try:
            from PIL import Image

            img = Image.open(path)

            # Crop to square center
            w, h = img.size
            min_dim = min(w, h)

            left = (w - min_dim) // 2
            top = (h - min_dim) // 2
            right = left + min_dim
            bottom = top + min_dim

            img = img.crop((left, top, right, bottom))
            img = img.resize((THUMB_SIZE, THUMB_SIZE))

            st.image(img, use_container_width=False)

        except Exception:
            st.caption("⚠️ Could not preview")

        # Optional caption (small)
        st.caption(f"ID: {row['id']}")

        # Delete button
        if st.button("Delete", key=f"del_{row['id']}"):
            execute_command(
                "DELETE FROM media_assets WHERE id=?",
                (row["id"],)
            )
            st.rerun()
