# ╔══════════════════════════════════════════════════════════════════════╗
# ║        APLIKASI PRAKTIKUM KIMIA ORGANIK — STREAMLIT APP             ║
# ║  pip install streamlit pandas                                        ║
# ║  streamlit run kimia_organik_app.py                                  ║
# ╚══════════════════════════════════════════════════════════════════════╝

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Praktikum Kimia Organik",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────
# SESSION STATE — simpan percobaan aktif
# ─────────────────────────────────────────────────────────────────────
if "active_exp" not in st.session_state:
    st.session_state.active_exp = 0

# ─────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #06080f;
    color: #e2e8f0;
}
.block-container { padding: 0 2rem 3rem 2rem !important; max-width: 1400px; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="collapsedControl"] { display: none; }

/* ── TOP NAV BAR ── */
.topbar {
    position: sticky; top: 0; z-index: 999;
    background: rgba(6,8,15,.92);
    backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(56,189,248,.15);
    padding: .6rem 0;
    margin: 0 -2rem 1.5rem -2rem;
    display: flex; align-items: center; gap: 0;
}
.topbar-logo {
    padding: 0 1.5rem 0 2rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .85rem; font-weight: 700; color: #38bdf8;
    white-space: nowrap; border-right: 1px solid rgba(56,189,248,.15);
    display: flex; align-items: center; gap: .5rem;
}
.topbar-nav { display: flex; align-items: center; padding: 0 1rem; gap: .35rem; flex-wrap: wrap; }
.topbar-sep { flex: 1; }
.topbar-info {
    padding: 0 2rem; font-family: 'JetBrains Mono', monospace;
    font-size: .68rem; color: #334155; white-space: nowrap;
}

/* ── EXP NAV PILLS (in-page, big) ── */
.exp-nav-wrap {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: .65rem;
    margin-bottom: 1.75rem;
    background: #0d1117;
    border: 1px solid rgba(56,189,248,.12);
    border-radius: 18px;
    padding: .85rem;
}
.exp-pill {
    border-radius: 12px; padding: .75rem .5rem;
    text-align: center; cursor: pointer;
    border: 1px solid rgba(56,189,248,.12);
    background: rgba(255,255,255,.02);
    transition: all .22s ease;
    user-select: none;
}
.exp-pill:hover {
    border-color: rgba(56,189,248,.4);
    background: rgba(56,189,248,.06);
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(56,189,248,.1);
}
.exp-pill.active {
    border-color: #38bdf8;
    background: linear-gradient(135deg, rgba(56,189,248,.15), rgba(129,140,248,.10));
    box-shadow: 0 0 24px rgba(56,189,248,.18);
    transform: translateY(-2px);
}
.exp-pill-icon { font-size: 1.6rem; display: block; margin-bottom: .3rem; }
.exp-pill-num  {
    font-family: 'JetBrains Mono', monospace; font-size: .62rem;
    font-weight: 700; color: #38bdf8; letter-spacing: .1em;
    text-transform: uppercase; margin-bottom: .2rem;
}
.exp-pill-name {
    font-size: .72rem; font-weight: 600; color: #94a3b8;
    line-height: 1.3;
}
.exp-pill.active .exp-pill-name { color: #e2e8f0; }
.exp-pill.active .exp-pill-num  { color: #7dd3fc; }

/* ── QUICK-JUMP BREADCRUMB ── */
.breadcrumb {
    display: flex; align-items: center; gap: .5rem;
    font-family: 'JetBrains Mono', monospace; font-size: .72rem;
    color: #334155; margin-bottom: 1.25rem; flex-wrap: wrap;
}
.breadcrumb-sep { color: #1e293b; }
.breadcrumb-cur { color: #38bdf8; font-weight: 700; }

/* ── HERO ── */
.hero-box {
    background: linear-gradient(135deg, #0d1117 0%, #141b26 60%, #0d1b2a 100%);
    border: 1px solid rgba(56,189,248,.2); border-radius: 20px;
    padding: 1.75rem 2.25rem; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.hero-box::before {
    content: ''; position: absolute; inset: 0;
    background: radial-gradient(circle at 10% 50%, rgba(56,189,248,.08) 0%, transparent 50%),
                radial-gradient(circle at 90% 20%, rgba(129,140,248,.06) 0%, transparent 50%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace; font-size: .7rem;
    color: #38bdf8; letter-spacing: .12em; text-transform: uppercase; margin-bottom: .5rem;
}
.hero-title {
    font-size: 1.9rem; font-weight: 700; line-height: 1.15;
    background: linear-gradient(135deg, #e2e8f0, #38bdf8, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub { font-family: 'JetBrains Mono', monospace; font-size: .75rem; color: #64748b; margin-top: .35rem; }
.chip-row { display: flex; flex-wrap: wrap; gap: .35rem; margin-top: .8rem; }
.chip {
    padding: .2rem .65rem; border-radius: 9999px; font-size: .68rem;
    font-weight: 600; font-family: 'JetBrains Mono', monospace;
    background: rgba(56,189,248,.08); border: 1px solid rgba(56,189,248,.25); color: #38bdf8;
}

/* ── METRICS ── */
.metric-row { display: grid; grid-template-columns: repeat(4,1fr); gap: .8rem; margin-bottom: 1.5rem; }
.metric-card {
    background: #0d1117; border: 1px solid rgba(56,189,248,.15);
    border-radius: 14px; padding: 1rem; text-align: center;
    transition: border-color .25s, box-shadow .25s;
}
.metric-card:hover { border-color: rgba(56,189,248,.4); box-shadow: 0 0 18px rgba(56,189,248,.08); }
.metric-val { font-size: 1.8rem; font-weight: 700; color: #38bdf8; font-family: 'JetBrains Mono', monospace; }
.metric-lbl { font-size: .66rem; color: #64748b; text-transform: uppercase; letter-spacing: .06em; margin-top: .18rem; }

/* ── SECTION HEAD ── */
.sec-head {
    font-family: 'JetBrains Mono', monospace; font-size: .78rem; font-weight: 700; color: #38bdf8;
    border-left: 3px solid #38bdf8; padding-left: .75rem; margin: 1.2rem 0 .8rem 0;
}

/* ── MOLECULE CARD ── */
.mol-card {
    background: #0d1117; border: 1px solid rgba(56,189,248,.15);
    border-radius: 14px; padding: 1.1rem; transition: all .25s; margin-bottom: .75rem;
}
.mol-card:hover { border-color: rgba(56,189,248,.4); transform: translateY(-2px); }
.mol-name { font-weight: 700; font-size: .88rem; color: #e2e8f0; margin-bottom: .55rem; }
.mol-svg-wrap { background: #f8fafc; border-radius: 10px; padding: .65rem; text-align: center; margin-bottom: .55rem; min-height: 80px; display:flex; align-items:center; justify-content:center; }
.mol-badge {
    display: inline-block; padding: .18rem .55rem; border-radius: 9999px;
    font-size: .66rem; font-weight: 600; font-family: 'JetBrains Mono', monospace;
    background: rgba(56,189,248,.1); border: 1px solid rgba(56,189,248,.25); color: #38bdf8; margin: .12rem;
}
.mol-iupac { font-size: .7rem; color: #818cf8; font-style: italic; margin-top: .35rem; }

/* ── REACTION CARD ── */
.rxn-card {
    border-radius: 11px; padding: .85rem 1rem; margin-bottom: .5rem;
    border-left: 3px solid; background: #141b26; transition: transform .2s;
}
.rxn-card:hover { transform: translateX(3px); }
.rxn-card.pos { border-left-color: #34d399; }
.rxn-card.neg { border-left-color: #f87171; }
.rxn-card.par { border-left-color: #fb923c; }
.rxn-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: .45rem; }
.rxn-sample-txt { font-weight: 600; font-size: .83rem; color: #e2e8f0; }
.rxn-badge {
    font-family: 'JetBrains Mono', monospace; font-size: .63rem; font-weight: 700;
    padding: .16rem .5rem; border-radius: 9999px; border: 1px solid;
}
.rxn-badge.pos { background: rgba(52,211,153,.12); color: #34d399; border-color: rgba(52,211,153,.3); }
.rxn-badge.neg { background: rgba(248,113,113,.12); color: #f87171; border-color: rgba(248,113,113,.3); }
.rxn-badge.par { background: rgba(251,146,60,.12);  color: #fb923c; border-color: rgba(251,146,60,.3);  }
.rxn-eq {
    font-family: 'JetBrains Mono', monospace; font-size: .73rem; color: #93c5fd;
    background: rgba(56,189,248,.04); border-radius: 7px;
    padding: .4rem .65rem; line-height: 1.6; word-break: break-all; margin-bottom: .35rem;
}
.rxn-result { font-size: .78rem; padding: .28rem .65rem; border-radius: 7px; border: 1px dashed; }
.rxn-result.pos { color: #34d399; border-color: rgba(52,211,153,.2); background: rgba(52,211,153,.04); }
.rxn-result.neg { color: #f87171; border-color: rgba(248,113,113,.2); background: rgba(248,113,113,.04); }
.rxn-result.par { color: #fb923c; border-color: rgba(251,146,60,.2);  background: rgba(251,146,60,.04);  }

/* ── STREAMLIT OVERRIDES ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1117 !important; border-radius: 12px !important;
    padding: .3rem !important; border: 1px solid rgba(56,189,248,.15) !important; gap: .25rem !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important; color: #64748b !important;
    font-family: 'JetBrains Mono', monospace !important; font-size: .76rem !important;
    border-radius: 9px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(56,189,248,.18), rgba(129,140,248,.13)) !important;
    color: #38bdf8 !important; border: 1px solid rgba(56,189,248,.35) !important;
}
div[data-testid="stExpander"] {
    background: #0d1117 !important; border: 1px solid rgba(56,189,248,.15) !important;
    border-radius: 12px !important; margin-bottom: .5rem !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace !important;
    color: #38bdf8 !important; font-size: .8rem !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(56,189,248,.12), rgba(129,140,248,.08)) !important;
    border: 1px solid rgba(56,189,248,.3) !important;
    color: #38bdf8 !important; font-family: 'JetBrains Mono', monospace !important;
    border-radius: 9px !important; font-size: .78rem !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, rgba(56,189,248,.22), rgba(129,140,248,.16)) !important;
    box-shadow: 0 0 15px rgba(56,189,248,.18) !important;
}
/* Streamlit button (nav pills) */
div[data-testid="column"] .stButton > button {
    width: 100%; border-radius: 12px; padding: .7rem .4rem;
    background: rgba(255,255,255,.02) !important;
    border: 1px solid rgba(56,189,248,.14) !important;
    color: #94a3b8 !important; font-family: 'Inter', sans-serif !important;
    font-size: .78rem !important; transition: all .22s ease;
    line-height: 1.4; white-space: normal !important; height: auto !important;
}
div[data-testid="column"] .stButton > button:hover {
    border-color: rgba(56,189,248,.45) !important;
    background: rgba(56,189,248,.07) !important;
    color: #e2e8f0 !important;
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(56,189,248,.1) !important;
}
div[data-testid="column"] .stButton > button:focus {
    border-color: #38bdf8 !important;
    background: linear-gradient(135deg, rgba(56,189,248,.15), rgba(129,140,248,.10)) !important;
    color: #e2e8f0 !important;
    box-shadow: 0 0 24px rgba(56,189,248,.18) !important;
}
/* active nav pill via data-active class trick — fallback via selected state */
.nav-active > button {
    border-color: #38bdf8 !important;
    background: linear-gradient(135deg, rgba(56,189,248,.18), rgba(129,140,248,.12)) !important;
    color: #e2e8f0 !important;
    box-shadow: 0 0 22px rgba(56,189,248,.2) !important;
}

/* Legend */
.legend-inline {
    display: flex; flex-wrap: wrap; gap: .75rem; align-items: center;
    font-family: 'JetBrains Mono', monospace; font-size: .7rem; color: #475569;
    padding: .6rem 1rem; background: #0d1117;
    border: 1px solid rgba(56,189,248,.1); border-radius: 10px; margin-bottom: 1rem;
}
.legend-item { display: flex; align-items: center; gap: .3rem; }

/* Nav panel wrapper */
.nav-panel-wrap {
    background: #0d1117; border: 1px solid rgba(56,189,248,.12);
    border-radius: 18px; padding: .85rem; margin-bottom: 1.5rem;
}
.nav-panel-label {
    font-family: 'JetBrains Mono', monospace; font-size: .65rem; color: #334155;
    text-transform: uppercase; letter-spacing: .12em; margin-bottom: .65rem;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# DATA — SVG MOLEKUL
# ─────────────────────────────────────────────────────────────────────
SVG = {
    "n-Heksana": """<svg viewBox="0 0 340 72" xmlns="http://www.w3.org/2000/svg" width="300" height="64">
  <line x1="18" y1="36" x2="60" y2="20" stroke="#334155" stroke-width="2"/>
  <line x1="60" y1="20" x2="105" y2="36" stroke="#334155" stroke-width="2"/>
  <line x1="105" y1="36" x2="150" y2="20" stroke="#334155" stroke-width="2"/>
  <line x1="150" y1="20" x2="195" y2="36" stroke="#334155" stroke-width="2"/>
  <line x1="195" y1="36" x2="240" y2="20" stroke="#334155" stroke-width="2"/>
  <line x1="240" y1="20" x2="285" y2="36" stroke="#334155" stroke-width="2"/>
  <text x="5"   y="50" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <text x="48"  y="15" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="92"  y="50" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="138" y="15" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="182" y="50" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="274" y="50" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <text x="150" y="66" text-anchor="middle" fill="#6366f1" font-size="9" font-weight="bold" font-family="monospace">ALKANA — C₆H₁₄</text>
</svg>""",

    "Benzena": """<svg viewBox="0 0 180 170" xmlns="http://www.w3.org/2000/svg" width="160" height="152">
  <polygon points="90,18 145,50 145,114 90,146 35,114 35,50" fill="none" stroke="#334155" stroke-width="2.5"/>
  <circle cx="90" cy="82" r="30" fill="none" stroke="#f59e0b" stroke-width="1.8" stroke-dasharray="5,3"/>
  <text x="90" y="11" text-anchor="middle" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="151" y="54" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="151" y="118" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="90" y="160" text-anchor="middle" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="18" y="118" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="18" y="54" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="90" y="86" text-anchor="middle" fill="#f59e0b" font-size="9.5" font-family="monospace">aromatic</text>
  <text x="90" y="98" text-anchor="middle" fill="#f59e0b" font-size="8.5" font-family="monospace">6π e⁻</text>
</svg>""",

    "1-Butanol": """<svg viewBox="0 0 310 95" xmlns="http://www.w3.org/2000/svg" width="280" height="86">
  <line x1="18" y1="52" x2="70" y2="32" stroke="#334155" stroke-width="2"/>
  <line x1="70" y1="32" x2="125" y2="52" stroke="#334155" stroke-width="2"/>
  <line x1="125" y1="52" x2="178" y2="32" stroke="#334155" stroke-width="2"/>
  <line x1="178" y1="32" x2="232" y2="52" stroke="#334155" stroke-width="2"/>
  <line x1="232" y1="52" x2="268" y2="25" stroke="#ef4444" stroke-width="2.5"/>
  <text x="5"   y="66" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <text x="57"  y="26" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="112" y="66" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="164" y="26" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="271" y="23" fill="#ef4444" font-size="11" font-weight="bold" font-family="monospace">OH</text>
  <text x="145" y="84" text-anchor="middle" fill="#0ea5e9" font-size="9" font-weight="bold" font-family="monospace">PRIMER — 2H pada C-OH</text>
</svg>""",

    "2-Butanol": """<svg viewBox="0 0 295 112" xmlns="http://www.w3.org/2000/svg" width="265" height="100">
  <line x1="18" y1="66" x2="75" y2="46" stroke="#334155" stroke-width="2"/>
  <line x1="75" y1="46" x2="142" y2="66" stroke="#334155" stroke-width="2"/>
  <line x1="142" y1="66" x2="205" y2="46" stroke="#334155" stroke-width="2"/>
  <line x1="205" y1="46" x2="262" y2="66" stroke="#334155" stroke-width="2"/>
  <line x1="142" y1="66" x2="142" y2="20" stroke="#ef4444" stroke-width="2.5"/>
  <text x="5"   y="80" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <text x="62"  y="40" fill="#334155" font-size="11" font-family="monospace">CH</text>
  <text x="190" y="40" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="248" y="80" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <text x="132" y="15" fill="#ef4444" font-size="11" font-weight="bold" font-family="monospace">OH</text>
  <text x="142" y="98" text-anchor="middle" fill="#0ea5e9" font-size="9" font-weight="bold" font-family="monospace">SEKUNDER — 1H pada C-OH</text>
</svg>""",

    "t-Butil Alkohol": """<svg viewBox="0 0 215 185" xmlns="http://www.w3.org/2000/svg" width="192" height="165">
  <circle cx="108" cy="90" r="18" fill="#6366f1"/>
  <text x="108" y="95" text-anchor="middle" fill="white" font-size="11" font-weight="bold" font-family="monospace">C</text>
  <line x1="108" y1="72" x2="108" y2="35" stroke="#334155" stroke-width="2"/>
  <text x="96"  y="29" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <line x1="90"  y1="90" x2="38" y2="90" stroke="#334155" stroke-width="2"/>
  <text x="7"   y="94" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <line x1="126" y1="90" x2="175" y2="90" stroke="#334155" stroke-width="2"/>
  <text x="174" y="94" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <line x1="108" y1="108" x2="108" y2="148" stroke="#ef4444" stroke-width="2.5"/>
  <text x="96"  y="162" fill="#ef4444" font-size="11" font-weight="bold" font-family="monospace">OH</text>
  <text x="108" y="178" text-anchor="middle" fill="#0ea5e9" font-size="9" font-weight="bold" font-family="monospace">TERSIER — 0H pada C-OH</text>
</svg>""",

    "Fenol": """<svg viewBox="0 0 185 180" xmlns="http://www.w3.org/2000/svg" width="166" height="162">
  <polygon points="85,22 140,55 140,122 85,154 30,122 30,55" fill="none" stroke="#334155" stroke-width="2.5"/>
  <circle cx="85" cy="88" r="28" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="85" y="14" text-anchor="middle" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="146" y="59" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="146" y="126" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="85" y="168" text-anchor="middle" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="14" y="126" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="14" y="59" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <line x1="85" y1="22" x2="85" y2="-5" stroke="#ef4444" stroke-width="2.5"/>
  <text x="72" y="-8" fill="#ef4444" font-size="11" font-weight="bold">OH</text>
  <text x="85" y="175" text-anchor="middle" fill="#f59e0b" font-size="8" font-family="monospace">OH pada cincin aromatik</text>
</svg>""",

    "Asetaldehid": """<svg viewBox="0 0 225 100" xmlns="http://www.w3.org/2000/svg" width="200" height="89">
  <line x1="18" y1="50" x2="95" y2="50" stroke="#334155" stroke-width="2"/>
  <line x1="95" y1="43" x2="178" y2="43" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="95" y1="57" x2="178" y2="57" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="178" y1="50" x2="205" y2="25" stroke="#64748b" stroke-width="1.5"/>
  <text x="5"   y="64" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="88"  y="39" fill="#6366f1" font-size="12" font-family="monospace">C</text>
  <text x="182" y="48" fill="#ef4444" font-size="14" font-weight="bold" font-family="monospace">O</text>
  <text x="208" y="22" fill="#64748b" font-size="11" font-family="monospace">H</text>
  <text x="112" y="88" text-anchor="middle" fill="#ef4444" font-size="9" font-weight="bold" font-family="monospace">ALDEHID — -CHO di ujung</text>
</svg>""",

    "Benzaldehid": """<svg viewBox="0 0 300 172" xmlns="http://www.w3.org/2000/svg" width="270" height="154">
  <polygon points="82,22 132,53 132,114 82,145 32,114 32,53" fill="none" stroke="#334155" stroke-width="2.5"/>
  <circle cx="82" cy="83" r="26" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="82" y="14" text-anchor="middle" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="138" y="57" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="138" y="118" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="82"  y="158" text-anchor="middle" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="16"  y="118" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="16"  y="57" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <line x1="132" y1="83" x2="188" y2="83" stroke="#334155" stroke-width="2"/>
  <text x="188" y="80" fill="#6366f1" font-size="12" font-weight="bold" font-family="monospace">C</text>
  <line x1="188" y1="66" x2="188" y2="43" stroke="#64748b" stroke-width="1.5"/>
  <text x="182" y="39" fill="#64748b" font-size="11" font-family="monospace">H</text>
  <line x1="200" y1="76" x2="244" y2="76" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="200" y1="88" x2="244" y2="88" stroke="#ef4444" stroke-width="2.5"/>
  <text x="247" y="86" fill="#ef4444" font-size="14" font-weight="bold" font-family="monospace">O</text>
  <text x="148" y="168" text-anchor="middle" fill="#f59e0b" font-size="9" font-weight="bold" font-family="monospace">ALDEHID AROMATIK — C₆H₅CHO</text>
</svg>""",

    "Aseton": """<svg viewBox="0 0 265 97" xmlns="http://www.w3.org/2000/svg" width="238" height="87">
  <line x1="18" y1="56" x2="95" y2="56" stroke="#334155" stroke-width="2"/>
  <line x1="95" y1="49" x2="170" y2="49" stroke="#8b5cf6" stroke-width="2.5"/>
  <line x1="95" y1="63" x2="170" y2="63" stroke="#8b5cf6" stroke-width="2.5"/>
  <line x1="170" y1="56" x2="242" y2="56" stroke="#334155" stroke-width="2"/>
  <line x1="132" y1="41" x2="132" y2="14" stroke="#ef4444" stroke-width="2.5"/>
  <text x="5"   y="70" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="111" y="45" fill="#6366f1" font-size="11" font-family="monospace">C=O</text>
  <text x="230" y="70" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="124" y="10" fill="#ef4444" font-size="12" font-weight="bold" font-family="monospace">O</text>
  <text x="132" y="86" text-anchor="middle" fill="#8b5cf6" font-size="9" font-weight="bold" font-family="monospace">KETON — C=O di tengah</text>
</svg>""",

    "Asam Asetat": """<svg viewBox="0 0 255 108" xmlns="http://www.w3.org/2000/svg" width="228" height="96">
  <line x1="18" y1="58" x2="93" y2="58" stroke="#334155" stroke-width="2"/>
  <line x1="93" y1="51" x2="172" y2="51" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="93" y1="65" x2="172" y2="65" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="172" y1="58" x2="214" y2="25" stroke="#10b981" stroke-width="2.5"/>
  <line x1="172" y1="58" x2="218" y2="86" stroke="#ef4444" stroke-width="2"/>
  <text x="5"   y="72" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="86"  y="47" fill="#6366f1" font-size="11" font-family="monospace">C</text>
  <text x="217" y="22" fill="#10b981" font-size="11" font-weight="bold" font-family="monospace">OH</text>
  <text x="222" y="89" fill="#ef4444" font-size="12" font-weight="bold" font-family="monospace">O</text>
  <text x="128" y="98" text-anchor="middle" fill="#10b981" font-size="9" font-weight="bold" font-family="monospace">GUGUS KARBOKSIL (-COOH)</text>
</svg>""",

    "Asam Oksalat": """<svg viewBox="0 0 265 108" xmlns="http://www.w3.org/2000/svg" width="238" height="97">
  <line x1="88" y1="52" x2="178" y2="52" stroke="#334155" stroke-width="2.5"/>
  <line x1="88" y1="64" x2="178" y2="64" stroke="#334155" stroke-width="2.5"/>
  <line x1="88" y1="58" x2="44" y2="24" stroke="#10b981" stroke-width="2.5"/>
  <line x1="88" y1="58" x2="40" y2="86" stroke="#ef4444" stroke-width="2"/>
  <line x1="178" y1="58" x2="222" y2="24" stroke="#10b981" stroke-width="2.5"/>
  <line x1="178" y1="58" x2="226" y2="86" stroke="#ef4444" stroke-width="2"/>
  <text x="22" y="21" fill="#10b981" font-size="11" font-weight="bold" font-family="monospace">HO</text>
  <text x="18" y="89" fill="#ef4444" font-size="12" font-weight="bold" font-family="monospace">O</text>
  <text x="80" y="46" fill="#6366f1" font-size="11" font-family="monospace">C</text>
  <text x="170" y="46" fill="#6366f1" font-size="11" font-family="monospace">C</text>
  <text x="224" y="21" fill="#10b981" font-size="11" font-weight="bold" font-family="monospace">OH</text>
  <text x="230" y="89" fill="#ef4444" font-size="12" font-weight="bold" font-family="monospace">O</text>
  <text x="133" y="98" text-anchor="middle" fill="#10b981" font-size="9" font-weight="bold" font-family="monospace">DIACID — dua gugus -COOH</text>
</svg>""",

    "Asam Oleat": """<svg viewBox="0 0 355 82" xmlns="http://www.w3.org/2000/svg" width="318" height="73">
  <text x="5" y="16" fill="#64748b" font-size="9" font-family="monospace">CH₃(CH₂)₇</text>
  <line x1="88" y1="42" x2="138" y2="24" stroke="#334155" stroke-width="2"/>
  <line x1="138" y1="24" x2="186" y2="42" stroke="#0ea5e9" stroke-width="2.5"/>
  <line x1="141" y1="18" x2="189" y2="36" stroke="#0ea5e9" stroke-width="2.5"/>
  <text x="135" y="18" fill="#0ea5e9" font-size="9" font-weight="bold" font-family="monospace">C=C</text>
  <line x1="186" y1="42" x2="238" y2="24" stroke="#334155" stroke-width="2"/>
  <text x="240" y="24" fill="#64748b" font-size="9" font-family="monospace">(CH₂)₇</text>
  <text x="292" y="38" fill="#10b981" font-size="10" font-weight="bold" font-family="monospace">COOH</text>
  <text x="168" y="68" text-anchor="middle" fill="#0ea5e9" font-size="9" font-weight="bold" font-family="monospace">TAK JENUH — C18:1 (cis)</text>
</svg>""",

    "Etil Asetat": """<svg viewBox="0 0 290 98" xmlns="http://www.w3.org/2000/svg" width="260" height="88">
  <line x1="15" y1="52" x2="84" y2="52" stroke="#334155" stroke-width="2"/>
  <line x1="84" y1="45" x2="156" y2="45" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="84" y1="59" x2="156" y2="59" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="84" y1="34" x2="84" y2="12" stroke="#ef4444" stroke-width="2"/>
  <line x1="156" y1="52" x2="202" y2="52" stroke="#f59e0b" stroke-width="2.5"/>
  <line x1="202" y1="52" x2="268" y2="52" stroke="#334155" stroke-width="2"/>
  <text x="4"   y="66" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="77"  y="41" fill="#6366f1" font-size="11" font-family="monospace">C</text>
  <text x="76"  y="9"  fill="#ef4444" font-size="12" font-weight="bold" font-family="monospace">O</text>
  <text x="194" y="47" fill="#f59e0b" font-size="11" font-weight="bold" font-family="monospace">O</text>
  <text x="193" y="66" fill="#334155" font-size="11" font-family="monospace">C₂H₅</text>
  <text x="142" y="86" text-anchor="middle" fill="#f59e0b" font-size="9" font-weight="bold" font-family="monospace">ESTER — R-COO-R'</text>
</svg>""",

    "Etilamina": """<svg viewBox="0 0 238 110" xmlns="http://www.w3.org/2000/svg" width="212" height="98">
  <line x1="15" y1="58" x2="90" y2="58" stroke="#334155" stroke-width="2"/>
  <line x1="90" y1="58" x2="170" y2="58" stroke="#334155" stroke-width="2"/>
  <line x1="170" y1="58" x2="202" y2="30" stroke="#10b981" stroke-width="2.5"/>
  <line x1="170" y1="58" x2="202" y2="86" stroke="#10b981" stroke-width="2.5"/>
  <text x="3"   y="72" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="78"  y="72" fill="#334155" font-size="12" font-family="monospace">CH₂</text>
  <text x="162" y="54" fill="#10b981" font-size="13" font-weight="bold" font-family="monospace">N</text>
  <text x="206" y="27" fill="#10b981" font-size="12" font-family="monospace">H</text>
  <text x="206" y="89" fill="#10b981" font-size="12" font-family="monospace">H</text>
  <text x="119" y="100" text-anchor="middle" fill="#10b981" font-size="9" font-weight="bold" font-family="monospace">AMINA PRIMER (-NH₂)</text>
</svg>""",

    "Dimetilamina": """<svg viewBox="0 0 200 120" xmlns="http://www.w3.org/2000/svg" width="178" height="107">
  <circle cx="100" cy="60" r="18" fill="#10b981"/>
  <text x="100" y="65" text-anchor="middle" fill="white" font-size="12" font-weight="bold" font-family="monospace">N</text>
  <line x1="82" y1="60" x2="35" y2="36" stroke="#334155" stroke-width="2"/>
  <text x="5"  y="36" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <line x1="82" y1="60" x2="35" y2="84" stroke="#334155" stroke-width="2"/>
  <text x="5"  y="87" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <line x1="118" y1="60" x2="160" y2="40" stroke="#10b981" stroke-width="2"/>
  <text x="163" y="40" fill="#10b981" font-size="12" font-weight="bold" font-family="monospace">H</text>
  <text x="100" y="108" text-anchor="middle" fill="#10b981" font-size="9" font-weight="bold" font-family="monospace">AMINA SEKUNDER</text>
</svg>""",

    "Trietilamina": """<svg viewBox="0 0 242 148" xmlns="http://www.w3.org/2000/svg" width="216" height="132">
  <circle cx="121" cy="74" r="18" fill="#8b5cf6"/>
  <text x="121" y="79" text-anchor="middle" fill="white" font-size="12" font-weight="bold" font-family="monospace">N</text>
  <line x1="103" y1="74" x2="50" y2="50" stroke="#334155" stroke-width="2"/>
  <text x="5"  y="52" fill="#334155" font-size="11" font-family="monospace">C₂H₅</text>
  <line x1="103" y1="74" x2="46" y2="98" stroke="#334155" stroke-width="2"/>
  <text x="3"  y="101" fill="#334155" font-size="11" font-family="monospace">C₂H₅</text>
  <line x1="121" y1="56" x2="121" y2="20" stroke="#334155" stroke-width="2"/>
  <text x="107" y="15" fill="#334155" font-size="11" font-family="monospace">C₂H₅</text>
  <text x="121" y="130" text-anchor="middle" fill="#8b5cf6" font-size="9" font-weight="bold" font-family="monospace">AMINA TERSIER — tanpa H pada N</text>
</svg>""",

    "Trigliserida": """<svg viewBox="0 0 358 162" xmlns="http://www.w3.org/2000/svg" width="320" height="145">
  <rect x="8"  y="26" width="52" height="20" rx="5" fill="#6366f1"/>
  <rect x="8"  y="70" width="52" height="20" rx="5" fill="#6366f1"/>
  <rect x="8"  y="114" width="52" height="20" rx="5" fill="#6366f1"/>
  <text x="34" y="40" text-anchor="middle" fill="white" font-size="9" font-family="monospace">CH₂</text>
  <text x="34" y="84" text-anchor="middle" fill="white" font-size="9" font-family="monospace">CH</text>
  <text x="34" y="128" text-anchor="middle" fill="white" font-size="9" font-family="monospace">CH₂</text>
  <rect x="62" y="26" width="46" height="20" rx="4" fill="#ef4444"/>
  <rect x="62" y="70" width="46" height="20" rx="4" fill="#ef4444"/>
  <rect x="62" y="114" width="46" height="20" rx="4" fill="#ef4444"/>
  <text x="85" y="40" text-anchor="middle" fill="white" font-size="8" font-family="monospace">O-C=O</text>
  <text x="85" y="84" text-anchor="middle" fill="white" font-size="8" font-family="monospace">O-C=O</text>
  <text x="85" y="128" text-anchor="middle" fill="white" font-size="8" font-family="monospace">O-C=O</text>
  <line x1="108" y1="36" x2="345" y2="36" stroke="#0ea5e9" stroke-width="2"/>
  <line x1="108" y1="80" x2="345" y2="80" stroke="#0ea5e9" stroke-width="2"/>
  <line x1="108" y1="124" x2="328" y2="124" stroke="#0ea5e9" stroke-width="2"/>
  <text x="225" y="30" fill="#0ea5e9" font-size="9" font-family="monospace">R₁ — asam lemak (C14–C22)</text>
  <text x="225" y="74" fill="#0ea5e9" font-size="9" font-family="monospace">R₂ — asam lemak</text>
  <text x="225" y="118" fill="#0ea5e9" font-size="9" font-family="monospace">R₃ — asam lemak</text>
  <text x="178" y="150" text-anchor="middle" fill="#f59e0b" font-size="9" font-weight="bold" font-family="monospace">TRIESTER GLISEROL — lemak/minyak</text>
</svg>""",
}

# ─────────────────────────────────────────────────────────────────────
# DATA PERCOBAAN
# ─────────────────────────────────────────────────────────────────────
EXP_LIST = [
    {
        "key": "P1", "icon": "⚗️",
        "num": "Percobaan 1", "short": "Hidrokarbon",
        "title": "⚗️ P1 — Hidrokarbon",
        "color": "#6366f1",
        "samples": ["Heksana", "Minyak Tanah", "Benzena"],
        "molecules": [
            {"name":"n-Heksana",    "formula":"C₆H₁₄",       "mw":"86.18 g/mol",  "bp":"69 °C",    "iupac":"n-Hexane",        "svg_key":"n-Heksana"},
            {"name":"Benzena",      "formula":"C₆H₆",         "mw":"78.11 g/mol",  "bp":"80.1 °C",  "iupac":"Benzene",         "svg_key":"Benzena"},
        ],
        "tests": [
            {"name":"Uji Br₂/CCl₄ (Gelap)", "reagent":"Br₂ dalam CCl₄", "reactions":[
                {"sample":"Heksana",     "eq":"C₆H₁₄ + Br₂ → tidak bereaksi (gelap)",                              "result":"⚪ Warna coklat TETAP — alkana tidak reaktif dalam gelap","type":"neg"},
                {"sample":"Minyak Tanah","eq":"CₙH₂ₙ₊₂ + Br₂ → tidak bereaksi",                                   "result":"⚪ Warna coklat TETAP — komponen alkana dominan",         "type":"neg"},
                {"sample":"Benzena",    "eq":"C₆H₆ + Br₂ → tidak bereaksi (tanpa katalis Lewis)",                  "result":"⚪ Warna tetap — cincin aromatik stabil terhadap adisi", "type":"neg"},
            ]},
            {"name":"Uji Baeyer (KMnO₄)", "reagent":"KMnO₄ 0.1% (larutan ungu)", "reactions":[
                {"sample":"Heksana",     "eq":"C₆H₁₄ + KMnO₄ → tidak bereaksi",                                   "result":"🟣 Tetap UNGU — alkana jenuh tidak teroksidasi",         "type":"neg"},
                {"sample":"Minyak Tanah","eq":"CₙH₂ₙ₊₂ + KMnO₄ → tidak bereaksi",                                "result":"🟣 Tetap UNGU — alkana dominan",                        "type":"neg"},
                {"sample":"Benzena",    "eq":"C₆H₆ + KMnO₄ → tidak bereaksi",                                     "result":"🟣 Tetap UNGU — aromatik (6π) stabil",                 "type":"neg"},
            ]},
            {"name":"SEAr Benzena (Br₂/FeBr₃ & Nitrasi)", "reagent":"Br₂+FeBr₃ katalis / HNO₃+H₂SO₄ pekat", "reactions":[
                {"sample":"Benzena + Br₂/FeBr₃",  "eq":"C₆H₆ + Br₂ → C₆H₅Br + HBr  (FeBr₃ katalis, SEAr)",    "result":"✅ Bromobenzena + asap HBr — substitusi elektrofilik",  "type":"pos"},
                {"sample":"Benzena + HNO₃/H₂SO₄","eq":"C₆H₆ + HNO₃ → C₆H₅NO₂ + H₂O  (H₂SO₄ katalis)",        "result":"✅ Nitrobenzena KUNING berminyak, bau almond",          "type":"pos"},
            ]},
            {"name":"Pembuatan & Uji Asetilena", "reagent":"CaC₂+H₂O; uji Br₂ & AgNO₃/NH₃", "reactions":[
                {"sample":"CaC₂ + H₂O",           "eq":"CaC₂ + 2H₂O → HC≡CH↑ + Ca(OH)₂",                       "result":"🫧 Gas HC≡CH (bau bawang), gelembung terus-menerus",    "type":"pos"},
                {"sample":"HC≡CH + Br₂/CCl₄",     "eq":"HC≡CH + 2Br₂ → CHBr₂-CHBr₂",                           "result":"✅ Coklat Br₂ PUDAR cepat — adisi 2 mol Br₂",          "type":"pos"},
                {"sample":"HC≡CH + AgNO₃/NH₃",    "eq":"HC≡CH + 2[Ag(NH₃)₂]⁺ → AgC≡CAg↓ + 2NH₄⁺",            "result":"✅ Endapan PUTIH AgC≡CAg — alkuna terminal",           "type":"pos"},
            ]},
        ],
    },
    {
        "key": "P2", "icon": "🍷",
        "num": "Percobaan 2", "short": "Alkohol & Fenol",
        "title": "🍷 P2 — Alkohol, Fenol & Eter",
        "color": "#0ea5e9",
        "samples": ["1-Butanol", "2-Butanol", "t-Butil Alkohol", "Fenol"],
        "molecules": [
            {"name":"1-Butanol",       "formula":"C₄H₉OH",     "mw":"74.12 g/mol",  "bp":"117.7 °C","iupac":"Butan-1-ol",          "svg_key":"1-Butanol"},
            {"name":"2-Butanol",       "formula":"C₄H₉OH",     "mw":"74.12 g/mol",  "bp":"99.5 °C", "iupac":"Butan-2-ol",          "svg_key":"2-Butanol"},
            {"name":"t-Butil Alkohol", "formula":"(CH₃)₃COH",  "mw":"74.12 g/mol",  "bp":"82.2 °C", "iupac":"2-Methylpropan-2-ol", "svg_key":"t-Butil Alkohol"},
            {"name":"Fenol",           "formula":"C₆H₅OH",     "mw":"94.11 g/mol",  "bp":"181.7 °C","iupac":"Phenol",              "svg_key":"Fenol"},
        ],
        "tests": [
            {"name":"Pereaksi Lucas (ZnCl₂/HCl pekat)", "reagent":"ZnCl₂ anhidrat + HCl pekat", "reactions":[
                {"sample":"1-Butanol (primer)",    "eq":"CH₃(CH₂)₃OH + HCl → CH₃(CH₂)₃Cl + H₂O  (SN2 lambat)",             "result":"⚪ Tidak keruh dalam 5 menit → PRIMER",                 "type":"neg"},
                {"sample":"2-Butanol (sekunder)",  "eq":"CH₃CH(OH)C₂H₅ + HCl → CH₃CHClC₂H₅ + H₂O",                        "result":"🟡 Keruh dalam 5–10 menit → SEKUNDER",                 "type":"par"},
                {"sample":"t-Butil (tersier)",     "eq":"(CH₃)₃COH + HCl → (CH₃)₃CCl + H₂O  (SN1, karbokation tersier)",  "result":"✅ Keruh SEGERA <2 menit → TERSIER",                   "type":"pos"},
            ]},
            {"name":"Pereaksi Jones (CrO₃/H₂SO₄)", "reagent":"CrO₃ dalam H₂SO₄/Aseton (oranye)", "reactions":[
                {"sample":"1-Butanol",             "eq":"C₄H₉OH + CrO₃/H₂SO₄ → C₃H₇CHO → C₃H₇COOH  (Cr⁶⁺→Cr³⁺)",        "result":"✅ Oranye → HIJAU segera — primer teroksidasi",         "type":"pos"},
                {"sample":"2-Butanol",             "eq":"CH₃CHOHC₂H₅ + CrO₃ → CH₃COC₂H₅ (MEK keton)",                    "result":"✅ Oranye → HIJAU — sekunder → keton",                 "type":"pos"},
                {"sample":"t-Butil Alkohol",       "eq":"(CH₃)₃COH + CrO₃ → tidak bereaksi",                               "result":"⚪ Tetap ORANYE — tersier resisten oksidasi",          "type":"neg"},
            ]},
            {"name":"Uji Iodoform (I₂/NaOH)", "reagent":"I₂ + NaOH berlebih (60 °C)", "reactions":[
                {"sample":"2-Butanol",             "eq":"CH₃CH(OH)C₂H₅ + 3I₂ + 3NaOH → CHI₃↓ + C₂H₅COO⁻Na⁺ + 3NaI + 3H₂O","result":"✅ Endapan KUNING CHI₃ (bau antiseptik) → POSITIF",   "type":"pos"},
                {"sample":"1-Butanol",             "eq":"CH₃(CH₂)₃OH + I₂/NaOH → tidak menghasilkan CHI₃",                 "result":"⚪ Tidak ada endapan kuning → NEGATIF",                "type":"neg"},
                {"sample":"t-Butil Alkohol",       "eq":"(CH₃)₃COH + I₂/NaOH → tidak menghasilkan CHI₃",                  "result":"⚪ Tidak ada endapan kuning → NEGATIF",                "type":"neg"},
            ]},
            {"name":"Uji Fenol (FeCl₃, Br₂/H₂O, NaOH)", "reagent":"FeCl₃ 1% / air brom / NaOH", "reactions":[
                {"sample":"Fenol + FeCl₃",         "eq":"C₆H₅OH + FeCl₃ → [Fe(OC₆H₅)₆]³⁻ + H⁺",                          "result":"✅ Larutan UNGU/VIOLET intens → fenol positif",        "type":"pos"},
                {"sample":"Fenol + Br₂/H₂O",       "eq":"C₆H₅OH + 3Br₂ → C₆H₂Br₃OH↓ + 3HBr  (2,4,6-tribromofenol)",    "result":"✅ Endapan PUTIH — tanpa katalis (OH aktivasi kuat)",  "type":"pos"},
                {"sample":"Fenol + NaOH",           "eq":"C₆H₅OH + NaOH → C₆H₅O⁻Na⁺ + H₂O",                              "result":"✅ Larut sempurna — fenol bersifat asam (pKa 9.95)",  "type":"pos"},
            ]},
        ],
    },
    {
        "key": "P3", "icon": "🧪",
        "num": "Percobaan 3", "short": "Aldehid & Keton",
        "title": "🧪 P3 — Aldehid & Keton",
        "color": "#ef4444",
        "samples": ["Asetaldehid", "Benzaldehid", "Aseton"],
        "molecules": [
            {"name":"Asetaldehid", "formula":"CH₃CHO",   "mw":"44.05 g/mol",  "bp":"20.2 °C",  "iupac":"Ethanal",      "svg_key":"Asetaldehid"},
            {"name":"Benzaldehid", "formula":"C₆H₅CHO",  "mw":"106.12 g/mol", "bp":"178.1 °C", "iupac":"Benzaldehyde", "svg_key":"Benzaldehid"},
            {"name":"Aseton",      "formula":"CH₃COCH₃", "mw":"58.08 g/mol",  "bp":"56.05 °C", "iupac":"Propan-2-one", "svg_key":"Aseton"},
        ],
        "tests": [
            {"name":"Pereaksi Tollens (Cermin Perak)", "reagent":"[Ag(NH₃)₂]⁺ — tabung bersih, suhu 40 °C", "reactions":[
                {"sample":"Asetaldehid","eq":"CH₃CHO + 2[Ag(NH₃)₂]⁺ + 2OH⁻ → CH₃COO⁻ + 2Ag⁰↓ + 4NH₃ + H₂O",           "result":"✅ CERMIN PERAK mengkilap di dinding tabung",          "type":"pos"},
                {"sample":"Benzaldehid","eq":"C₆H₅CHO + 2[Ag(NH₃)₂]⁺ + 2OH⁻ → C₆H₅COO⁻ + 2Ag⁰↓ + 4NH₃ + H₂O",        "result":"✅ CERMIN PERAK — aldehid aromatik bereaksi",         "type":"pos"},
                {"sample":"Aseton",    "eq":"CH₃COCH₃ + Tollens → tidak bereaksi",                                         "result":"⚪ Tidak ada cermin perak → KETON NEGATIF",           "type":"neg"},
            ]},
            {"name":"Pereaksi Fehling (Cu²⁺ → Cu₂O)", "reagent":"Fehling A + Fehling B, didihkan", "reactions":[
                {"sample":"Asetaldehid","eq":"CH₃CHO + 2Cu²⁺ + 5OH⁻ → CH₃COO⁻ + Cu₂O↓ + 3H₂O",                         "result":"✅ Endapan MERAH BATA Cu₂O — aldehid alifatik",       "type":"pos"},
                {"sample":"Benzaldehid","eq":"C₆H₅CHO + Fehling → tidak bereaksi (aldehid aromatik)",                     "result":"⚪ Tidak ada Cu₂O — aldehid aromatik NEGATIF",        "type":"neg"},
                {"sample":"Aseton",    "eq":"CH₃COCH₃ + Fehling → tidak bereaksi",                                        "result":"⚪ Tidak ada perubahan → KETON NEGATIF",              "type":"neg"},
            ]},
            {"name":"Pereaksi Schiff (Fuchsin/SO₂)", "reagent":"Reagen Schiff tidak berwarna", "reactions":[
                {"sample":"Asetaldehid","eq":"CH₃CHO + [Schiff] → kompleks merah-violet",                                  "result":"✅ Merah-VIOLET → aldehid positif Schiff",            "type":"pos"},
                {"sample":"Benzaldehid","eq":"C₆H₅CHO + [Schiff] → kompleks merah-violet",                                "result":"✅ Merah-VIOLET → aldehid aromatik positif",          "type":"pos"},
                {"sample":"Aseton",    "eq":"CH₃COCH₃ + [Schiff] → tidak bereaksi",                                       "result":"⚪ Tidak berwarna → KETON NEGATIF",                  "type":"neg"},
            ]},
            {"name":"Na-Bisulfit & Pembentukan Asetal", "reagent":"NaHSO₃ jenuh / ROH+H⁺ katalis", "reactions":[
                {"sample":"Asetaldehid + NaHSO₃", "eq":"CH₃CHO + NaHSO₃ → CH₃CH(OH)SO₃Na↓",                             "result":"✅ Endapan PUTIH kristal — adisi nukleofilik",        "type":"pos"},
                {"sample":"Benzaldehid + NaHSO₃", "eq":"C₆H₅CHO + NaHSO₃ → C₆H₅CH(OH)SO₃Na↓",                          "result":"✅ Endapan PUTIH — benzaldehid positif",             "type":"pos"},
                {"sample":"Aseton + NaHSO₃",      "eq":"CH₃COCH₃ + NaHSO₃ → (CH₃)₂C(OH)SO₃Na↓ (lambat)",              "result":"🟡 Endapan PUTIH lebih lambat — sterik lebih besar", "type":"par"},
                {"sample":"Asetaldehid → Asetal",  "eq":"CH₃CHO + 2CH₃OH → CH₃CH(OCH₃)₂ + H₂O  (H⁺ katalis)",         "result":"✅ Asetal terbentuk — NEGATIF Tollens (terlindungi)","type":"pos"},
            ]},
        ],
    },
    {
        "key": "P4", "icon": "🌿",
        "num": "Percobaan 4", "short": "Asam Karboksilat",
        "title": "🌿 P4 — Asam Karboksilat & Derivatnya",
        "color": "#10b981",
        "samples": ["Asam Asetat","Asam Oksalat","Asam Oleat","Etil Asetat","Anhidrida Ftalat"],
        "molecules": [
            {"name":"Asam Asetat",  "formula":"CH₃COOH",     "mw":"60.05 g/mol",  "bp":"117.9 °C","iupac":"Acetic Acid",      "svg_key":"Asam Asetat"},
            {"name":"Asam Oksalat", "formula":"HOOCCOOH",    "mw":"90.03 g/mol",  "bp":"189 °C",  "iupac":"Oxalic Acid",     "svg_key":"Asam Oksalat"},
            {"name":"Asam Oleat",   "formula":"C₁₇H₃₃COOH", "mw":"282.46 g/mol", "bp":"360 °C",  "iupac":"cis-9-Octadecenoic","svg_key":"Asam Oleat"},
            {"name":"Etil Asetat",  "formula":"CH₃COOC₂H₅", "mw":"88.11 g/mol",  "bp":"77.1 °C", "iupac":"Ethyl Acetate",   "svg_key":"Etil Asetat"},
        ],
        "tests": [
            {"name":"Uji Kelarutan", "reagent":"Air / heksana / NaOH", "reactions":[
                {"sample":"Asam Asetat + H₂O",  "eq":"CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺  (Ka=1.8×10⁻⁵)",              "result":"✅ LARUT SEMPURNA — miscible, ionisasi parsial",        "type":"pos"},
                {"sample":"Asam Oksalat + H₂O", "eq":"HOOCCOOH + H₂O ⇌ ⁻OOCCOOH + H₃O⁺",                            "result":"✅ LARUT — diacid hidrofilik (90 g/L @ 25°C)",          "type":"pos"},
                {"sample":"Asam Oleat + H₂O",   "eq":"C₁₈H₃₄O₂ + H₂O → tidak larut",                                 "result":"⚪ DUA LAPISAN — rantai C18 sangat hidrofobik",         "type":"neg"},
                {"sample":"Etil Asetat + H₂O",  "eq":"CH₃COOC₂H₅ + H₂O → larut parsial (8.3g/100mL)",               "result":"🟡 Sedikit larut — dua fase pada konsentrasi tinggi",  "type":"par"},
            ]},
            {"name":"Penggaraman & Saponifikasi (NaOH)", "reagent":"NaOH 10% / KOH + pemanasan", "reactions":[
                {"sample":"Asam Asetat + NaOH",  "eq":"CH₃COOH + NaOH → CH₃COO⁻Na⁺ + H₂O",                          "result":"✅ Netralisasi — bau cuka hilang, pH basa",             "type":"pos"},
                {"sample":"Asam Oksalat + NaOH", "eq":"HOOCCOOH + 2NaOH → NaOOCCOONa + 2H₂O",                        "result":"✅ Garam dinatrium oksalat — larut, pH basa",           "type":"pos"},
                {"sample":"Asam Oleat + NaOH",   "eq":"C₁₇H₃₃COOH + NaOH → C₁₇H₃₃COO⁻Na⁺ + H₂O",                  "result":"✅ Sabun sodium oleat berbusa — asam lemak tersabun",  "type":"pos"},
                {"sample":"Etil Asetat + NaOH",  "eq":"CH₃COOC₂H₅ + NaOH → CH₃COO⁻Na⁺ + C₂H₅OH",                  "result":"✅ Saponifikasi — lapisan ester hilang, homogen",       "type":"pos"},
            ]},
            {"name":"Reaksi Oksidasi (KMnO₄)", "reagent":"KMnO₄ dalam H₂SO₄ encer", "reactions":[
                {"sample":"Asam Oksalat",         "eq":"5HOOCCOOH + 2KMnO₄ + 3H₂SO₄ → 10CO₂↑ + 2MnSO₄ + K₂SO₄ + 8H₂O","result":"✅ KMnO₄ ungu → TAK BERWARNA — oksidasi sempurna",   "type":"pos"},
                {"sample":"Asam Oleat",           "eq":"-CH=CH- + KMnO₄ → diol/asam pendek + MnO₂↓",                 "result":"✅ Ungu pudar + endapan coklat MnO₂",                  "type":"pos"},
                {"sample":"Asam Asetat",          "eq":"CH₃COOH + KMnO₄ → tidak bereaksi (jenuh)",                   "result":"⚪ Tetap UNGU — asam jenuh stabil",                    "type":"neg"},
            ]},
            {"name":"Identifikasi Ester & Anhidrida", "reagent":"NH₂OH/FeCl₃ (uji hidroxamat) / H₂O", "reactions":[
                {"sample":"Etil Asetat + NH₂OH/FeCl₃","eq":"CH₃COOC₂H₅ + NH₂OH → CH₃CONHOH + C₂H₅OH  (+FeCl₃→ merah)","result":"✅ Larutan MERAH/UNGU — ester positif hidroxamat",    "type":"pos"},
                {"sample":"Anh. Ftalat + H₂O",    "eq":"C₆H₄(CO)₂O + H₂O → C₆H₄(COOH)₂ (asam ftalat)",            "result":"✅ Endapan PUTIH asam ftalat — anhidrida terhidrolisis","type":"pos"},
            ]},
        ],
    },
    {
        "key": "P5", "icon": "🔵",
        "num": "Percobaan 5", "short": "Amina",
        "title": "🔵 P5 — Amina & Derivatnya",
        "color": "#8b5cf6",
        "samples": ["Etilamina", "Dimetilamina", "Trietilamina"],
        "molecules": [
            {"name":"Etilamina",    "formula":"CH₃CH₂NH₂", "mw":"45.08 g/mol",  "bp":"16.6 °C", "iupac":"Ethanamine",    "svg_key":"Etilamina"},
            {"name":"Dimetilamina", "formula":"(CH₃)₂NH",  "mw":"45.08 g/mol",  "bp":"7.4 °C",  "iupac":"Dimethylamine", "svg_key":"Dimetilamina"},
            {"name":"Trietilamina", "formula":"(C₂H₅)₃N", "mw":"101.19 g/mol", "bp":"89.7 °C", "iupac":"Triethylamine", "svg_key":"Trietilamina"},
        ],
        "tests": [
            {"name":"Uji Kelarutan & Kebasaan (pH)", "reagent":"Air suling + indikator universal", "reactions":[
                {"sample":"Etilamina",    "eq":"CH₃CH₂NH₂ + H₂O ⇌ CH₃CH₂NH₃⁺ + OH⁻  (Kb=5.4×10⁻⁴)",               "result":"✅ pH > 7, bau amis menyengat — AMINA PRIMER",         "type":"pos"},
                {"sample":"Dimetilamina", "eq":"(CH₃)₂NH + H₂O ⇌ (CH₃)₂NH₂⁺ + OH⁻  (Kb=5.9×10⁻⁴)",                "result":"✅ pH > 7, basa lebih kuat dari primer",               "type":"pos"},
                {"sample":"Trietilamina", "eq":"(C₂H₅)₃N + H₂O ⇌ (C₂H₅)₃NH⁺ + OH⁻",                                "result":"✅ pH > 7, basa (sedikit lemah karena sterik)",        "type":"pos"},
            ]},
            {"name":"Uji Hinsberg (C₆H₅SO₂Cl)", "reagent":"Benzenasulfonil klorida + NaOH aq.", "reactions":[
                {"sample":"Etilamina (primer)",     "eq":"C₂H₅NH₂ + C₆H₅SO₂Cl → C₆H₅SO₂NHC₂H₅ + HCl  (larut NaOH)","result":"✅ Sulfonamid LARUT NaOH → AMINA PRIMER",             "type":"pos"},
                {"sample":"Dimetilamina (sekunder)","eq":"(CH₃)₂NH + C₆H₅SO₂Cl → C₆H₅SO₂N(CH₃)₂ + HCl  (tak larut NaOH)","result":"🟡 Endapan TAK larut NaOH → AMINA SEKUNDER",   "type":"par"},
                {"sample":"Trietilamina (tersier)", "eq":"(C₂H₅)₃N + C₆H₅SO₂Cl → tidak bereaksi",                   "result":"⚪ Tidak ada sulfonamid → AMINA TERSIER",             "type":"neg"},
            ]},
            {"name":"Diazotisasi & Kopling Azo", "reagent":"NaNO₂+HCl (0–5 °C) → kopling β-naftol", "reactions":[
                {"sample":"Anilina (ref. aromatik)","eq":"C₆H₅NH₂ + NaNO₂ + 2HCl → C₆H₅N₂⁺Cl⁻ + NaCl + 2H₂O  (0-5°C)","result":"✅ Garam diazonium stabil — tidak berwarna di 0-5 °C","type":"pos"},
                {"sample":"Diazonium + β-naftol",   "eq":"C₆H₅N₂⁺ + C₁₀H₇OH → C₆H₅-N=N-C₁₀H₆OH + H⁺",           "result":"✅ PEWARNA AZO MERAH/ORANYE terbentuk",               "type":"pos"},
                {"sample":"Etilamina (alifatik)",   "eq":"C₂H₅NH₂ + NaNO₂ + HCl → C₂H₅OH + N₂↑ + NaCl + H₂O",    "result":"🫧 Gas N₂ gelembung — diazonium alifatik tak stabil", "type":"par"},
            ]},
        ],
    },
    {
        "key": "P6", "icon": "🫙",
        "num": "Percobaan 6", "short": "Lemak & Minyak",
        "title": "🫙 P6 — Lemak & Minyak",
        "color": "#f59e0b",
        "samples": ["Margarin","Mentega","Minyak Sawit","Minyak Kedelai","Minyak Tengik"],
        "molecules": [
            {"name":"Trigliserida (Umum)","formula":"C₃H₅(OOCR)₃","mw":"~885 g/mol","bp":">300 °C","iupac":"Triglyceride","svg_key":"Trigliserida"},
        ],
        "tests": [
            {"name":"Uji Kelarutan", "reagent":"Air / heksana / kloroform", "reactions":[
                {"sample":"Semua sampel + H₂O",    "eq":"Trigliserida + H₂O → tidak larut (nonpolar vs polar)",             "result":"⚪ DUA LAPISAN, minyak mengapung — hidrofobik",         "type":"neg"},
                {"sample":"Semua sampel + heksana", "eq":"Trigliserida + C₆H₁₄ → larut (like dissolves like)",              "result":"✅ LARUT SEMPURNA — nonpolar dalam nonpolar",           "type":"pos"},
            ]},
            {"name":"Saponifikasi (NaOH/KOH)", "reagent":"NaOH 30% + pemanasan 30 menit", "reactions":[
                {"sample":"Minyak Sawit",   "eq":"(C₁₅H₃₁COO)₃C₃H₅ + 3NaOH → 3C₁₅H₃₁COO⁻Na⁺ + C₃H₅(OH)₃",          "result":"✅ Sabun sodium palmitat + gliserol, berbusa lebat",    "type":"pos"},
                {"sample":"Minyak Kedelai", "eq":"(RCO₂)₃C₃H₅ + 3NaOH → 3RCOONa + C₃H₅(OH)₃  (R=C₁₇:₂/C₁₇:₃)",     "result":"✅ Sabun linoleat/linolenat + gliserol",               "type":"pos"},
                {"sample":"Mentega",        "eq":"Trigliserida susu + NaOH → sabun campuran + gliserol",                  "result":"✅ Sabun lunak berbusa, bau mentega hilang",           "type":"pos"},
                {"sample":"Margarin",       "eq":"Trigliserida terhidrogenasi + KOH → sabun kalium (lunak)",             "result":"✅ Sabun kalium berbusa lebih lebat",                  "type":"pos"},
            ]},
            {"name":"Uji Ketidakjenuhan (Br₂/KMnO₄)", "reagent":"Br₂ dalam CCl₄ atau KMnO₄ 0.1%", "reactions":[
                {"sample":"Minyak Kedelai", "eq":"-CH=CH- (linoleat C18:2) + Br₂ → -CHBr-CHBr-  (adisi)",              "result":"✅ Br₂ CEPAT PUDAR — banyak C=C (C18:2, C18:3)",      "type":"pos"},
                {"sample":"Minyak Sawit",   "eq":"-CH=CH- (oleat C18:1) + Br₂ → -CHBr-CHBr-",                          "result":"🟡 Br₂ pudar LAMBAT — palmitat C16:0 dominan",        "type":"par"},
                {"sample":"Mentega",        "eq":"Asam lemak jenuh dominan + Br₂ → tidak bereaksi",                     "result":"⚪ Br₂ sangat sedikit pudar — jenuh dominan",         "type":"neg"},
                {"sample":"Margarin",       "eq":"Asam jenuh (terhidrogenasi) + Br₂ → bereaksi sedikit",                "result":"⚪ Sedikit pudar — proses hidrogenasi menjenuhkan",   "type":"neg"},
            ]},
            {"name":"Uji Ketengikan (Kreiss & NaHSO₃)", "reagent":"Phloroglucinol/HCl pekat / NaHSO₃ jenuh", "reactions":[
                {"sample":"Minyak Tengik (Kreiss)", "eq":"-CH=CH- + O₂ → ROOH → R-CHO + R'-CHO (aldehid)",             "result":"✅ MERAH/PINK — epihidrin aldehid positif ketengikan", "type":"pos"},
                {"sample":"Minyak Tengik + NaHSO₃", "eq":"RCHO + NaHSO₃ → RCH(OH)SO₃Na↓",                             "result":"✅ Endapan adduct — aldehid ketengikan terdeteksi",   "type":"pos"},
                {"sample":"Minyak Segar + Kreiss",  "eq":"Trigliserida segar + phloroglucinol → sedikit bereaksi",      "result":"⚪ Kuning pucat — segar, oksidasi minimal",           "type":"neg"},
            ]},
        ],
    },
]

# ─────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────
TYPE_META = {
    "pos": ("pos", "POSITIF"),
    "neg": ("neg", "NEGATIF"),
    "par": ("par", "PARSIAL"),
}

def render_rxn(rxn: dict):
    cls, label = TYPE_META[rxn["type"]]
    st.markdown(f"""
    <div class="rxn-card {cls}">
        <div class="rxn-top">
            <span class="rxn-sample-txt">{rxn['sample']}</span>
            <span class="rxn-badge {cls}">{label}</span>
        </div>
        <div class="rxn-eq">⚗ {rxn['eq']}</div>
        <div class="rxn-result {cls}">📋 {rxn['result']}</div>
    </div>""", unsafe_allow_html=True)

def render_mol(mol: dict):
    svg = SVG.get(mol["svg_key"], "<span style='color:#475569;font-size:.8rem'>SVG tidak tersedia</span>")
    st.markdown(f"""
    <div class="mol-card">
        <div class="mol-name">{mol['name']}</div>
        <div class="mol-svg-wrap">{svg}</div>
        <div>
            <span class="mol-badge">{mol['formula']}</span>
            <span class="mol-badge">MW: {mol['mw']}</span>
            <span class="mol-badge">bp: {mol['bp']}</span>
        </div>
        <div class="mol-iupac">IUPAC: {mol['iupac']}</div>
    </div>""", unsafe_allow_html=True)

def build_df(exp: dict) -> pd.DataFrame:
    rows = []
    for t in exp["tests"]:
        for r in t["reactions"]:
            rows.append({
                "Uji / Pereaksi":   t["name"],
                "Sampel":           r["sample"],
                "Persamaan Reaksi": r["eq"],
                "Hasil Pengamatan": r["result"],
                "Status": {"pos":"✅ Positif","neg":"⚪ Negatif","par":"🟡 Parsial"}[r["type"]],
            })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────────────────────────
# TOP NAVIGATION BAR (sticky)
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topbar">
    <div class="topbar-logo">⚗️ KIMIA ORGANIK</div>
    <div class="topbar-nav">
        <span style="font-family:'JetBrains Mono',monospace;font-size:.62rem;color:#334155;letter-spacing:.1em;margin-right:.3rem">PERCOBAAN →</span>
    </div>
    <div class="topbar-sep"></div>
    <div class="topbar-info">Laboratorium Kimia Organik · 2025</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# IN-PAGE NAVIGATION PANEL  (6 tombol besar, satu baris)
# ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="nav-panel-label">// PILIH PERCOBAAN</div>', unsafe_allow_html=True)

nav_cols = st.columns(6, gap="small")
for i, ep in enumerate(EXP_LIST):
    with nav_cols[i]:
        # highlight active button menggunakan label khusus
        active_mark = "▶ " if i == st.session_state.active_exp else ""
        label = f"{ep['icon']}\n**{ep['num'][:12]}**\n{ep['short']}"
        if st.button(
            f"{active_mark}{ep['icon']}  {ep['num']}\n{ep['short']}",
            key=f"nav_{i}",
            use_container_width=True,
        ):
            st.session_state.active_exp = i
            st.rerun()

# Garis pemisah tipis
st.markdown("<hr style='border:none;border-top:1px solid rgba(56,189,248,.1);margin:.5rem 0 1.25rem 0'>",
            unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# BREADCRUMB  (prev / next navigasi cepat)
# ─────────────────────────────────────────────────────────────────────
idx = st.session_state.active_exp
exp = EXP_LIST[idx]

bc1, bc2, bc3 = st.columns([1, 6, 1])
with bc1:
    if idx > 0:
        prev = EXP_LIST[idx - 1]
        if st.button(f"← {prev['icon']} {prev['key']}", use_container_width=True, key="prev_btn"):
            st.session_state.active_exp = idx - 1
            st.rerun()
with bc2:
    crumbs = " › ".join(
        f'<span class="breadcrumb-cur">{ep["icon"]} {ep["num"]} — {ep["short"]}</span>'
        if j == idx else
        f'<span style="color:#1e293b">{ep["icon"]} {ep["key"]}</span>'
        for j, ep in enumerate(EXP_LIST)
    )
    st.markdown(f'<div class="breadcrumb">{crumbs}</div>', unsafe_allow_html=True)
with bc3:
    if idx < len(EXP_LIST) - 1:
        nxt = EXP_LIST[idx + 1]
        if st.button(f"{nxt['icon']} {nxt['key']} →", use_container_width=True, key="next_btn"):
            st.session_state.active_exp = idx + 1
            st.rerun()

# ─────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────
chips = "".join(f'<span class="chip">{s}</span>' for s in exp["samples"])
st.markdown(f"""
<div class="hero-box">
    <div class="hero-eyebrow">// {exp['num']} · Kimia Organik</div>
    <div class="hero-title">{exp['title']}</div>
    <div class="hero-sub">sampel: {" · ".join(exp['samples'])}</div>
    <div class="chip-row">{chips}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# METRICS
# ─────────────────────────────────────────────────────────────────────
total_r = sum(len(t["reactions"]) for t in exp["tests"])
pos_r   = sum(1 for t in exp["tests"] for r in t["reactions"] if r["type"] == "pos")
par_r   = sum(1 for t in exp["tests"] for r in t["reactions"] if r["type"] == "par")
neg_r   = sum(1 for t in exp["tests"] for r in t["reactions"] if r["type"] == "neg")

st.markdown(f"""
<div class="metric-row">
    <div class="metric-card">
        <div class="metric-val">{len(exp['samples'])}</div>
        <div class="metric-lbl">Jumlah Sampel</div>
    </div>
    <div class="metric-card">
        <div class="metric-val">{len(exp['tests'])}</div>
        <div class="metric-lbl">Jenis Uji</div>
    </div>
    <div class="metric-card">
        <div class="metric-val">{total_r}</div>
        <div class="metric-lbl">Total Reaksi</div>
    </div>
    <div class="metric-card">
        <div class="metric-val" style="color:#34d399">{pos_r}</div>
        <div class="metric-lbl">Hasil Positif</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# LEGEND (inline, kompak)
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="legend-inline">
    <span style="color:#475569;font-weight:700;font-size:.68rem">LEGENDA:</span>
    <span class="legend-item"><span style="color:#34d399">✅</span> Positif/Bereaksi</span>
    <span class="legend-item"><span style="color:#fb923c">🟡</span> Parsial/Lambat</span>
    <span class="legend-item"><span style="color:#f87171">⚪</span> Negatif</span>
    <span class="legend-item"><span style="color:#38bdf8">🫧</span> Gas/Gelembung</span>
    <span style="margin-left:auto;color:#1e293b">
        ✅ {pos_r} positif &nbsp;·&nbsp; 🟡 {par_r} parsial &nbsp;·&nbsp; ⚪ {neg_r} negatif
    </span>
</div>
""".format(pos_r=pos_r, par_r=par_r, neg_r=neg_r), unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────
# TABS KONTEN
# ─────────────────────────────────────────────────────────────────────
tab_struct, tab_rxn, tab_tabel = st.tabs([
    "🔬  Struktur Kimia",
    "⚗️  Reaksi & Hasil",
    "📊  Tabel Ringkasan",
])

# ── TAB 1: STRUKTUR ──
with tab_struct:
    st.markdown('<div class="sec-head">// STRUKTUR MOLEKUL SAMPEL</div>', unsafe_allow_html=True)
    mols = exp["molecules"]
    n_cols = min(len(mols), 3)
    for row_start in range(0, len(mols), n_cols):
        row = mols[row_start: row_start + n_cols]
        cols = st.columns(len(row), gap="medium")
        for col, mol in zip(cols, row):
            with col:
                render_mol(mol)

# ── TAB 2: REAKSI ──
with tab_rxn:
    st.markdown('<div class="sec-head">// UJI KIMIA & HASIL REAKSI</div>', unsafe_allow_html=True)
    for test in exp["tests"]:
        n = len(test["reactions"])
        pos_n = sum(1 for r in test["reactions"] if r["type"] == "pos")
        with st.expander(f"🧬 {test['name']}  ·  {n} reaksi  ·  {pos_n} positif", expanded=True):
            st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#64748b;
                        margin-bottom:.7rem;padding:.38rem .65rem;
                        background:rgba(56,189,248,.04);border-radius:7px;
                        border-left:2px solid rgba(56,189,248,.3);">
                Pereaksi: {test['reagent']}
            </div>""", unsafe_allow_html=True)
            for rxn in test["reactions"]:
                render_rxn(rxn)

# ── TAB 3: TABEL ──
with tab_tabel:
    st.markdown('<div class="sec-head">// TABEL RINGKASAN SEMUA REAKSI</div>', unsafe_allow_html=True)
    df = build_df(exp)
    st.dataframe(
        df, use_container_width=True, height=520,
        column_config={
            "Uji / Pereaksi":   st.column_config.TextColumn(width="medium"),
            "Sampel":           st.column_config.TextColumn(width="medium"),
            "Persamaan Reaksi": st.column_config.TextColumn(width="large"),
            "Hasil Pengamatan": st.column_config.TextColumn(width="large"),
            "Status":           st.column_config.TextColumn(width="small"),
        },
    )
    col_dl, col_info = st.columns([1, 3])
    with col_dl:
        fname = f"{exp['key']}_{exp['short'].replace(' ','_')}.csv"
        st.download_button(
            "⬇️ Download CSV",
            df.to_csv(index=False).encode("utf-8"),
            file_name=fname, mime="text/csv",
        )
    with col_info:
        st.markdown(
            f"<span style='font-family:JetBrains Mono,monospace;font-size:.72rem;color:#334155'>"
            f"{total_r} baris · {pos_r} positif · {par_r} parsial · {neg_r} negatif</span>",
            unsafe_allow_html=True,
        )

# ─────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:2.5rem 0 .5rem 0;
            color:#1e293b;font-family:'JetBrains Mono',monospace;font-size:.7rem;
            border-top:1px solid rgba(56,189,248,.07);margin-top:2.5rem;">
    ⚗️ Laboratorium Kimia Organik &nbsp;·&nbsp; Aplikasi Praktikum Interaktif &nbsp;·&nbsp; 2025
</div>
""", unsafe_allow_html=True)
PYEOF
echo "Lines: $(wc -l < /mnt/user-data/outputs/kimia_organik_app.py)"
