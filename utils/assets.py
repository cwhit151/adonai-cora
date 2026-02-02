# utils/assets.py
from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple, Union
from PIL import Image, ImageDraw

PathLike = Union[str, Path]

def safe_image(
    path: Optional[PathLike],
    *,
    fallback_size: Tuple[int, int] = (1200, 675),
    label: str = "Image unavailable",
) -> Image.Image:
    """
    Returns a PIL Image.
    - If `path` exists and opens correctly -> returns the real image
    - Otherwise -> returns a generated placeholder image (no external assets needed)
    """
    if path:
        try:
            p = Path(path)
            if p.exists() and p.is_file():
                return Image.open(p)
        except Exception:
            pass

    # Generated fallback
    w, h = fallback_size
    img = Image.new("RGB", (w, h), (245, 245, 245))
    draw = ImageDraw.Draw(img)

    # Simple centered label (no font dependency)
    text = label
    bbox = draw.textbbox((0, 0), text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((w - tw) / 2, (h - th) / 2), text, fill=(120, 120, 120))

    return img
