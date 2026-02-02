import streamlit as st

def set_page_config(**kwargs):
    """
    Safe wrapper around Streamlit's native set_page_config.
    Accepts any Streamlit config kwargs.
    """
    st.set_page_config(**kwargs)

def render_status_badge(status: str) -> str:
    """
    Returns a small HTML badge for post status.
    Use with: st.markdown(render_status_badge(status), unsafe_allow_html=True)
    """
    status = (status or "").strip().lower()

    styles = {
        "draft": ("#6b7280", "#111827"),
        "approved": ("#10b981", "#052e2b"),
        "scheduled": ("#3b82f6", "#0b1b3a"),
        "posted": ("#a855f7", "#240b3a"),
    }

    bg, text = styles.get(status, ("#6b7280", "#111827"))
    label = status.title() if status else "Unknown"

    return f"""
    <span style="
        display:inline-block;
        padding:4px 10px;
        border-radius:999px;
        font-size:12px;
        font-weight:600;
        background:{bg};
        color:white;
        letter-spacing:.2px;
    ">
        {label}
    </span>
    """
