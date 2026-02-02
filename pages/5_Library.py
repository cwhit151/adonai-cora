import streamlit as st
import pandas as pd

from pathlib import Path
import uuid
from PIL import Image

from utils.db import run_query, execute_command
from utils.helpers import set_page_config

set_page_config(page_title="Library")

st.title("📁 Media Library")

UPLOAD_DIR = Path("assets/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

THUMB_SIZE = 250  # Instagram-style square thumb size

# ----------------------------
# Upload
# ----------------------------
with st.expander("Upload New Media"):
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=["png", "jpg", "jpeg", "webp", "gif"],
    )

    tags = st.text_input("Tags (comma separated)", value="", key="user_upload_tags")

    if uploaded_file is not None:
        # Small IG-style preview
        img = Image.open(uploaded_file)

        # crop to square
        w, h = img.size
        m = min(w, h)
        left = (w - m) // 2
        top = (h - m) // 2
        img = img.crop((left, top, left + m, top + m))

        # resize square preview
        img = img.resize((THUMB_SIZE, THUMB_SIZE))

        c1, c2, c3 = st.columns([1, 2, 1])
        with c2:
            st.image(img, caption="Preview", width=THUMB_SIZE)

        if st.button("Save to Library"):
            ext = Path(uploaded_file.name).suffix.lower()
            if ext not in [".png", ".jpg", ".jpeg", ".webp", ".gif"]:
                st.error("Unsupported file type.")
                st.stop()

            safe_name = f"{uuid.uuid4().hex}{ext}"
            save_path = UPLOAD_DIR / safe_name

            # reset pointer after PIL read
            uploaded_file.seek(0)
            save_path.write_bytes(uploaded_file.getbuffer())

            execute_command(
                "INSERT INTO media_assets (media_path, source, tags) VALUES (?, ?, ?)",
                (str(save_path), "upload", tags),
            )

            st.success("Saved to library!")
            st.rerun()

st.divider()

# ----------------------------
# Instagram Grid
# ----------------------------
st.subheader("📸 Library Grid")

assets = run_query("SELECT * FROM media_assets ORDER BY created_at DESC")

if assets is None or (isinstance(assets, pd.DataFrame) and assets.empty):
    st.info("No media assets found.")
    st.stop()

if not isinstance(assets, pd.DataFrame):
    assets = pd.DataFrame(assets)

cols = st.columns(3)

for idx, row in assets.iterrows():
    col = cols[idx % 3]

    with col:
        path = row.get("media_path")

        try:
            img = Image.open(path)

            # crop square center
            w, h = img.size
            m = min(w, h)
            left = (w - m) // 2
            top = (h - m) // 2
            img = img.crop((left, top, left + m, top + m))

            # resize to uniform thumb
            img = img.resize((THUMB_SIZE, THUMB_SIZE))

            st.image(img, width=THUMB_SIZE)

        except Exception:
            st.caption("⚠️ Could not preview")

        # tiny actions
        if st.button("Delete", key=f"del_{row.get('id')}"):
            execute_command("DELETE FROM media_assets WHERE id=?", (row.get("id"),))
            st.rerun()
