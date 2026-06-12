import streamlit as st
import time
from graph.workflow import graph  # Standard import path for your compiled graph
import html
import json
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def format_score(score):
    if score is None:
        return "—", None

    try:
        value = float(score)
    except (TypeError, ValueError):
        return str(score), None

    display = f"{value:.0f}"

    return display, value
import re
from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet


def clean_pdf_text(text):

    if not text:
        return ""

    text = str(text)

    # Replace common symbols
    text = text.replace("✔", "[PASS]")
    text = text.replace("✓", "[PASS]")
    text = text.replace("✖", "[FAIL]")
    text = text.replace("✗", "[FAIL]")
    text = text.replace("→", "->")
    text = text.replace("•", "-")
    text = text.replace("📊", "[CHART]")
    text = text.replace("📈", "[TREND]")
    text = text.replace("📉", "[TREND]")
    text = text.replace("🔍", "[SEARCH]")
    text = text.replace("⚠️", "[WARNING]")
    text = text.replace("✅", "[SUCCESS]")

    # Remove unsupported unicode
    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    # Remove excessive spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def generate_pdf(report):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    elements = []

    # =====================================
    # TITLE
    # =====================================

    title = getattr(
        report,
        "title",
        "Deep Research Report"
    )

    elements.append(
        Paragraph(
            clean_pdf_text(title),
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 20)
    )

    # =====================================
    # EXECUTIVE SUMMARY
    # =====================================

    executive_summary = getattr(
        report,
        "executive_summary",
        ""
    )

    if executive_summary:

        elements.append(
            Paragraph(
                "Executive Summary",
                styles["Heading2"]
            )
        )

        elements.append(
            Spacer(1, 8)
        )

        for para in str(executive_summary).split("\n\n"):

            para = clean_pdf_text(para)

            if para.strip():

                elements.append(
                    Paragraph(
                        para,
                        styles["BodyText"]
                    )
                )

                elements.append(
                    Spacer(1, 6)
                )

        elements.append(
            Spacer(1, 12)
        )

    # =====================================
    # FULL REPORT
    # =====================================

    full_report = getattr(
        report,
        "report",
        ""
    )

    if full_report:

        elements.append(
            Paragraph(
                "Full Report",
                styles["Heading2"]
            )
        )

        elements.append(
            Spacer(1, 8)
        )

        report_text = str(full_report)

        for para in report_text.split("\n\n"):

            para = clean_pdf_text(para)

            if para.strip():

                elements.append(
                    Paragraph(
                        para,
                        styles["BodyText"]
                    )
                )

                elements.append(
                    Spacer(1, 6)
                )

    # =====================================
    # REFERENCES
    # =====================================

    references = getattr(
        report,
        "references",
        []
    )

    if references:

        elements.append(
            PageBreak()
        )

        elements.append(
            Paragraph(
                "References",
                styles["Heading2"]
            )
        )

        elements.append(
            Spacer(1, 10)
        )

        for idx, ref in enumerate(references, start=1):

            ref_text = clean_pdf_text(ref)

            elements.append(
                Paragraph(
                    f"{idx}. {ref_text}",
                    styles["BodyText"]
                )
            )

            elements.append(
                Spacer(1, 4)
            )

    doc.build(elements)

    buffer.seek(0)

    return buffer


# =====================================================================
# SECTION 1: PAGE SETUP & GLOBAL STYLES
# =====================================================================
def setup_page():
    st.set_page_config(
        page_title="Deep Research — Control Center",
        layout="wide",
        page_icon="🔬"
    )

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Reset & Base ── */
    *, *::before, *::after { box-sizing: border-box; }

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
        color: #1E293B;
    }

    [data-testid="stAppViewContainer"] {
        background: #F1F5F9;
    }
    [data-testid="stHeader"] {
        background: transparent;
        border-bottom: 1px solid #E2E8F0;
        backdrop-filter: blur(8px);
    }
    .main .block-container {
        padding: 2rem 2.5rem 4rem;
        max-width: 1280px;
    }

    /* ── Page Header ── */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.25rem 1.75rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .app-header-left {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .app-header-icon {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        flex-shrink: 0;
    }
    .app-header-title {
        font-size: 1.2rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.025em;
        line-height: 1.2;
    }
    .app-header-sub {
        font-size: 0.75rem;
        color: #94A3B8;
        margin-top: 0.1rem;
        letter-spacing: 0.01em;
    }
    .app-header-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-radius: 9999px;
        padding: 0.3rem 0.9rem;
        font-size: 0.72rem;
        font-weight: 600;
        color: #16A34A;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }
    .badge-dot {
        width: 6px; height: 6px;
        border-radius: 50%;
        background: #22C55E;
        animation: blink 2s ease-in-out infinite;
    }
    @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0.3} }

    /* ── Query Card ── */
    .query-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.5rem 1.75rem 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .card-eyebrow {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #2563EB;
        margin-bottom: 0.75rem;
    }

    /* ── Input ── */
    .stTextInput > label { display: none !important; }
    .stTextInput > div > div > input {
        background: #F8FAFC !important;
        border: 1.5px solid #CBD5E1 !important;
        border-radius: 10px !important;
        color: #0F172A !important;
        font-size: 0.95rem !important;
        padding: 0.7rem 1rem !important;
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    .stTextInput > div > div > input:focus {
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
        background: #FFFFFF !important;
    }
    .stTextInput > div > div > input::placeholder { color: #94A3B8 !important; }

    /* ── Button ── */
    .stButton > button {
        background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        padding: 0.65rem 1.5rem !important;
        box-shadow: 0 2px 8px rgba(37,99,235,0.25) !important;
        transition: transform 0.15s, box-shadow 0.15s !important;
    }
    .stButton > button:hover:not(:disabled) {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(37,99,235,0.35) !important;
    }
    .stButton > button:disabled {
        background: #E2E8F0 !important;
        color: #94A3B8 !important;
        box-shadow: none !important;
    }

    /* ── Section Panel ── */
    .panel {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.75rem 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .panel-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid #F1F5F9;
    }
    .panel-icon {
        width: 34px; height: 34px;
        border-radius: 8px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.95rem; flex-shrink: 0;
    }
    .panel-icon-blue  { background: #EFF6FF; }
    .panel-icon-green { background: #F0FDF4; }
    .panel-icon-amber { background: #FFFBEB; }
    .panel-title {
        font-size: 1rem;
        font-weight: 700;
        color: #0F172A;
        letter-spacing: -0.015em;
        line-height: 1;
    }
    .panel-subtitle {
        font-size: 0.73rem;
        color: #94A3B8;
        margin-top: 0.2rem;
    }

    /* ── Report Sections ── */
    .report-main-title {
        font-size: 1.65rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.03em;
        line-height: 1.3;
        margin-bottom: 0.25rem;
    }
    .report-section-block {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.25rem 1.5rem;
        margin-bottom: 1rem;
    }
    .report-section-block:last-child { margin-bottom: 0; }
    .report-block-label {
        font-size: 0.65rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #2563EB;
        margin-bottom: 0.6rem;
        display: flex; align-items: center; gap: 0.4rem;
    }
    .report-block-label::after {
        content: '';
        display: block;
        height: 1px;
        background: #DBEAFE;
        flex: 1;
    }
    .summary-text {
        color: #334155;
        font-size: 0.92rem;
        line-height: 1.75;
    }

    /* ── References ── */
    .ref-list { list-style: none; padding: 0; margin: 0; }
    .ref-item {
        display: flex; gap: 0.75rem;
        padding: 0.55rem 0;
        border-bottom: 1px solid #F1F5F9;
        font-size: 0.82rem; color: #475569;
        align-items: flex-start;
    }
    .ref-item:last-child { border-bottom: none; }
    .ref-num {
        min-width: 1.75rem; height: 1.75rem;
        background: #EFF6FF; border-radius: 5px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.7rem; font-weight: 700; color: #2563EB;
        flex-shrink: 0;
    }

    /* ── Quality Review ── */
    .score-tile-box {
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.1rem 1.25rem;
    }
    .score-big {
        font-size: 2.75rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -0.04em;
        line-height: 1;
    }
    .score-denom {
        font-size: 1rem;
        color: #94A3B8;
        font-weight: 500;
    }
    .score-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: #64748B;
        margin-top: 0.2rem;
    }
    .verdict-chip {
        display: inline-flex; align-items: center; gap: 0.35rem;
        padding: 0.3rem 0.9rem;
        border-radius: 9999px;
        font-size: 0.72rem; font-weight: 700;
        letter-spacing: 0.05em; text-transform: uppercase;
    }
    .verdict-pass { background: #F0FDF4; color: #16A34A; border: 1px solid #BBF7D0; }
    .verdict-fail { background: #FFF7ED; color: #C2410C; border: 1px solid #FED7AA; }
    .feedback-box {
        background: #FFFBEB;
        border: 1px solid #FDE68A;
        border-left: 3px solid #F59E0B;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        font-size: 0.88rem;
        color: #78350F;
        line-height: 1.7;
    }
    .feedback-box-pass {
        background: #F0FDF4;
        border: 1px solid #BBF7D0;
        border-left: 3px solid #22C55E;
        border-radius: 0 8px 8px 0;
        padding: 1rem 1.25rem;
        font-size: 0.88rem;
        color: #14532D;
        line-height: 1.7;
    }
    .passes-row {
        display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1rem;
    }
    .pass-chip {
        background: #F1F5F9; border: 1px solid #E2E8F0;
        border-radius: 7px; padding: 0.5rem 0.85rem;
        font-size: 0.78rem; color: #475569; font-weight: 500;
    }
    .pass-chip strong { color: #0F172A; }

    /* ── Execution Timeline ── */
    .timeline-wrap {
        position: relative;
        padding-left: 0;
    }
    .timeline-node {
        display: flex; gap: 1rem; align-items: flex-start;
        margin-bottom: 0;
        position: relative;
    }
    .timeline-left {
        display: flex; flex-direction: column; align-items: center;
        width: 32px; flex-shrink: 0;
    }
    .tl-dot {
        width: 32px; height: 32px;
        border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.75rem; font-weight: 700;
        flex-shrink: 0; z-index: 1; position: relative;
    }
    .tl-dot-done  { background: #DCFCE7; color: #16A34A; border: 2px solid #86EFAC; }
    .tl-dot-warn  { background: #FEF9C3; color: #A16207; border: 2px solid #FDE047; }
    .tl-dot-error { background: #FEE2E2; color: #DC2626; border: 2px solid #FCA5A5; }
    .tl-line {
        width: 2px; background: #E2E8F0; flex: 1;
        min-height: 20px; margin: 2px 0;
    }
    .tl-card {
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        flex: 1;
        margin-bottom: 0.75rem;
    }
    .tl-card-header {
        display: flex; align-items: center; justify-content: space-between;
        margin-bottom: 0.35rem;
    }
    .tl-node-name {
        font-size: 0.85rem; font-weight: 700; color: #0F172A;
        font-family: 'JetBrains Mono', monospace;
    }
    .tl-duration {
        font-size: 0.72rem; font-weight: 600;
        background: #EFF6FF; color: #2563EB;
        border-radius: 5px; padding: 0.15rem 0.5rem;
    }
    .tl-message {
        font-size: 0.8rem; color: #64748B; line-height: 1.5;
    }
    .tl-timestamp {
        font-size: 0.7rem; color: #94A3B8;
        font-family: 'JetBrains Mono', monospace;
        margin-top: 0.3rem;
    }

    /* ── Metrics row ── */
    .metrics-row {
        display: flex; gap: 1rem; margin-bottom: 1rem; flex-wrap: wrap;
    }
    .metric-tile {
        flex: 1; min-width: 160px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1rem 1.25rem;
    }
    .metric-tile-label {
        font-size: 0.65rem; font-weight: 700;
        letter-spacing: 0.09em; text-transform: uppercase;
        color: #94A3B8; margin-bottom: 0.3rem;
    }
    .metric-tile-value {
        font-size: 1.5rem; font-weight: 800;
        color: #0F172A; letter-spacing: -0.03em;
        font-variant-numeric: tabular-nums;
    }
    .metric-tile-unit {
        font-size: 0.75rem; font-weight: 500; color: #94A3B8; margin-left: 0.2rem;
    }

    /* ── Live log stream ── */
    .log-stream {
        background: #0F172A;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        font-family: 'JetBrains Mono', 'Courier New', monospace;
        font-size: 0.78rem;
        line-height: 1.8;
        color: #94A3B8;
        max-height: 280px;
        overflow-y: auto;
        margin-top: 0.75rem;
    }
    .log-ts   { color: #475569; }
    .log-node { color: #60A5FA; font-weight: 700; }
    .log-ok   { color: #4ADE80; }
    .log-warn { color: #FBBF24; }
    .log-info { color: #E2E8F0; }

    /* ── Status box ── */
    [data-testid="stStatus"] {
        background: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
    }

    /* ── Alerts ── */
    [data-testid="stAlert"] { border-radius: 10px !important; font-size: 0.87rem !important; }
    div[data-baseweb="notification"] { border-radius: 10px !important; }

    /* ── Streamlit metric overrides ── */
    [data-testid="stMetric"] {
        background: #F8FAFC !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 10px !important;
        padding: 1rem 1.25rem !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.65rem !important; font-weight: 700 !important;
        letter-spacing: 0.09em !important; text-transform: uppercase !important;
        color: #94A3B8 !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.4rem !important; font-weight: 800 !important;
        color: #0F172A !important; font-variant-numeric: tabular-nums !important;
    }

    /* ── JSON ── */
    .stJson { border-radius: 10px !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #F1F5F9; }
    ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #2563EB; }

    /* ── Divider ── */
    .soft-divider {
        border: none; border-top: 1px solid #F1F5F9; margin: 1.25rem 0;
    }

    /* FIX: Streamlit containers as cards */
    div[data-testid="stVerticalBlock"]:has(.panel-header) {
        background:#FFFFFF;
        border:1px solid #E2E8F0;
        border-radius:14px;
        padding:1.75rem 2rem;
        margin-bottom:1.5rem;
        box-shadow:0 1px 3px rgba(0,0,0,.05);
    }

    div[data-testid="stVerticalBlock"]:has(.card-eyebrow) {
        background:#FFFFFF;
        border:1px solid #E2E8F0;
        border-radius:14px;
        padding:1.5rem 1.75rem;
        margin-bottom:1.5rem;
        box-shadow:0 1px 3px rgba(0,0,0,.05);
    }
    ```css
.tl-card{
    background:#F8FAFC;
    border:1px solid #E2E8F0;
    border-radius:12px;
    padding:16px;
    margin-bottom:12px;
}

.tl-card-header{
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:8px;
}

.tl-node-name{
    font-weight:700;
    color:#0F172A;
}

.tl-duration{
    background:#EFF6FF;
    color:#2563EB;
    padding:4px 8px;
    border-radius:6px;
    font-size:12px;
    font-weight:600;
}
```

    </style>
    """, unsafe_allow_html=True)

    # ── App Header ────────────────────────────────────────────────────
    st.markdown("""
    <div class="app-header">
        <div class="app-header-left">
            <div class="app-header-icon">🔬</div>
            <div>
                <div class="app-header-title">Deep Research Control Center</div>
                <div class="app-header-sub">Multi-agent graph pipeline · State-synchronized monitoring</div>
            </div>
        </div>
        <div class="app-header-badge">
            <div class="badge-dot"></div> System Ready
        </div>
    </div>
    """, unsafe_allow_html=True)


# =====================================================================
# SECTION 2: SESSION STATE & QUERY INPUT PANEL
# =====================================================================
def init_session_state():
    if "research_results" not in st.session_state:
        st.session_state.research_results = None
    if "is_running" not in st.session_state:
        st.session_state.is_running = False
    if "timeline_events" not in st.session_state:
        st.session_state.timeline_events = []
    if "run_metrics" not in st.session_state:
        st.session_state.run_metrics = {}


def render_query_panel():
    st.markdown('<div class="card-eyebrow">🔍 Research Query</div>', unsafe_allow_html=True)

    col_input, col_btn = st.columns([5, 1], vertical_alignment="bottom")
    with col_input:
        query = st.text_input(
            label="query",
            label_visibility="collapsed",
            placeholder="e.g., What are the key LLM advancements in 2026?",
            disabled=st.session_state.is_running,
        )
    with col_btn:
        run_button = st.button(
            "▶  Run Research",
            disabled=st.session_state.is_running,
            use_container_width=True,
        )


    return query, run_button


# =====================================================================
# SECTION 3: RUNTIME EXECUTION
# =====================================================================
def run_pipeline(query):
    st.session_state.is_running = True
    st.session_state.research_results = None
    st.session_state.timeline_events = []
    st.session_state.run_metrics = {}

    # ── Live Execution Panel ─────────────────────────────────────
    st.markdown("""
    <div class="panel-header" style="margin-bottom:0.75rem">
        <div class="panel-icon panel-icon-amber">⚡</div>
        <div>
            <div class="panel-title">Live Execution Monitor</div>
            <div class="panel-subtitle">Real-time pipeline telemetry</div>
        </div>
    </div>""", unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1: time_ph = st.empty(); time_ph.metric("⏱ Elapsed", "0.00 s")
    with m2: node_ph = st.empty(); node_ph.metric("⚡ Nodes Run", "0")
    with m3: pass_ph = st.empty(); pass_ph.metric("🔁 Revision Passes", "0")

    active_ph = st.empty()

    with st.status("Initializing pipeline…", expanded=True) as status_box:
        log_ph = st.empty()
        live_logs = []
        timeline_events = []
        nodes_count = 0
        attempts_count = 0

        def log(node, msg, kind="info"):
            ts = time.strftime('%H:%M:%S')
            cls_map = {"ok": "log-ok", "warn": "log-warn", "info": "log-info"}
            icon_map = {"ok": "✔", "warn": "⚠", "info": "›"}
            cls  = cls_map.get(kind, "log-info")
            icon = icon_map.get(kind, "›")
            line = (
                f"<div>"
                f"<span class='log-ts'>{ts} </span>"
                f"<span class='log-node'>{node:<14}</span> "
                f"<span class='{cls}'>{icon} {msg}</span>"
                f"</div>"
            )
            live_logs.append(line)
            log_ph.markdown(
                f"<div class='log-stream'>{''.join(live_logs)}</div>",
                unsafe_allow_html=True,
            )

        start = time.time()
        node_t = time.time()
        log("planner", "Node entered — planning sub-routines initializing…")

        try:
            snap = {}

            for event in graph.stream({"query": query}, stream_mode="updates"):
                for node_name, state_updates in event.items():

                    dur = round(time.time() - node_t, 2)
                    log(node_name, f"Execution complete ({dur}s)", "ok")
                    nodes_count += 1
                    elapsed = round(time.time() - start, 2)

                    # store timeline event
                    tl_entry = {
                        "node": node_name,
                        "duration": dur,
                        "timestamp": time.strftime('%H:%M:%S'),
                        "messages": [f"Completed in {dur}s"],
                        "kind": "done",
                    }

                    time_ph.metric("⏱ Elapsed", f"{elapsed} s")
                    node_ph.metric("⚡ Nodes Run", str(nodes_count))
                    snap.update(state_updates)

                    if node_name == "writer":
                        attempts_count = snap.get("rewrite_attempts", 1)
                        pass_ph.metric("🔁 Revision Passes", str(attempts_count))
                        log("writer", f"Report draft complete — pass #{attempts_count}", "ok")
                        tl_entry["messages"].append(f"Draft pass #{attempts_count}")

                    elif node_name == "reviewer":
                        rev = snap.get("review")
                        if rev:
                            raw_score = getattr(rev, 'overall_score', None)
                            score_disp, _ = format_score(raw_score)
                            approved = getattr(rev, 'approved', False)
                            log("reviewer", f"Score: {score_disp}/100 | Approved: {approved}", "ok")
                            tl_entry["messages"].append(f"Score {score_disp}/100, approved={approved}")
                            if not approved:
                                fb = getattr(rev, 'feedback', '')
                                log("reviewer", f"Quality gate failed → re-routing to writer: {fb}", "warn")
                                tl_entry["messages"].append(f"Re-route: {fb}")
                                tl_entry["kind"] = "warn"

                    timeline_events.append(tl_entry)
                    node_t = time.time()
                    active_ph.info("Transitioning to next pipeline stage…")

            st.session_state.research_results = snap
            st.session_state.timeline_events  = timeline_events
            total = round(time.time() - start, 2)
            st.session_state.run_metrics = {
                "total_time": total,
                "nodes": nodes_count,
                "passes": attempts_count,
            }

            time_ph.metric("⏱ Total Runtime", f"{total} s")
            active_ph.empty()
            status_box.update(
                label=f"✅ Pipeline complete — {total}s · {nodes_count} nodes",
                state="complete", expanded=False,
            )

        except Exception as e:
            status_box.update(label="Pipeline execution failed", state="error")
            st.error(f"**Runtime error:** {e}")

    st.session_state.is_running = False


# =====================================================================
# SECTION 4: RESULTS — THREE MAIN PANELS
# =====================================================================
def render_results(page):
    if st.session_state.research_results is None:
        return

    snap      = st.session_state.research_results
    report    = snap.get("report")
    review    = snap.get("review")
    attempts  = snap.get("rewrite_attempts", 0)
    metrics   = st.session_state.run_metrics
    timeline  = st.session_state.timeline_events

    st.markdown("<div style='height:0.25rem'></div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    if page == "Research Report":
        # PANEL 1 — RESEARCH REPORT
        # ══════════════════════════════════════════════════════════════════
        st.markdown("""
        <div class="panel-header">
            <div class="panel-icon panel-icon-blue">📄</div>
            <div>
                <div class="panel-title">Research Report</div>
                <div class="panel-subtitle">AI-compiled intelligence output</div>
            </div>
        </div>""", unsafe_allow_html=True)
    
        if report:
            # Title
            title_text = getattr(report, 'title', 'Compiled Intelligence Report')
            st.markdown(f'<div class="report-main-title">{title_text}</div>', unsafe_allow_html=True)
            st.markdown("<div style='height:1.25rem'></div>", unsafe_allow_html=True)
    
            # ── Section: Executive Summary ───────────────────────────────
            st.markdown("""
            <div class="report-section-block">
                <div class="report-block-label">Executive Summary</div>""", unsafe_allow_html=True)
            st.markdown(
                f'<div class="summary-text">{getattr(report, "executive_summary", "No summary available.")}</div>',
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
    
            # ── Section: Full Report Body ────────────────────────────────
            st.markdown("""
            <div class="report-section-block">
                <div class="report-block-label">Full Report</div>""", unsafe_allow_html=True)
            body = getattr(report, 'report', None)
            if body:
                st.markdown(body)
            else:
                st.caption("No report body available.")
            st.markdown("</div>", unsafe_allow_html=True)
    
            # ── Section: Key Findings (if present) ───────────────────────
            findings = getattr(report, 'key_findings', None)
            if findings:
                st.markdown("""
                <div class="report-section-block">
                    <div class="report-block-label">Key Findings</div>""", unsafe_allow_html=True)
                if isinstance(findings, list):
                    for f in findings:
                        st.markdown(f"- {f}")
                else:
                    st.markdown(str(findings))
                st.markdown("</div>", unsafe_allow_html=True)
    
            # ── Section: Methodology (if present) ────────────────────────
            methodology = getattr(report, 'methodology', None)
            if methodology:
                st.markdown("""
                <div class="report-section-block">
                    <div class="report-block-label">Methodology</div>""", unsafe_allow_html=True)
                st.markdown(f'<div class="summary-text">{methodology}</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
    
            # ── Section: Conclusion (if present) ─────────────────────────
            conclusion = getattr(report, 'conclusion', None)
            if conclusion:
                st.markdown("""
                <div class="report-section-block">
                    <div class="report-block-label">Conclusion</div>""", unsafe_allow_html=True)
                st.markdown(f'<div class="summary-text">{conclusion}</div>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
    
            # ── Section: References ──────────────────────────────────────
            refs = getattr(report, 'references', [])
            st.markdown("""
            <div class="report-section-block">
                <div class="report-block-label">References & Sources</div>""", unsafe_allow_html=True)
            if refs:
                items_html = "".join(
                    f'<div class="ref-item"><span class="ref-num">{i+1}</span><span>{ref}</span></div>'
                    for i, ref in enumerate(refs)
                )
                st.markdown(items_html, unsafe_allow_html=True)
            else:
                st.caption("No citations recorded in the output schema.")
            st.markdown("</div>", unsafe_allow_html=True)
    
        else:
            st.error("No report object found in pipeline output.")
    
    
        # ══════════════════════════════════════════════════════════════════
    if page == "Quality Review":
        # PANEL 2 — QUALITY REVIEW & FEEDBACK
        # ══════════════════════════════════════════════════════════════════
        st.markdown("""
        <div class="panel-header">
            <div class="panel-icon panel-icon-green">🛡</div>
            <div>
                <div class="panel-title">Quality Review & Feedback</div>
                <div class="panel-subtitle">Automated evaluator verdict and critique</div>
            </div>
        </div>""", unsafe_allow_html=True)
    
        if review:
            # Be tolerant of different attribute names the review object might use
            raw_score = getattr(review, 'overall_score', None)
            if raw_score is None:
                raw_score = getattr(review, 'score', None)
            if raw_score is None:
                raw_score = getattr(review, 'rating', None)
    
            approved = getattr(review, 'approved', False)
            feedback = getattr(review, 'feedback', 'No feedback recorded.')
            criteria = getattr(review, 'criteria', None) or getattr(review, 'scores', None)
    
            # Score + verdict row
            verdict_class = "verdict-pass" if approved else "verdict-fail"
            verdict_label = "✓ Approved" if approved else "✗ Needs Revision"
            score_display, _ = format_score(raw_score)
    
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.markdown(f"""
                <div class="score-tile-box">
                    <div style="display:flex;align-items:baseline;gap:0.2rem">
                        <span class="score-big">{score_display}</span>
                        <span class="score-denom"> / 100
                        </span>
                    </div>
                    <div class="score-label">Overall Score</div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div class="score-tile-box">
                    <div class="score-label" style="margin-bottom:0.4rem">Final Verdict</div>
                    <span class="verdict-chip {verdict_class}">{verdict_label}</span>
                </div>""", unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div class="score-tile-box">
                    <div class="score-label" style="margin-bottom:0.4rem">Revision Passes</div>
                    <span style="font-size:1.4rem;font-weight:800;color:#0F172A">{attempts}</span>
                    <span style="font-size:0.75rem;color:#94A3B8;margin-left:0.2rem">loops</span>
                </div>""", unsafe_allow_html=True)
    
            # Feedback
            fb_class = "feedback-box-pass" if approved else "feedback-box"
            fb_icon  = "✅" if approved else "⚠️"
            st.markdown(f"""
            <div class="report-section-block">
                <div class="report-block-label">Critic Feedback</div>
                <div class="{fb_class}">{fb_icon} {feedback}</div>
            </div>""", unsafe_allow_html=True)
    
            # Detailed criteria (if present)
            criteria = getattr(review, 'criteria', None) or getattr(review, 'scores', None)
            if criteria:
                st.markdown("""
                <div class="report-section-block">
                    <div class="report-block-label">Evaluation Criteria Breakdown</div>""",
                    unsafe_allow_html=True,
                )
                if isinstance(criteria, dict):
                    cols = st.columns(len(criteria))
                    for i, (k, v) in enumerate(criteria.items()):
                        cols[i].metric(k.replace("_", " ").title(), f"{v}/100")
                else:
                    st.write(criteria)
                # st.markdown("</div>", unsafe_allow_html=True)
    
            # Suggestions (if present)
            suggestions = getattr(review, 'suggestions', None)
            if suggestions:
                st.markdown("""
                <div class="report-section-block">
                    <div class="report-block-label">Improvement Suggestions</div>""",
                    unsafe_allow_html=True,
                )
                if isinstance(suggestions, list):
                    for s in suggestions:
                        st.markdown(f"- {s}")
                else:
                    st.markdown(str(suggestions))
                st.markdown("</div>", unsafe_allow_html=True)
    
        else:
            st.info("No review object found in pipeline output.")
    
    
        # ══════════════════════════════════════════════════════════════════

    if page == "Execution Timeline":

        snap = st.session_state.get("research_results")
        metrics = st.session_state.get("run_metrics", {})
        timeline = st.session_state.get("timeline_events", [])

        if not snap:
            st.info("Run a research query first.")
            return

        # Header
        st.markdown("""
        <div class="panel-header">
            <div class="panel-icon panel-icon-amber">🕐</div>
            <div>
                <div class="panel-title">Execution Timeline & Diagnostics</div>
                <div class="panel-subtitle">
                    Node-by-node runtime breakdown and state snapshot
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ===========================
        # METRICS
        # ===========================

        if metrics:

            total_t = metrics.get("total_time", 0)
            n_nodes = metrics.get("nodes", 0)
            n_passes = metrics.get("passes", 0)
            avg_t = round(total_t / n_nodes, 2) if n_nodes else 0

            c1, c2, c3, c4 = st.columns(4)

            with c1:
                st.metric("Total Runtime", f"{total_t}s")

            with c2:
                st.metric("Nodes Executed", n_nodes)

            with c3:
                st.metric("Avg Node Time", f"{avg_t}s")

            with c4:
                st.metric("Revision Loops", n_passes)

        st.divider()

        # ===========================
        # TIMELINE
        # ===========================

        st.markdown(
            '<div class="report-block-label">Node Execution Flow</div>',
            unsafe_allow_html=True
        )

        if timeline:

            for ev in timeline:

                kind = ev.get("kind", "done")

                if kind == "done":
                    icon = "✅"
                elif kind == "warn":
                    icon = "⚠️"
                else:
                    icon = "❌"

                with st.container(border=True):

                    c1, c2 = st.columns([4,1])

                    with c1:
                        st.markdown(
                            f"### {icon} {ev.get('node','Unknown')}"
                        )

                    with c2:
                        st.metric(
                            "Duration",
                            f"{ev.get('duration',0)}s"
                        )

                    for msg in ev.get("messages", []):
                        st.write(msg)

                    st.caption(
                        f"@ {ev.get('timestamp','')}"
                    )

        else:
            st.caption("No timeline data available.")

            st.divider()

        # ===========================
        # RAW STATE
        # ===========================

        st.markdown(
            '<div class="report-block-label">Raw State Snapshot (JSON)</div>',
            unsafe_allow_html=True
        )

        st.json(snap, expanded=False)


    
    # =====================================================================
    # MAIN
    # =====================================================================
def main():
    setup_page()
    init_session_state()

    query, run_button = render_query_panel()

    if run_button:
        if query:
            run_pipeline(query)
        else:
            st.warning("Please enter a research query before running the pipeline.")
    st.markdown("""
<style>

/* Radio button text only */
div[role="radiogroup"] label span {
    color: white !important;
    font-weight: 700 !important;
}

/* Selected radio text */
div[role="radiogroup"] label:has(input:checked) span {
    color: white !important;
    font-weight: 800 !important;
}

</style>
""", unsafe_allow_html=True)
    page = st.sidebar.radio(
        "Navigation",
        ["Research Report", "Quality Review", "Execution Timeline"]
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📥 Export Report")
    if st.session_state.research_results:

        report = st.session_state.research_results.get("report")

        if report:

            # JSON DOWNLOAD
            json_report = {
                "title": getattr(report, "title", ""),
                "executive_summary": getattr(report, "executive_summary", ""),
                "report": getattr(report, "report", ""),
                "references": getattr(report, "references", [])
            }

            st.sidebar.download_button(
                label="📄 Download JSON",
                data=json.dumps(
                    json_report,
                    indent=4,
                    ensure_ascii=False
                ),
                file_name="research_report.json",
                mime="application/json",
                use_container_width=True
            )

            # PDF DOWNLOAD
            pdf_file = generate_pdf(report)

            st.sidebar.download_button(
                label="📕 Download PDF",
                data=pdf_file,
                file_name="research_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    render_results(page)

    


if __name__ == "__main__":
    main()