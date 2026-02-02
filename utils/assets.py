from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import streamlit as st

PathLike = Union[str, Path]

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

def show_image_safely(path: Optional[PathLike], *, caption: str = "") -> None:
    """
    Safe Streamlit image display:
    - Only displays if path exists AND is an image file
    - Otherwise shows a small warning instead of crashing
    """
    if not path:
        st.caption("No media attached.")
        return

    p = Path(str(path))

    # If it's a folder or doesn't exist, don't crash
    if not p.exists():
        st.caption("Media missing.")
        return
    if p.is_dir():
        st.caption("Media path is a folder (not an image).")
        return

    # Must be a known image extension
    if p.suffix.lower() not in IMAGE_EXTS:
        st.caption("Media is not an image file.")
        return

    # If PIL fails anyway, catch it
    try:
        st.image(str(p), use_container_width=True, caption=caption or None)
    except Exception:
        st.caption("Could not preview this image.")
