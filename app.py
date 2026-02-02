# app.py
import streamlit as st
from utils.db import init_db
from utils.seed import seed_data
from utils.helpers import set_page_config

# Initialize DB and Seed Data on first load
init_db()
seed_data()

set_page_config(page_title="CORA", page_icon="☕", layout="wide")

st.markdown(
    """
    <style>
      .block-container { padding-top: 1.5rem; }
      [data-testid="stSidebar"] { padding-top: 0.75rem; }
      .cora-hero {
        padding: 1rem 1.25rem;
        border: 1px solid rgba(49, 51, 63, 0.15);
        border-radius: 14px;
        background: rgba(250, 250, 250, 0.6);
      }
      .cora-kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: .75rem; }
      @media (max-width: 1100px) { .cora-kpis { grid-template-columns: repeat(2, 1fr); } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="cora-hero">
      <div style="display:flex;align-items:center;gap:.75rem;">
        <div style="font-size:1.7rem;">☕</div>
        <div>
          <div style="font-size:1.25rem;font-weight:700;line-height:1.2;">CORA</div>
          <div style="opacity:.75;">Coffee Operations + Reporting Assistant</div>
        </div>
      </div>
      <div style="margin-top:.75rem;opacity:.85;">
        Select a page from the sidebar to get started.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
st.subheader("MVP Status")

st.markdown(
    """
- ✅ Database
- ✅ Seeded demo content
- ✅ Calendar / Post workflow pages
- ✅ AI Studio (demo)
- ✅ Media Library
"""
)
