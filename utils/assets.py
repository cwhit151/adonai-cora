from __future__ import annotations

from pathlib import Path
from typing import Optional, Union

import streamlit as st

PathLike = Union[str, Path]

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}


def show_image_safely(path: Optional[PathLike], caption: str = "") -> None:
    """
    Safe Streamlit image display:
    - Only shows if file exists AND is a valid image
    - Otherwise shows a small caption instead of crashing
    """

    if not path:
        st.caption("No media attached.")
        return

    p = Path(str(path))

    # Missing file
    if not p.exists():
        st.caption("Media missing.")
        return

    # Folder instead of image
    if p.is_dir():
        st.caption("Media path is a folder (not an image).")
        return

    # Wrong extension
    if p.suffix.lower() not in IMAGE_EXTS:
        st.caption("Media is not an image file.")
        return

    # Safe preview
    try:
        st.image(str(p), use_container_width=True, caption=caption or None)
    except Exception:
        st.caption("Could not preview this image.")
