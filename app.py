import streamlit as st

# -------------------------------
# Page Config (must be first)
# -------------------------------
st.set_page_config(
    page_title="CORA",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Styling
# -----------------------------
st.markdown(
    """
<style>
/* Tighten page spacing */
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1200px; }

/* Card style */
.card {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.10);
  border-radius: 16px;
  padding: 16px 18px;
}

/* Subtle label */
.muted { color: rgba(255,255,255,0.65); font-size: 0.95rem; }

/* Big header */
.hero-title { font-size: 2.1rem; font-weight: 700; margin: 0; }
.hero-sub { font-size: 1.05rem; color: rgba(255,255,255,0.75); margin-top: 0.25rem; }

/* KPI */
.kpi { font-size: 1.7rem; font-weight: 700; }
.kpi-label { color: rgba(255,255,255,0.65); font-size: 0.9rem; }

/* Divider */
.hr { height: 1px; background: rgba(255,255,255,0.08); margin: 10px 0 14px 0; }

/* Small badge */
.badge {
  display: inline-block;
  padding: 4px 10px;
  border-radius: 999px;
  background: rgba(34,197,94,0.12);
  border: 1px solid rgba(34,197,94,0.25);
  color: rgba(34,197,94,1);
  font-size: 0.85rem;
  margin-left: 8px;
}
</style>
""",
    unsafe_allow_html=True,
)

# -----------------------------
# Helpers
# -----------------------------
def page_link_safe(label: str, page: str, icon: str = ""):
    """Use st.page_link when available; otherwise show a hint."""
    try:
        st.page_link(page, label=f"{icon} {label}".strip())
    except Exception:
        st.caption(f"{icon} Go to: {label} (page: {page})")

# -----------------------------
# Layout
# -----------------------------
left, right = st.columns([1, 2.2], gap="large")

with left:
    st.markdown("### ☕ CORA")
    st.markdown(
        '<div class="muted">Coffee Operations + Reporting Assistant</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    st.markdown("#### Quick Actions")
    a, b = st.columns(2)
    with a:
        page_link_safe("AI Studio", "pages/4_AI_Studio.py", "✨")
        page_link_safe("Post Editor", "pages/3_Post_Editor.py", "✍️")
    with b:
        page_link_safe("Calendar", "pages/2_Calendar.py", "🗓️")
        page_link_safe("Library", "pages/5_Library.py", "🗂️")

    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown("#### MVP Status")
    st.markdown(
        """
        <div class="card">
          <div><b>System Health</b> <span class="badge">LIVE</span></div>
          <div style="margin-top:10px" class="muted">
            ✅ Database connected<br/>
            ✅ Seeded demo content<br/>
            ✅ AI Studio demo flows<br/>
            ✅ Media library uploads<br/>
            ✅ Post workflow pages
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with right:
    st.markdown('<p class="hero-title">Welcome to CORA</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="hero-sub">Create content, schedule posts, and manage media — all in one clean demo workflow.</p>',
        unsafe_allow_html=True,
    )

    st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

    # KPIs (demo-friendly placeholders)
    k1, k2, k3, k4 = st.columns(4, gap="medium")
    with k1:
        st.markdown(
            "<div class='card'><div class='kpi'>12</div><div class='kpi-label'>Drafts</div></div>",
            unsafe_allow_html=True,
        )
    with k2:
        st.markdown(
            "<div class='card'><div class='kpi'>6</div><div class='kpi-label'>Scheduled</div></div>",
            unsafe_allow_html=True,
        )
    with k3:
        st.markdown(
            "<div class='card'><div class='kpi'>3</div><div class='kpi-label'>Approved</div></div>",
            unsafe_allow_html=True,
        )
    with k4:
        st.markdown(
            "<div class='card'><div class='kpi'>18</div><div class='kpi-label'>Media Assets</div></div>",
            unsafe_allow_html=True,
        )

    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown("### How the demo works")
    st.markdown(
        """
        <div class="card">
          <b>1) Generate</b> in <i>AI Studio</i> → creates a Draft post<br/>
          <b>2) Edit</b> in <i>Post Editor</i> → caption, hashtags, status, schedule time<br/>
          <b>3) Attach media</b> from <i>Library</i> → choose or upload images<br/>
          <b>4) Review schedule</b> in <i>Calendar</i> → see what’s coming up
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br/>", unsafe_allow_html=True)

    st.markdown("### Demo checklist")
    c1, c2 = st.columns(2, gap="medium")
    with c1:
        st.markdown(
            """
            <div class="card">
              <b>Try this:</b><br/>
              • Generate a draft in AI Studio<br/>
              • Click “Go to Post Editor”<br/>
              • Set status → Scheduled<br/>
              • Add a time + date
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="card">
              <b>Then:</b><br/>
              • Upload an image in Library<br/>
              • Confirm it displays as a square tile<br/>
              • (Optional) attach it to a post
            </div>
            """,
            unsafe_allow_html=True,
        )
