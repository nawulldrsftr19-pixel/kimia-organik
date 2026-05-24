# ╔══════════════════════════════════════════════════════════════════════╗
# ║        APLIKASI PRAKTIKUM KIMIA ORGANIK — STREAMLIT APP             ║
# ║  Cara menjalankan:                                                   ║
# ║    pip install streamlit pandas                                       ║
# ║    streamlit run kimia_organik_app.py                                ║
# ╚══════════════════════════════════════════════════════════════════════╝

import streamlit as st
import pandas as pd

# ─────────────────────────────────────────────────────────────────────
# PAGE CONFIG  (harus baris pertama setelah import)
# ─────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Praktikum Kimia Organik",
    page_icon="⚗️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;500;600;700&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #06080f;
    color: #e2e8f0;
}
.block-container { padding: 1.5rem 2rem 3rem 2rem; max-width: 1300px; }
#MainMenu, footer, header { visibility: hidden; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #0d1b2a 100%) !important;
    border-right: 1px solid rgba(56,189,248,.15);
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebar"] .stRadio label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    padding: 0.5rem 0.75rem !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    transition: all .2s !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(56,189,248,.08) !important;
    color: #38bdf8 !important;
}

/* Hero Banner */
.hero-box {
    background: linear-gradient(135deg, #0d1117 0%, #141b26 50%, #0d1b2a 100%);
    border: 1px solid rgba(56,189,248,.2);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.hero-box::before {
    content: '';
    position: absolute; inset: 0;
    background: radial-gradient(circle at 15% 50%, rgba(56,189,248,.07) 0%, transparent 55%),
                radial-gradient(circle at 85% 20%, rgba(129,140,248,.06) 0%, transparent 55%);
    pointer-events: none;
}
.hero-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: .72rem; color: #38bdf8;
    letter-spacing: .12em; text-transform: uppercase;
    margin-bottom: .6rem;
}
.hero-title {
    font-size: 2rem; font-weight: 700; line-height: 1.15;
    background: linear-gradient(135deg, #e2e8f0, #38bdf8, #818cf8);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: .78rem; color: #64748b; margin-top: .4rem;
}

/* Metric Cards */
.metric-row { display: grid; grid-template-columns: repeat(4,1fr); gap: .85rem; margin-bottom: 1.5rem; }
.metric-card {
    background: #0d1117; border: 1px solid rgba(56,189,248,.15);
    border-radius: 14px; padding: 1.1rem; text-align: center;
    transition: border-color .25s, box-shadow .25s;
}
.metric-card:hover { border-color: rgba(56,189,248,.4); box-shadow: 0 0 18px rgba(56,189,248,.08); }
.metric-val { font-size: 1.8rem; font-weight: 700; color: #38bdf8; font-family: 'JetBrains Mono', monospace; }
.metric-lbl { font-size: .68rem; color: #64748b; text-transform: uppercase; letter-spacing: .06em; margin-top: .2rem; }

/* Section Header */
.sec-head {
    font-family: 'JetBrains Mono', monospace; font-size: .8rem;
    font-weight: 700; color: #38bdf8;
    border-left: 3px solid #38bdf8; padding-left: .75rem;
    margin: 1.2rem 0 .8rem 0;
}

/* Molecule Card */
.mol-card {
    background: #0d1117; border: 1px solid rgba(56,189,248,.15);
    border-radius: 14px; padding: 1.1rem;
    transition: all .25s; margin-bottom: .75rem;
}
.mol-card:hover { border-color: rgba(56,189,248,.4); transform: translateY(-2px); }
.mol-name { font-weight: 700; font-size: .9rem; color: #e2e8f0; margin-bottom: .6rem; }
.mol-svg-wrap { background: #f8fafc; border-radius: 10px; padding: .7rem; text-align: center; margin-bottom: .6rem; }
.mol-badge {
    display: inline-block; padding: .2rem .6rem; border-radius: 9999px;
    font-size: .68rem; font-weight: 600; font-family: 'JetBrains Mono', monospace;
    background: rgba(56,189,248,.1); border: 1px solid rgba(56,189,248,.25); color: #38bdf8;
    margin: .15rem;
}
.mol-iupac { font-size: .72rem; color: #818cf8; font-style: italic; margin-top: .4rem; }

/* Reaction Block */
.test-hdr {
    background: #141b26; border: 1px solid rgba(56,189,248,.15);
    border-radius: 12px; padding: .85rem 1.1rem; margin-bottom: .1rem;
    display: flex; justify-content: space-between; align-items: center;
}
.test-name-txt { font-weight: 700; font-size: .9rem; color: #e2e8f0; }
.test-reagent-txt { font-family: 'JetBrains Mono', monospace; font-size: .7rem; color: #64748b; margin-top: .25rem; }
.test-cnt {
    font-family: 'JetBrains Mono', monospace; font-size: .7rem; color: #38bdf8;
    background: rgba(56,189,248,.1); border: 1px solid rgba(56,189,248,.25);
    padding: .2rem .55rem; border-radius: 9999px; white-space: nowrap;
}

.rxn-card {
    border-radius: 11px; padding: .9rem 1.1rem; margin-bottom: .55rem;
    border-left: 3px solid; background: #141b26;
    transition: transform .2s;
}
.rxn-card:hover { transform: translateX(4px); }
.rxn-card.pos { border-left-color: #34d399; }
.rxn-card.neg { border-left-color: #f87171; }
.rxn-card.par { border-left-color: #fb923c; }

.rxn-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: .5rem; }
.rxn-sample-txt { font-weight: 600; font-size: .85rem; color: #e2e8f0; }
.rxn-badge {
    font-family: 'JetBrains Mono', monospace; font-size: .65rem; font-weight: 700;
    padding: .18rem .55rem; border-radius: 9999px; border: 1px solid;
}
.rxn-badge.pos { background: rgba(52,211,153,.12); color: #34d399; border-color: rgba(52,211,153,.3); }
.rxn-badge.neg { background: rgba(248,113,113,.12); color: #f87171; border-color: rgba(248,113,113,.3); }
.rxn-badge.par { background: rgba(251,146,60,.12);  color: #fb923c; border-color: rgba(251,146,60,.3);  }

.rxn-eq {
    font-family: 'JetBrains Mono', monospace; font-size: .75rem; color: #93c5fd;
    background: rgba(56,189,248,.04); border-radius: 7px;
    padding: .45rem .7rem; line-height: 1.6; word-break: break-all; margin-bottom: .4rem;
}
.rxn-result {
    font-size: .8rem; padding: .3rem .7rem; border-radius: 7px;
    border: 1px dashed;
}
.rxn-result.pos { color: #34d399; border-color: rgba(52,211,153,.2); background: rgba(52,211,153,.04); }
.rxn-result.neg { color: #f87171; border-color: rgba(248,113,113,.2); background: rgba(248,113,113,.04); }
.rxn-result.par { color: #fb923c; border-color: rgba(251,146,60,.2);  background: rgba(251,146,60,.04);  }

/* Summary Table */
.stDataFrame { border-radius: 12px; overflow: hidden; }
thead th { background: #141b26 !important; color: #38bdf8 !important; font-family: 'JetBrains Mono', monospace !important; }

/* Streamlit widget overrides */
.stTabs [data-baseweb="tab-list"] {
    background: #0d1117 !important;
    border-radius: 12px !important;
    padding: .3rem !important;
    border: 1px solid rgba(56,189,248,.15) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: .78rem !important;
    border-radius: 9px !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(56,189,248,.2), rgba(129,140,248,.15)) !important;
    color: #38bdf8 !important;
    border: 1px solid rgba(56,189,248,.35) !important;
}
div[data-testid="stExpander"] {
    background: #0d1117 !important;
    border: 1px solid rgba(56,189,248,.15) !important;
    border-radius: 12px !important;
}
div[data-testid="stExpander"] summary {
    font-family: 'JetBrains Mono', monospace !important;
    color: #38bdf8 !important; font-size: .82rem !important;
}
.stDownloadButton button {
    background: linear-gradient(135deg, rgba(56,189,248,.15), rgba(129,140,248,.1)) !important;
    border: 1px solid rgba(56,189,248,.35) !important;
    color: #38bdf8 !important;
    font-family: 'JetBrains Mono', monospace !important;
    border-radius: 9px !important;
}
.stDownloadButton button:hover {
    background: linear-gradient(135deg, rgba(56,189,248,.25), rgba(129,140,248,.2)) !important;
    box-shadow: 0 0 15px rgba(56,189,248,.2) !important;
}
/* Selectbox / sidebar radio */
.stRadio > label { display: none; }

/* Legend box */
.legend-box {
    background: #141b26; border: 1px solid rgba(56,189,248,.15);
    border-radius: 12px; padding: .85rem 1rem; margin-top: 1rem;
    font-family: 'JetBrains Mono', monospace; font-size: .72rem;
}
.legend-title { color: #38bdf8; font-weight: 700; margin-bottom: .5rem; }
.legend-row { display: flex; align-items: center; gap: .5rem; padding: .18rem 0; color: #94a3b8; }

/* Sidebar title */
.sidebar-title {
    text-align: center; padding: 1rem 0 1.2rem 0;
    border-bottom: 1px solid rgba(56,189,248,.15); margin-bottom: .75rem;
}
.sidebar-icon { font-size: 2.8rem; display: block; margin-bottom: .4rem; }
.sidebar-name { font-size: .95rem; font-weight: 700; color: #38bdf8; font-family: 'JetBrains Mono', monospace; }
.sidebar-sub  { font-size: .68rem; color: #64748b; margin-top: .2rem; }

/* chip inline */
.chip-row { display: flex; flex-wrap: wrap; gap: .4rem; margin-top: .9rem; }
.chip {
    padding: .25rem .75rem; border-radius: 9999px;
    font-size: .7rem; font-weight: 600; font-family: 'JetBrains Mono', monospace;
    background: rgba(56,189,248,.08); border: 1px solid rgba(56,189,248,.25); color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# SVG MOLEKUL
# ─────────────────────────────────────────────────────────────────────
SVG = {
    "n-Heksana": """<svg viewBox="0 0 380 80" xmlns="http://www.w3.org/2000/svg" width="330" height="68">
  <line x1="20" y1="40" x2="65" y2="22" stroke="#334155" stroke-width="2"/>
  <line x1="65" y1="22" x2="115" y2="40" stroke="#334155" stroke-width="2"/>
  <line x1="115" y1="40" x2="165" y2="22" stroke="#334155" stroke-width="2"/>
  <line x1="165" y1="22" x2="215" y2="40" stroke="#334155" stroke-width="2"/>
  <line x1="215" y1="40" x2="265" y2="22" stroke="#334155" stroke-width="2"/>
  <line x1="265" y1="22" x2="315" y2="40" stroke="#334155" stroke-width="2"/>
  <text x="8" y="55" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <text x="53" y="18" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="102" y="55" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="152" y="18" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="202" y="55" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="303" y="55" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <text x="165" y="72" text-anchor="middle" fill="#6366f1" font-size="9" font-weight="bold" font-family="monospace">ALKANA — rantai lurus C₆H₁₄</text>
</svg>""",

    "Benzena": """<svg viewBox="0 0 200 190" xmlns="http://www.w3.org/2000/svg" width="170" height="160">
  <polygon points="100,22 158,57 158,127 100,162 42,127 42,57" fill="none" stroke="#334155" stroke-width="2.5"/>
  <circle cx="100" cy="92" r="33" fill="none" stroke="#f59e0b" stroke-width="2" stroke-dasharray="5,3"/>
  <text x="100" y="14" text-anchor="middle" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="165" y="61" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="165" y="133" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="100" y="177" text-anchor="middle" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="24" y="133" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="24" y="61" fill="#1e40af" font-size="11" font-weight="bold">C</text>
  <text x="100" y="96" text-anchor="middle" fill="#f59e0b" font-size="10" font-family="monospace">aromatic</text>
  <text x="100" y="108" text-anchor="middle" fill="#f59e0b" font-size="9" font-family="monospace">6π e⁻</text>
</svg>""",

    "1-Butanol": """<svg viewBox="0 0 330 100" xmlns="http://www.w3.org/2000/svg" width="300" height="90">
  <line x1="20" y1="55" x2="75" y2="35" stroke="#334155" stroke-width="2"/>
  <line x1="75" y1="35" x2="135" y2="55" stroke="#334155" stroke-width="2"/>
  <line x1="135" y1="55" x2="190" y2="35" stroke="#334155" stroke-width="2"/>
  <line x1="190" y1="35" x2="250" y2="55" stroke="#334155" stroke-width="2"/>
  <line x1="250" y1="55" x2="285" y2="28" stroke="#ef4444" stroke-width="2.5"/>
  <text x="8" y="70" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <text x="62" y="28" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="122" y="70" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="177" y="28" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="288" y="25" fill="#ef4444" font-size="11" font-weight="bold" font-family="monospace">OH</text>
  <text x="155" y="88" text-anchor="middle" fill="#0ea5e9" font-size="9" font-weight="bold" font-family="monospace">ALKOHOL PRIMER — C-OH punya 2H</text>
</svg>""",

    "2-Butanol": """<svg viewBox="0 0 310 120" xmlns="http://www.w3.org/2000/svg" width="280" height="108">
  <line x1="20" y1="70" x2="80" y2="50" stroke="#334155" stroke-width="2"/>
  <line x1="80" y1="50" x2="150" y2="70" stroke="#334155" stroke-width="2"/>
  <line x1="150" y1="70" x2="215" y2="50" stroke="#334155" stroke-width="2"/>
  <line x1="215" y1="50" x2="275" y2="70" stroke="#334155" stroke-width="2"/>
  <line x1="150" y1="70" x2="150" y2="22" stroke="#ef4444" stroke-width="2.5"/>
  <text x="8" y="84" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <text x="67" y="43" fill="#334155" font-size="11" font-family="monospace">CH</text>
  <text x="200" y="43" fill="#334155" font-size="11" font-family="monospace">CH₂</text>
  <text x="263" y="84" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <text x="140" y="16" fill="#ef4444" font-size="11" font-weight="bold" font-family="monospace">OH</text>
  <text x="150" y="104" text-anchor="middle" fill="#0ea5e9" font-size="9" font-weight="bold" font-family="monospace">ALKOHOL SEKUNDER — C-OH punya 1H</text>
</svg>""",

    "t-Butil Alkohol": """<svg viewBox="0 0 230 200" xmlns="http://www.w3.org/2000/svg" width="200" height="175">
  <circle cx="115" cy="95" r="20" fill="#6366f1"/>
  <text x="115" y="100" text-anchor="middle" fill="white" font-size="11" font-weight="bold" font-family="monospace">C</text>
  <line x1="115" y1="75" x2="115" y2="36" stroke="#334155" stroke-width="2"/>
  <text x="103" y="30" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <line x1="95" y1="95" x2="42" y2="95" stroke="#334155" stroke-width="2"/>
  <text x="10" y="99" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <line x1="135" y1="95" x2="185" y2="95" stroke="#334155" stroke-width="2"/>
  <text x="183" y="99" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <line x1="115" y1="115" x2="115" y2="155" stroke="#ef4444" stroke-width="2.5"/>
  <text x="102" y="170" fill="#ef4444" font-size="11" font-weight="bold" font-family="monospace">OH</text>
  <text x="115" y="190" text-anchor="middle" fill="#0ea5e9" font-size="9" font-weight="bold" font-family="monospace">ALKOHOL TERSIER — C-OH tanpa H</text>
</svg>""",

    "Fenol": """<svg viewBox="0 0 200 195" xmlns="http://www.w3.org/2000/svg" width="170" height="165">
  <polygon points="90,25 148,60 148,130 90,165 32,130 32,60" fill="none" stroke="#334155" stroke-width="2.5"/>
  <circle cx="90" cy="95" r="30" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="5,3"/>
  <text x="90" y="17" text-anchor="middle" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="154" y="64" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="154" y="134" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="90" y="180" text-anchor="middle" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="16" y="134" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="16" y="64" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <line x1="90" y1="25" x2="90" y2="-4" stroke="#ef4444" stroke-width="2.5"/>
  <text x="78" y="-7" fill="#ef4444" font-size="11" font-weight="bold">OH</text>
</svg>""",

    "Asetaldehid": """<svg viewBox="0 0 240 110" xmlns="http://www.w3.org/2000/svg" width="215" height="98">
  <line x1="20" y1="55" x2="100" y2="55" stroke="#334155" stroke-width="2"/>
  <line x1="100" y1="48" x2="188" y2="48" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="100" y1="62" x2="188" y2="62" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="188" y1="55" x2="215" y2="28" stroke="#64748b" stroke-width="1.5"/>
  <text x="8" y="70" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="93" y="44" fill="#6366f1" font-size="12" font-family="monospace">C</text>
  <text x="191" y="52" fill="#ef4444" font-size="14" font-weight="bold" font-family="monospace">O</text>
  <text x="218" y="25" fill="#64748b" font-size="12" font-family="monospace">H</text>
  <text x="140" y="45" fill="#ef4444" font-size="9" font-family="monospace">C=O</text>
  <text x="120" y="95" text-anchor="middle" fill="#ef4444" font-size="9" font-weight="bold" font-family="monospace">ALDEHID — CHO di ujung rantai</text>
</svg>""",

    "Benzaldehid": """<svg viewBox="0 0 320 185" xmlns="http://www.w3.org/2000/svg" width="290" height="165">
  <polygon points="90,25 142,57 142,119 90,150 38,119 38,57" fill="none" stroke="#334155" stroke-width="2.5"/>
  <circle cx="90" cy="88" r="28" fill="none" stroke="#f59e0b" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="90" y="17" text-anchor="middle" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="149" y="61" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="149" y="123" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="90" y="164" text-anchor="middle" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="21" y="123" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <text x="21" y="61" fill="#1e40af" font-size="10" font-weight="bold">C</text>
  <line x1="142" y1="88" x2="200" y2="88" stroke="#334155" stroke-width="2"/>
  <text x="200" y="84" fill="#6366f1" font-size="12" font-weight="bold" font-family="monospace">C</text>
  <line x1="200" y1="70" x2="200" y2="46" stroke="#64748b" stroke-width="1.5"/>
  <text x="194" y="42" fill="#64748b" font-size="11" font-family="monospace">H</text>
  <line x1="213" y1="81" x2="258" y2="81" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="213" y1="93" x2="258" y2="93" stroke="#ef4444" stroke-width="2.5"/>
  <text x="261" y="91" fill="#ef4444" font-size="14" font-weight="bold" font-family="monospace">O</text>
  <text x="155" y="180" text-anchor="middle" fill="#f59e0b" font-size="9" font-weight="bold" font-family="monospace">ALDEHID AROMATIK — C₆H₅CHO</text>
</svg>""",

    "Aseton": """<svg viewBox="0 0 280 105" xmlns="http://www.w3.org/2000/svg" width="255" height="94">
  <line x1="20" y1="60" x2="100" y2="60" stroke="#334155" stroke-width="2"/>
  <line x1="100" y1="53" x2="180" y2="53" stroke="#8b5cf6" stroke-width="2.5"/>
  <line x1="100" y1="67" x2="180" y2="67" stroke="#8b5cf6" stroke-width="2.5"/>
  <line x1="180" y1="60" x2="255" y2="60" stroke="#334155" stroke-width="2"/>
  <line x1="140" y1="45" x2="140" y2="15" stroke="#ef4444" stroke-width="2.5"/>
  <text x="8" y="75" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="119" y="49" fill="#6366f1" font-size="11" font-family="monospace">C=O</text>
  <text x="243" y="75" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="132" y="11" fill="#ef4444" font-size="12" font-weight="bold" font-family="monospace">O</text>
  <text x="140" y="92" text-anchor="middle" fill="#8b5cf6" font-size="9" font-weight="bold" font-family="monospace">KETON — C=O di tengah rantai</text>
</svg>""",

    "Asam Asetat": """<svg viewBox="0 0 270 115" xmlns="http://www.w3.org/2000/svg" width="245" height="103">
  <line x1="20" y1="62" x2="98" y2="62" stroke="#334155" stroke-width="2"/>
  <line x1="98" y1="55" x2="182" y2="55" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="98" y1="69" x2="182" y2="69" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="182" y1="62" x2="225" y2="28" stroke="#10b981" stroke-width="2.5"/>
  <line x1="182" y1="62" x2="228" y2="92" stroke="#ef4444" stroke-width="2"/>
  <text x="8" y="76" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="90" y="50" fill="#6366f1" font-size="11" font-family="monospace">C</text>
  <text x="228" y="25" fill="#10b981" font-size="11" font-weight="bold" font-family="monospace">OH</text>
  <text x="232" y="95" fill="#ef4444" font-size="12" font-weight="bold" font-family="monospace">O</text>
  <text x="136" y="48" fill="#ef4444" font-size="9" font-family="monospace">C=O</text>
  <text x="135" y="105" text-anchor="middle" fill="#10b981" font-size="9" font-weight="bold" font-family="monospace">GUGUS KARBOKSIL (-COOH)</text>
</svg>""",

    "Asam Oksalat": """<svg viewBox="0 0 280 115" xmlns="http://www.w3.org/2000/svg" width="255" height="103">
  <line x1="90" y1="55" x2="188" y2="55" stroke="#334155" stroke-width="2.5"/>
  <line x1="90" y1="67" x2="188" y2="67" stroke="#334155" stroke-width="2.5"/>
  <line x1="90" y1="61" x2="45" y2="27" stroke="#10b981" stroke-width="2.5"/>
  <line x1="90" y1="61" x2="40" y2="90" stroke="#ef4444" stroke-width="2"/>
  <line x1="188" y1="61" x2="234" y2="27" stroke="#10b981" stroke-width="2.5"/>
  <line x1="188" y1="61" x2="238" y2="90" stroke="#ef4444" stroke-width="2"/>
  <text x="24" y="24" fill="#10b981" font-size="11" font-weight="bold" font-family="monospace">HO</text>
  <text x="20" y="93" fill="#ef4444" font-size="12" font-weight="bold" font-family="monospace">O</text>
  <text x="82" y="49" fill="#6366f1" font-size="11" font-family="monospace">C</text>
  <text x="180" y="49" fill="#6366f1" font-size="11" font-family="monospace">C</text>
  <text x="236" y="24" fill="#10b981" font-size="11" font-weight="bold" font-family="monospace">OH</text>
  <text x="242" y="93" fill="#ef4444" font-size="12" font-weight="bold" font-family="monospace">O</text>
  <text x="140" y="105" text-anchor="middle" fill="#10b981" font-size="9" font-weight="bold" font-family="monospace">DIACID — dua gugus -COOH</text>
</svg>""",

    "Asam Oleat": """<svg viewBox="0 0 370 88" xmlns="http://www.w3.org/2000/svg" width="340" height="78">
  <text x="8" y="18" fill="#64748b" font-size="10" font-family="monospace">CH₃(CH₂)₇</text>
  <line x1="90" y1="44" x2="143" y2="26" stroke="#334155" stroke-width="2"/>
  <line x1="143" y1="26" x2="193" y2="44" stroke="#0ea5e9" stroke-width="2.5"/>
  <line x1="146" y1="20" x2="196" y2="38" stroke="#0ea5e9" stroke-width="2.5"/>
  <text x="140" y="20" fill="#0ea5e9" font-size="9" font-weight="bold" font-family="monospace">C=C</text>
  <line x1="193" y1="44" x2="248" y2="26" stroke="#334155" stroke-width="2"/>
  <text x="252" y="26" fill="#64748b" font-size="10" font-family="monospace">(CH₂)₇</text>
  <text x="300" y="40" fill="#10b981" font-size="10" font-weight="bold" font-family="monospace">COOH</text>
  <text x="175" y="72" text-anchor="middle" fill="#0ea5e9" font-size="9" font-weight="bold" font-family="monospace">ASAM LEMAK TAK JENUH (C18:1, cis)</text>
</svg>""",

    "Etil Asetat": """<svg viewBox="0 0 305 105" xmlns="http://www.w3.org/2000/svg" width="278" height="94">
  <line x1="18" y1="55" x2="88" y2="55" stroke="#334155" stroke-width="2"/>
  <line x1="88" y1="48" x2="162" y2="48" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="88" y1="62" x2="162" y2="62" stroke="#ef4444" stroke-width="2.5"/>
  <line x1="88" y1="36" x2="88" y2="14" stroke="#ef4444" stroke-width="2"/>
  <line x1="162" y1="55" x2="210" y2="55" stroke="#f59e0b" stroke-width="2.5"/>
  <line x1="210" y1="55" x2="278" y2="55" stroke="#334155" stroke-width="2"/>
  <text x="6" y="70" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="80" y="44" fill="#6366f1" font-size="11" font-family="monospace">C</text>
  <text x="80" y="11" fill="#ef4444" font-size="12" font-weight="bold" font-family="monospace">O</text>
  <text x="202" y="50" fill="#f59e0b" font-size="11" font-weight="bold" font-family="monospace">O</text>
  <text x="202" y="70" fill="#334155" font-size="11" font-family="monospace">C₂H₅</text>
  <text x="148" y="93" text-anchor="middle" fill="#f59e0b" font-size="9" font-weight="bold" font-family="monospace">ESTER — R-COO-R'</text>
</svg>""",

    "Etilamina": """<svg viewBox="0 0 250 118" xmlns="http://www.w3.org/2000/svg" width="225" height="106">
  <line x1="18" y1="62" x2="95" y2="62" stroke="#334155" stroke-width="2"/>
  <line x1="95" y1="62" x2="178" y2="62" stroke="#334155" stroke-width="2"/>
  <line x1="178" y1="62" x2="212" y2="33" stroke="#10b981" stroke-width="2.5"/>
  <line x1="178" y1="62" x2="212" y2="91" stroke="#10b981" stroke-width="2.5"/>
  <text x="6" y="76" fill="#334155" font-size="12" font-family="monospace">CH₃</text>
  <text x="82" y="76" fill="#334155" font-size="12" font-family="monospace">CH₂</text>
  <text x="170" y="58" fill="#10b981" font-size="12" font-weight="bold" font-family="monospace">N</text>
  <text x="216" y="30" fill="#10b981" font-size="12" font-family="monospace">H</text>
  <text x="216" y="95" fill="#10b981" font-size="12" font-family="monospace">H</text>
  <text x="125" y="108" text-anchor="middle" fill="#10b981" font-size="9" font-weight="bold" font-family="monospace">AMINA PRIMER (-NH₂)</text>
</svg>""",

    "Dimetilamina": """<svg viewBox="0 0 215 128" xmlns="http://www.w3.org/2000/svg" width="192" height="114">
  <circle cx="108" cy="64" r="20" fill="#10b981"/>
  <text x="108" y="69" text-anchor="middle" fill="white" font-size="12" font-weight="bold" font-family="monospace">N</text>
  <line x1="88" y1="64" x2="38" y2="38" stroke="#334155" stroke-width="2"/>
  <text x="8" y="38" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <line x1="88" y1="64" x2="38" y2="88" stroke="#334155" stroke-width="2"/>
  <text x="8" y="91" fill="#334155" font-size="11" font-family="monospace">CH₃</text>
  <line x1="128" y1="64" x2="172" y2="43" stroke="#10b981" stroke-width="2"/>
  <text x="175" y="43" fill="#10b981" font-size="12" font-weight="bold" font-family="monospace">H</text>
  <text x="108" y="115" text-anchor="middle" fill="#10b981" font-size="9" font-weight="bold" font-family="monospace">AMINA SEKUNDER (-NHR)</text>
</svg>""",

    "Trietilamina": """<svg viewBox="0 0 258 155" xmlns="http://www.w3.org/2000/svg" width="232" height="138">
  <circle cx="128" cy="78" r="20" fill="#8b5cf6"/>
  <text x="128" y="83" text-anchor="middle" fill="white" font-size="12" font-weight="bold" font-family="monospace">N</text>
  <line x1="108" y1="78" x2="52" y2="52" stroke="#334155" stroke-width="2"/>
  <text x="8" y="54" fill="#334155" font-size="11" font-family="monospace">C₂H₅</text>
  <line x1="108" y1="78" x2="48" y2="104" stroke="#334155" stroke-width="2"/>
  <text x="5" y="107" fill="#334155" font-size="11" font-family="monospace">C₂H₅</text>
  <line x1="128" y1="58" x2="128" y2="22" stroke="#334155" stroke-width="2"/>
  <text x="113" y="17" fill="#334155" font-size="11" font-family="monospace">C₂H₅</text>
  <text x="128" y="135" text-anchor="middle" fill="#8b5cf6" font-size="9" font-weight="bold" font-family="monospace">AMINA TERSIER — tanpa H pada N</text>
</svg>""",

    "Trigliserida": """<svg viewBox="0 0 375 175" xmlns="http://www.w3.org/2000/svg" width="348" height="158">
  <rect x="10" y="30" width="55" height="22" rx="5" fill="#6366f1"/>
  <rect x="10" y="76" width="55" height="22" rx="5" fill="#6366f1"/>
  <rect x="10" y="122" width="55" height="22" rx="5" fill="#6366f1"/>
  <text x="37" y="45" text-anchor="middle" fill="white" font-size="9" font-family="monospace">CH₂</text>
  <text x="37" y="91" text-anchor="middle" fill="white" font-size="9" font-family="monospace">CH</text>
  <text x="37" y="137" text-anchor="middle" fill="white" font-size="9" font-family="monospace">CH₂</text>
  <rect x="66" y="30" width="50" height="22" rx="4" fill="#ef4444"/>
  <rect x="66" y="76" width="50" height="22" rx="4" fill="#ef4444"/>
  <rect x="66" y="122" width="50" height="22" rx="4" fill="#ef4444"/>
  <text x="91" y="45" text-anchor="middle" fill="white" font-size="8" font-family="monospace">O-C=O</text>
  <text x="91" y="91" text-anchor="middle" fill="white" font-size="8" font-family="monospace">O-C=O</text>
  <text x="91" y="137" text-anchor="middle" fill="white" font-size="8" font-family="monospace">O-C=O</text>
  <line x1="116" y1="41" x2="355" y2="41" stroke="#0ea5e9" stroke-width="2"/>
  <line x1="116" y1="87" x2="355" y2="87" stroke="#0ea5e9" stroke-width="2"/>
  <line x1="116" y1="133" x2="340" y2="133" stroke="#0ea5e9" stroke-width="2"/>
  <text x="230" y="36" fill="#0ea5e9" font-size="9" font-family="monospace">R₁ — asam lemak (C14–C22)</text>
  <text x="230" y="82" fill="#0ea5e9" font-size="9" font-family="monospace">R₂ — asam lemak</text>
  <text x="230" y="128" fill="#0ea5e9" font-size="9" font-family="monospace">R₃ — asam lemak</text>
  <text x="180" y="162" text-anchor="middle" fill="#f59e0b" font-size="9" font-weight="bold" font-family="monospace">TRIESTER GLISEROL — lemak/minyak</text>
</svg>""",
}


# ─────────────────────────────────────────────────────────────────────
# DATA PERCOBAAN
# ─────────────────────────────────────────────────────────────────────
EXPERIMENTS = {
    "⚗️ P1 — Hidrokarbon": {
        "eyebrow": "Percobaan 1",
        "color": "#6366f1",
        "samples": ["Heksana", "Minyak Tanah", "Benzena"],
        "molecules": [
            {"name": "n-Heksana",    "formula": "C₆H₁₄",        "mw": "86.18 g/mol",  "bp": "69 °C",    "iupac": "n-Hexane",            "svg_key": "n-Heksana"},
            {"name": "Benzena",      "formula": "C₆H₆",          "mw": "78.11 g/mol",  "bp": "80.1 °C",  "iupac": "Benzene",             "svg_key": "Benzena"},
        ],
        "tests": [
            {
                "name": "Uji Br₂/CCl₄ (Gelap)",
                "reagent": "Br₂ dalam CCl₄",
                "reactions": [
                    {"sample": "Heksana",     "eq": "C₆H₁₄ + Br₂ → tidak bereaksi (gelap)",                                          "result": "⚪ Warna coklat TETAP — alkana tidak reaktif",                "type": "neg"},
                    {"sample": "Minyak Tanah","eq": "CₙH₂ₙ₊₂ + Br₂ → tidak bereaksi",                                               "result": "⚪ Warna coklat TETAP — komponen alkana dominan",            "type": "neg"},
                    {"sample": "Benzena",     "eq": "C₆H₆ + Br₂ → tidak bereaksi (tanpa katalis Lewis)",                             "result": "⚪ Warna tetap — cincin aromatik stabil terhadap adisi",    "type": "neg"},
                ]
            },
            {
                "name": "Uji Baeyer (KMnO₄)",
                "reagent": "KMnO₄ 0.1% (larutan ungu)",
                "reactions": [
                    {"sample": "Heksana",     "eq": "C₆H₁₄ + KMnO₄ → tidak bereaksi",                                               "result": "🟣 Tetap UNGU — alkana jenuh tidak teroksidasi",           "type": "neg"},
                    {"sample": "Minyak Tanah","eq": "CₙH₂ₙ₊₂ + KMnO₄ → tidak bereaksi",                                            "result": "🟣 Tetap UNGU — alkana dominan",                           "type": "neg"},
                    {"sample": "Benzena",     "eq": "C₆H₆ + KMnO₄ → tidak bereaksi",                                                "result": "🟣 Tetap UNGU — aromatik (6π) stabil",                    "type": "neg"},
                ]
            },
            {
                "name": "SEAr Benzena (Br₂/FeBr₃ & Nitrasi)",
                "reagent": "Br₂ + FeBr₃ katalis / HNO₃ + H₂SO₄ pekat",
                "reactions": [
                    {"sample": "Benzena + Br₂/FeBr₃",    "eq": "C₆H₆ + Br₂ → C₆H₅Br + HBr  (FeBr₃ katalis, SEAr)",                "result": "✅ Bromobenzena + asap HBr — substitusi elektrofilik",     "type": "pos"},
                    {"sample": "Benzena + HNO₃/H₂SO₄",   "eq": "C₆H₆ + HNO₃ → C₆H₅NO₂ + H₂O  (H₂SO₄ katalis)",                  "result": "✅ Nitrobenzena KUNING berminyak, bau almond",             "type": "pos"},
                ]
            },
            {
                "name": "Pembuatan & Uji Asetilena",
                "reagent": "CaC₂ + H₂O → HC≡CH; uji Br₂ & AgNO₃/NH₃",
                "reactions": [
                    {"sample": "CaC₂ + H₂O",             "eq": "CaC₂ + 2H₂O → HC≡CH↑ + Ca(OH)₂",                                  "result": "🫧 Gas HC≡CH (bau bawang), gelembung terus-menerus",      "type": "pos"},
                    {"sample": "HC≡CH + Br₂/CCl₄",       "eq": "HC≡CH + 2Br₂ → CHBr₂-CHBr₂",                                      "result": "✅ Coklat Br₂ PUDAR cepat — adisi 2 mol Br₂",            "type": "pos"},
                    {"sample": "HC≡CH + AgNO₃/NH₃",      "eq": "HC≡CH + 2[Ag(NH₃)₂]⁺ → AgC≡CAg↓ + 2NH₄⁺",                       "result": "✅ Endapan PUTIH AgC≡CAg — alkuna terminal",             "type": "pos"},
                ]
            },
        ]
    },

    "🍷 P2 — Alkohol, Fenol & Eter": {
        "eyebrow": "Percobaan 2",
        "color": "#0ea5e9",
        "samples": ["1-Butanol", "2-Butanol", "t-Butil Alkohol", "Fenol"],
        "molecules": [
            {"name": "1-Butanol",      "formula": "C₄H₉OH",      "mw": "74.12 g/mol",  "bp": "117.7 °C", "iupac": "Butan-1-ol",              "svg_key": "1-Butanol"},
            {"name": "2-Butanol",      "formula": "C₄H₉OH",      "mw": "74.12 g/mol",  "bp": "99.5 °C",  "iupac": "Butan-2-ol",              "svg_key": "2-Butanol"},
            {"name": "t-Butil Alkohol","formula": "(CH₃)₃COH",   "mw": "74.12 g/mol",  "bp": "82.2 °C",  "iupac": "2-Methylpropan-2-ol",     "svg_key": "t-Butil Alkohol"},
            {"name": "Fenol",          "formula": "C₆H₅OH",      "mw": "94.11 g/mol",  "bp": "181.7 °C", "iupac": "Phenol",                  "svg_key": "Fenol"},
        ],
        "tests": [
            {
                "name": "Pereaksi Lucas (ZnCl₂/HCl pekat)",
                "reagent": "ZnCl₂ anhidrat + HCl pekat",
                "reactions": [
                    {"sample": "1-Butanol (primer)",     "eq": "CH₃(CH₂)₃OH + HCl → CH₃(CH₂)₃Cl + H₂O  (SN2 lambat)",               "result": "⚪ Tidak keruh dalam 5 menit → PRIMER",                   "type": "neg"},
                    {"sample": "2-Butanol (sekunder)",   "eq": "CH₃CH(OH)C₂H₅ + HCl → CH₃CHClC₂H₅ + H₂O",                           "result": "🟡 Keruh dalam 5–10 menit → SEKUNDER (SN1/SN2)",          "type": "par"},
                    {"sample": "t-Butil (tersier)",      "eq": "(CH₃)₃COH + HCl → (CH₃)₃CCl + H₂O  (SN1 via karbokation tersier)",   "result": "✅ Keruh SEGERA <2 menit → TERSIER (SN1 cepat)",         "type": "pos"},
                ]
            },
            {
                "name": "Pereaksi Jones (CrO₃/H₂SO₄/Aseton)",
                "reagent": "CrO₃ dalam H₂SO₄/Aseton (oranye)",
                "reactions": [
                    {"sample": "1-Butanol",              "eq": "C₄H₉OH + CrO₃/H₂SO₄ → C₃H₇CHO → C₃H₇COOH  (Cr⁶⁺→Cr³⁺)",          "result": "✅ Oranye → HIJAU segera — primer teroksidasi",           "type": "pos"},
                    {"sample": "2-Butanol",              "eq": "CH₃CHOHC₂H₅ + CrO₃ → CH₃COC₂H₅ (MEK keton)",                        "result": "✅ Oranye → HIJAU — sekunder → keton",                   "type": "pos"},
                    {"sample": "t-Butil Alkohol",        "eq": "(CH₃)₃COH + CrO₃ → tidak bereaksi",                                   "result": "⚪ Tetap ORANYE — tersier resisten oksidasi",            "type": "neg"},
                ]
            },
            {
                "name": "Uji Iodoform (I₂/NaOH)",
                "reagent": "I₂ + NaOH berlebih (60 °C)",
                "reactions": [
                    {"sample": "2-Butanol",              "eq": "CH₃CH(OH)C₂H₅ + 3I₂ + 3NaOH → CHI₃↓ + C₂H₅COO⁻Na⁺ + 3NaI + 3H₂O","result": "✅ Endapan KUNING CHI₃ (bau antiseptik) → POSITIF",      "type": "pos"},
                    {"sample": "1-Butanol",              "eq": "CH₃(CH₂)₃OH + I₂/NaOH → tidak menghasilkan CHI₃",                    "result": "⚪ Tidak ada endapan kuning → NEGATIF",                  "type": "neg"},
                    {"sample": "t-Butil Alkohol",        "eq": "(CH₃)₃COH + I₂/NaOH → tidak menghasilkan CHI₃",                      "result": "⚪ Tidak ada endapan kuning → NEGATIF",                  "type": "neg"},
                ]
            },
            {
                "name": "Uji Fenol (FeCl₃ & Br₂/H₂O & NaOH)",
                "reagent": "FeCl₃ 1% / air brom / NaOH",
                "reactions": [
                    {"sample": "Fenol + FeCl₃",          "eq": "C₆H₅OH + FeCl₃ → [Fe(OC₆H₅)₆]³⁻ + H⁺",                             "result": "✅ Larutan UNGU/VIOLET intens → fenol positif",           "type": "pos"},
                    {"sample": "Fenol + Br₂/H₂O",        "eq": "C₆H₅OH + 3Br₂ → C₆H₂Br₃OH↓ + 3HBr (2,4,6-tribromofenol)",         "result": "✅ Endapan PUTIH — tanpa katalis, aktivasi OH kuat",     "type": "pos"},
                    {"sample": "Fenol + NaOH",            "eq": "C₆H₅OH + NaOH → C₆H₅O⁻Na⁺ + H₂O",                                  "result": "✅ Larut sempurna — fenol bersifat asam (pKa 9.95)",    "type": "pos"},
                ]
            },
            {
                "name": "Pereaksi Ceric Nitrat & Esterifikasi",
                "reagent": "Ce(NH₄)₂(NO₃)₆ / CH₃COOH + H⁺ katalis",
                "reactions": [
                    {"sample": "1-Butanol + Ce(IV)",     "eq": "Ce⁴⁺ + R-OH → [Ce-OR]³⁺ + H⁺ (kompleks)",                            "result": "✅ Oranye → MERAH — alkohol primer positif",             "type": "pos"},
                    {"sample": "t-Butil + Ce(IV)",       "eq": "Ce⁴⁺ + (CH₃)₃COH → kompleks",                                         "result": "✅ Merah (lebih lemah) — alkohol tersier positif",       "type": "pos"},
                    {"sample": "1-Butanol (ester)",      "eq": "CH₃(CH₂)₃OH + CH₃COOH → CH₃COO(CH₂)₃CH₃ + H₂O (H⁺ katalis)",      "result": "✅ AROMA buah pisang — n-butil asetat terbentuk",        "type": "pos"},
                ]
            },
        ]
    },

    "🧪 P3 — Aldehid & Keton": {
        "eyebrow": "Percobaan 3",
        "color": "#ef4444",
        "samples": ["Asetaldehid", "Benzaldehid", "Aseton"],
        "molecules": [
            {"name": "Asetaldehid",  "formula": "CH₃CHO",   "mw": "44.05 g/mol", "bp": "20.2 °C",   "iupac": "Ethanal",       "svg_key": "Asetaldehid"},
            {"name": "Benzaldehid",  "formula": "C₆H₅CHO",  "mw": "106.12 g/mol","bp": "178.1 °C",  "iupac": "Benzaldehyde",  "svg_key": "Benzaldehid"},
            {"name": "Aseton",       "formula": "CH₃COCH₃", "mw": "58.08 g/mol", "bp": "56.05 °C",  "iupac": "Propan-2-one",  "svg_key": "Aseton"},
        ],
        "tests": [
            {
                "name": "Pereaksi Tollens (Cermin Perak)",
                "reagent": "[Ag(NH₃)₂]⁺ — tabung bersih, suhu 40 °C",
                "reactions": [
                    {"sample": "Asetaldehid", "eq": "CH₃CHO + 2[Ag(NH₃)₂]⁺ + 2OH⁻ → CH₃COO⁻ + 2Ag⁰↓ + 4NH₃ + H₂O",            "result": "✅ CERMIN PERAK mengkilap di dinding tabung",            "type": "pos"},
                    {"sample": "Benzaldehid", "eq": "C₆H₅CHO + 2[Ag(NH₃)₂]⁺ + 2OH⁻ → C₆H₅COO⁻ + 2Ag⁰↓ + 4NH₃ + H₂O",         "result": "✅ CERMIN PERAK — aldehid aromatik bereaksi",           "type": "pos"},
                    {"sample": "Aseton",      "eq": "CH₃COCH₃ + Tollens → tidak bereaksi",                                         "result": "⚪ Tidak ada cermin perak → KETON NEGATIF",             "type": "neg"},
                ]
            },
            {
                "name": "Pereaksi Fehling (Cu²⁺ → Cu₂O)",
                "reagent": "Fehling A (CuSO₄) + Fehling B (NaOH+tartrat), didihkan",
                "reactions": [
                    {"sample": "Asetaldehid", "eq": "CH₃CHO + 2Cu²⁺ + 5OH⁻ → CH₃COO⁻ + Cu₂O↓ + 3H₂O",                          "result": "✅ Endapan MERAH BATA Cu₂O — aldehid alifatik positif",  "type": "pos"},
                    {"sample": "Benzaldehid", "eq": "C₆H₅CHO + Fehling → tidak bereaksi (aldehid aromatik)",                      "result": "⚪ Tidak ada Cu₂O — aldehid aromatik NEGATIF",          "type": "neg"},
                    {"sample": "Aseton",      "eq": "CH₃COCH₃ + Fehling → tidak bereaksi",                                        "result": "⚪ Tidak ada perubahan → KETON NEGATIF",                "type": "neg"},
                ]
            },
            {
                "name": "Pereaksi Schiff (Fuchsin/SO₂)",
                "reagent": "Reagen Schiff tidak berwarna",
                "reactions": [
                    {"sample": "Asetaldehid", "eq": "CH₃CHO + [Schiff] → kompleks merah-violet",                                   "result": "✅ Merah-VIOLET — aldehid positif Schiff",              "type": "pos"},
                    {"sample": "Benzaldehid", "eq": "C₆H₅CHO + [Schiff] → kompleks merah-violet",                                  "result": "✅ Merah-VIOLET — aldehid aromatik positif",            "type": "pos"},
                    {"sample": "Aseton",      "eq": "CH₃COCH₃ + [Schiff] → tidak bereaksi",                                       "result": "⚪ Tidak berwarna → KETON NEGATIF",                     "type": "neg"},
                ]
            },
            {
                "name": "Na-Bisulfit & Pembentukan Asetal",
                "reagent": "NaHSO₃ jenuh / ROH + H⁺ katalis",
                "reactions": [
                    {"sample": "Asetaldehid + NaHSO₃",  "eq": "CH₃CHO + NaHSO₃ → CH₃CH(OH)SO₃Na↓",                              "result": "✅ Endapan PUTIH kristal — adisi nukleofilik bisulfit",  "type": "pos"},
                    {"sample": "Benzaldehid + NaHSO₃",  "eq": "C₆H₅CHO + NaHSO₃ → C₆H₅CH(OH)SO₃Na↓",                           "result": "✅ Endapan PUTIH — benzaldehid positif bisulfit",       "type": "pos"},
                    {"sample": "Aseton + NaHSO₃",       "eq": "CH₃COCH₃ + NaHSO₃ → (CH₃)₂C(OH)SO₃Na↓ (lambat)",                "result": "🟡 Endapan PUTIH lebih lambat — sterik lebih besar",   "type": "par"},
                    {"sample": "Asetaldehid → Asetal",  "eq": "CH₃CHO + 2CH₃OH → CH₃CH(OCH₃)₂ + H₂O  (H⁺ katalis, asetal)",   "result": "✅ Asetal terbentuk — NEGATIF Tollens (terlindungi)",  "type": "pos"},
                ]
            },
        ]
    },

    "🌿 P4 — Asam Karboksilat": {
        "eyebrow": "Percobaan 4",
        "color": "#10b981",
        "samples": ["Asam Asetat","Asam Oksalat","Asam Oleat","Etil Asetat","Anhidrida Ftalat"],
        "molecules": [
            {"name": "Asam Asetat",   "formula": "CH₃COOH",        "mw": "60.05 g/mol",  "bp": "117.9 °C",  "iupac": "Acetic Acid",      "svg_key": "Asam Asetat"},
            {"name": "Asam Oksalat",  "formula": "HOOCCOOH",       "mw": "90.03 g/mol",  "bp": "189 °C",    "iupac": "Oxalic Acid",      "svg_key": "Asam Oksalat"},
            {"name": "Asam Oleat",    "formula": "C₁₇H₃₃COOH",    "mw": "282.46 g/mol", "bp": "360 °C",    "iupac": "cis-9-Octadecenoic","svg_key": "Asam Oleat"},
            {"name": "Etil Asetat",   "formula": "CH₃COOC₂H₅",    "mw": "88.11 g/mol",  "bp": "77.1 °C",   "iupac": "Ethyl Acetate",    "svg_key": "Etil Asetat"},
        ],
        "tests": [
            {
                "name": "Uji Kelarutan Asam Karboksilat",
                "reagent": "Air / heksana / NaOH",
                "reactions": [
                    {"sample": "Asam Asetat + H₂O",   "eq": "CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺  (Ka=1.8×10⁻⁵)",                   "result": "✅ LARUT SEMPURNA — miscible, ionisasi parsial",          "type": "pos"},
                    {"sample": "Asam Oksalat + H₂O",  "eq": "HOOCCOOH + H₂O ⇌ -OOCCOOH + H₃O⁺",                                  "result": "✅ LARUT — diacid hidrofilik (90 g/L @ 25°C)",           "type": "pos"},
                    {"sample": "Asam Oleat + H₂O",    "eq": "C₁₈H₃₄O₂ + H₂O → tidak larut",                                      "result": "⚪ DUA LAPISAN — rantai C18 sangat hidrofobik",          "type": "neg"},
                    {"sample": "Etil Asetat + H₂O",   "eq": "CH₃COOC₂H₅ + H₂O → larut parsial (8.3g/100mL)",                     "result": "🟡 Sedikit larut — campuran dua fase pada konsentrasi tinggi","type": "par"},
                ]
            },
            {
                "name": "Reaksi Penggaraman & Saponifikasi",
                "reagent": "NaOH 10% / KOH + pemanasan",
                "reactions": [
                    {"sample": "Asam Asetat + NaOH",  "eq": "CH₃COOH + NaOH → CH₃COO⁻Na⁺ + H₂O",                                "result": "✅ Netralisasi — bau cuka hilang, pH basa",               "type": "pos"},
                    {"sample": "Asam Oksalat + NaOH", "eq": "HOOCCOOH + 2NaOH → NaOOCCOONa + 2H₂O",                              "result": "✅ Garam dinatrium oksalat — larut, pH basa",             "type": "pos"},
                    {"sample": "Asam Oleat + NaOH",   "eq": "C₁₇H₃₃COOH + NaOH → C₁₇H₃₃COO⁻Na⁺ + H₂O",                        "result": "✅ Sabun sodium oleat berbusa — penyabunan asam lemak",  "type": "pos"},
                    {"sample": "Etil Asetat + NaOH",  "eq": "CH₃COOC₂H₅ + NaOH → CH₃COO⁻Na⁺ + C₂H₅OH",                        "result": "✅ Saponifikasi — lapisan ester hilang, homogen",        "type": "pos"},
                ]
            },
            {
                "name": "Reaksi Oksidasi (KMnO₄)",
                "reagent": "KMnO₄ dalam H₂SO₄ encer",
                "reactions": [
                    {"sample": "Asam Oksalat",        "eq": "5HOOCCOOH + 2KMnO₄ + 3H₂SO₄ → 10CO₂↑ + 2MnSO₄ + K₂SO₄ + 8H₂O",  "result": "✅ KMnO₄ ungu → TAK BERWARNA — oksidasi sempurna",      "type": "pos"},
                    {"sample": "Asam Oleat",           "eq": "-CH=CH- + KMnO₄ → diol/asam pendek + MnO₂↓",                       "result": "✅ Ungu pudar + endapan coklat MnO₂",                   "type": "pos"},
                    {"sample": "Asam Asetat",          "eq": "CH₃COOH + KMnO₄ → tidak bereaksi (jenuh)",                         "result": "⚪ Tetap UNGU — asam jenuh stabil",                     "type": "neg"},
                ]
            },
            {
                "name": "Identifikasi Ester & Anhidrida",
                "reagent": "NH₂OH/FeCl₃ (uji hidroxamat) / H₂O",
                "reactions": [
                    {"sample": "Etil Asetat + NH₂OH/FeCl₃","eq": "CH₃COOC₂H₅ + NH₂OH → CH₃CONHOH + C₂H₅OH → (+FeCl₃) → merah", "result": "✅ Larutan MERAH/UNGU — ester positif hidroxamat",       "type": "pos"},
                    {"sample": "Anh. Ftalat + H₂O",        "eq": "C₆H₄(CO)₂O + H₂O → C₆H₄(COOH)₂ (asam ftalat)",               "result": "✅ Endapan PUTIH asam ftalat — anhidrida terhidrolisis", "type": "pos"},
                ]
            },
        ]
    },

    "🔵 P5 — Amina & Derivatnya": {
        "eyebrow": "Percobaan 5",
        "color": "#8b5cf6",
        "samples": ["Etilamina", "Dimetilamina", "Trietilamina"],
        "molecules": [
            {"name": "Etilamina",    "formula": "CH₃CH₂NH₂",  "mw": "45.08 g/mol",  "bp": "16.6 °C",  "iupac": "Ethanamine",    "svg_key": "Etilamina"},
            {"name": "Dimetilamina", "formula": "(CH₃)₂NH",   "mw": "45.08 g/mol",  "bp": "7.4 °C",   "iupac": "Dimethylamine", "svg_key": "Dimetilamina"},
            {"name": "Trietilamina", "formula": "(C₂H₅)₃N",  "mw": "101.19 g/mol", "bp": "89.7 °C",  "iupac": "Triethylamine", "svg_key": "Trietilamina"},
        ],
        "tests": [
            {
                "name": "Uji Kelarutan & Kebasaan (pH)",
                "reagent": "Air suling + indikator universal",
                "reactions": [
                    {"sample": "Etilamina",    "eq": "CH₃CH₂NH₂ + H₂O ⇌ CH₃CH₂NH₃⁺ + OH⁻  (Kb=5.4×10⁻⁴)",                      "result": "✅ pH > 7, bau amis menyengat — AMINA PRIMER",          "type": "pos"},
                    {"sample": "Dimetilamina", "eq": "(CH₃)₂NH + H₂O ⇌ (CH₃)₂NH₂⁺ + OH⁻  (Kb=5.9×10⁻⁴)",                       "result": "✅ pH > 7, basa lebih kuat dari primer",                "type": "pos"},
                    {"sample": "Trietilamina", "eq": "(C₂H₅)₃N + H₂O ⇌ (C₂H₅)₃NH⁺ + OH⁻",                                      "result": "✅ pH > 7, basa (sedikit lebih lemah-sterik)",          "type": "pos"},
                ]
            },
            {
                "name": "Uji Hinsberg (C₆H₅SO₂Cl)",
                "reagent": "Benzenasulfonil klorida + NaOH aq.",
                "reactions": [
                    {"sample": "Etilamina (primer)",    "eq": "C₂H₅NH₂ + C₆H₅SO₂Cl → C₆H₅SO₂NHC₂H₅ + HCl  (larut NaOH)",      "result": "✅ Sulfonamid LARUT NaOH — AMINA PRIMER",              "type": "pos"},
                    {"sample": "Dimetilamina (sekunder)","eq": "(CH₃)₂NH + C₆H₅SO₂Cl → C₆H₅SO₂N(CH₃)₂ + HCl  (tidak larut NaOH)","result": "🟡 Endapan TIDAK larut NaOH — AMINA SEKUNDER",      "type": "par"},
                    {"sample": "Trietilamina (tersier)", "eq": "(C₂H₅)₃N + C₆H₅SO₂Cl → tidak bereaksi",                           "result": "⚪ Tidak ada sulfonamid — AMINA TERSIER",              "type": "neg"},
                ]
            },
            {
                "name": "Diazotisasi & Kopling Azo",
                "reagent": "NaNO₂ + HCl (0–5 °C) → kopling β-naftol",
                "reactions": [
                    {"sample": "Anilina (ref. aromatik)", "eq": "C₆H₅NH₂ + NaNO₂ + 2HCl → C₆H₅N₂⁺Cl⁻ + NaCl + 2H₂O  (0-5°C)", "result": "✅ Garam diazonium stabil — tidak berwarna di 0-5 °C", "type": "pos"},
                    {"sample": "Diazonium + β-naftol",    "eq": "C₆H₅N₂⁺ + C₁₀H₇OH → C₆H₅-N=N-C₁₀H₆OH + H⁺",                  "result": "✅ PEWARNA AZO MERAH/ORANYE terbentuk",                "type": "pos"},
                    {"sample": "Etilamina (alifatik)",    "eq": "C₂H₅NH₂ + NaNO₂ + HCl → C₂H₅OH + N₂↑ + NaCl + H₂O",          "result": "🫧 Gas N₂ gelembung — diazonium alifatik tidak stabil","type": "par"},
                ]
            },
        ]
    },

    "🫙 P6 — Lemak & Minyak": {
        "eyebrow": "Percobaan 6",
        "color": "#f59e0b",
        "samples": ["Margarin","Mentega","Minyak Sawit","Minyak Kedelai","Minyak Tengik"],
        "molecules": [
            {"name": "Trigliserida (Umum)", "formula": "C₃H₅(OOCR)₃", "mw": "~885 g/mol", "bp": ">300 °C", "iupac": "Triglyceride", "svg_key": "Trigliserida"},
        ],
        "tests": [
            {
                "name": "Uji Kelarutan Lemak/Minyak",
                "reagent": "Air / heksana / kloroform",
                "reactions": [
                    {"sample": "Semua sampel + H₂O",    "eq": "Trigliserida + H₂O → tidak larut (nonpolar vs polar)",               "result": "⚪ DUA LAPISAN, minyak mengapung — hidrofobik",         "type": "neg"},
                    {"sample": "Semua sampel + heksana", "eq": "Trigliserida + C₆H₁₄ → larut (like dissolves like)",                "result": "✅ LARUT SEMPURNA — nonpolar dalam nonpolar",           "type": "pos"},
                ]
            },
            {
                "name": "Reaksi Saponifikasi (NaOH/KOH)",
                "reagent": "NaOH 30% + pemanasan 30 menit",
                "reactions": [
                    {"sample": "Minyak Sawit",    "eq": "(C₁₅H₃₁COO)₃C₃H₅ + 3NaOH → 3C₁₅H₃₁COO⁻Na⁺ + C₃H₅(OH)₃",             "result": "✅ Sabun sodium palmitat + gliserol, berbusa lebat",     "type": "pos"},
                    {"sample": "Minyak Kedelai",  "eq": "(RCO₂)₃C₃H₅ + 3NaOH → 3RCOONa + C₃H₅(OH)₃  (R=C₁₇:₂/C₁₇:₃)",       "result": "✅ Sabun linoleat/linolenat + gliserol",                "type": "pos"},
                    {"sample": "Mentega",         "eq": "Trigliserida susu + NaOH → sabun campuran + gliserol",                    "result": "✅ Sabun lunak berbusa, bau mentega hilang",            "type": "pos"},
                    {"sample": "Margarin",        "eq": "Trigliserida terhidrogenasi + KOH → sabun kalium (lunak)",               "result": "✅ Sabun kalium berbusa lebih lebat",                   "type": "pos"},
                ]
            },
            {
                "name": "Uji Ketidakjenuhan (Br₂/KMnO₄)",
                "reagent": "Br₂ dalam CCl₄ atau KMnO₄ 0.1%",
                "reactions": [
                    {"sample": "Minyak Kedelai", "eq": "-CH=CH- (linoleat C18:2) + Br₂ → -CHBr-CHBr-  (adisi)",                  "result": "✅ Br₂ CEPAT PUDAR — banyak C=C (C18:2, C18:3)",       "type": "pos"},
                    {"sample": "Minyak Sawit",   "eq": "-CH=CH- (oleat C18:1) + Br₂ → -CHBr-CHBr-",                             "result": "🟡 Br₂ pudar LAMBAT — palmitat C16:0 dominan",         "type": "par"},
                    {"sample": "Mentega",        "eq": "Asam lemak jenuh dominan + Br₂ → tidak bereaksi",                        "result": "⚪ Br₂ sangat sedikit pudar — jenuh dominan",           "type": "neg"},
                    {"sample": "Margarin",       "eq": "Asam jenuh (terhidrogenasi) + Br₂ → sedikit bereaksi",                   "result": "⚪ Sedikit pudar — proses hidrogenasi menjenuhkan",     "type": "neg"},
                ]
            },
            {
                "name": "Uji Ketengikan (Kreiss & NaHSO₃)",
                "reagent": "Phloroglucinol/HCl pekat / NaHSO₃ jenuh",
                "reactions": [
                    {"sample": "Minyak Tengik (Kreiss)", "eq": "-CH=CH- + O₂ → ROOH (peroksida) → R-CHO + R'-CHO (aldehid)",     "result": "✅ MERAH/PINK — epihidrin aldehid positif",             "type": "pos"},
                    {"sample": "Minyak Tengik + NaHSO₃", "eq": "RCHO + NaHSO₃ → RCH(OH)SO₃Na↓",                                 "result": "✅ Endapan adduct — aldehid ketengikan terdeteksi",     "type": "pos"},
                    {"sample": "Minyak Segar + Kreiss",  "eq": "Trigliserida segar + phloroglucinol → sedikit bereaksi",          "result": "⚪ Kuning pucat — segar, oksidasi minimal",             "type": "neg"},
                ]
            },
        ]
    },
}


# ─────────────────────────────────────────────────────────────────────
# HELPER RENDER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────
TYPE_META = {
    "pos": ("pos", "POSITIF", "#34d399"),
    "neg": ("neg", "NEGATIF", "#f87171"),
    "par": ("par", "PARSIAL",  "#fb923c"),
}

def render_reaction_card(rxn: dict):
    cls, label, color = TYPE_META[rxn["type"]]
    st.markdown(f"""
    <div class="rxn-card {cls}">
        <div class="rxn-top">
            <span class="rxn-sample-txt">{rxn['sample']}</span>
            <span class="rxn-badge {cls}">{label}</span>
        </div>
        <div class="rxn-eq">⚗ {rxn['eq']}</div>
        <div class="rxn-result {cls}">📋 {rxn['result']}</div>
    </div>
    """, unsafe_allow_html=True)


def render_molecule_card(mol: dict):
    svg_html = SVG.get(mol["svg_key"], "<p style='color:#64748b'>Struktur tidak tersedia</p>")
    st.markdown(f"""
    <div class="mol-card">
        <div class="mol-name">{mol['name']}</div>
        <div class="mol-svg-wrap">{svg_html}</div>
        <div>
            <span class="mol-badge">{mol['formula']}</span>
            <span class="mol-badge">MW: {mol['mw']}</span>
            <span class="mol-badge">bp: {mol['bp']}</span>
        </div>
        <div class="mol-iupac">IUPAC: {mol['iupac']}</div>
    </div>
    """, unsafe_allow_html=True)


def build_dataframe(exp: dict) -> pd.DataFrame:
    rows = []
    for test in exp["tests"]:
        for rxn in test["reactions"]:
            status = {"pos": "✅ Positif", "neg": "⚪ Negatif", "par": "🟡 Parsial"}[rxn["type"]]
            rows.append({
                "Uji / Pereaksi":         test["name"],
                "Sampel":                 rxn["sample"],
                "Persamaan Reaksi":       rxn["eq"],
                "Hasil Pengamatan":       rxn["result"],
                "Status":                 status,
            })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-title">
        <span class="sidebar-icon">⚗️</span>
        <div class="sidebar-name">KIMIA ORGANIK</div>
        <div class="sidebar-sub">Laboratorium Interaktif</div>
    </div>
    """, unsafe_allow_html=True)

    selected = st.radio(
        "Pilih Percobaan",
        list(EXPERIMENTS.keys()),
        label_visibility="collapsed",
    )

    st.markdown("""
    <div class="legend-box">
        <div class="legend-title">// LEGENDA HASIL</div>
        <div class="legend-row"><span style="color:#34d399">✅</span> Positif / Bereaksi</div>
        <div class="legend-row"><span style="color:#fb923c">🟡</span> Parsial / Lambat</div>
        <div class="legend-row"><span style="color:#f87171">⚪</span> Negatif / Tidak bereaksi</div>
        <div class="legend-row"><span style="color:#38bdf8">🫧</span> Gas / Gelembung</div>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────
# MAIN CONTENT
# ─────────────────────────────────────────────────────────────────────
exp = EXPERIMENTS[selected]

# ── HERO ──
samples_str = " · ".join(exp["samples"])
chips_html  = "".join(f'<span class="chip">{s}</span>' for s in exp["samples"])
st.markdown(f"""
<div class="hero-box">
    <div class="hero-eyebrow">// {exp['eyebrow']} · Kimia Organik</div>
    <div class="hero-title">{selected}</div>
    <div class="hero-sub">sampel: {samples_str}</div>
    <div class="chip-row">{chips_html}</div>
</div>
""", unsafe_allow_html=True)

# ── METRICS ──
total_rxn = sum(len(t["reactions"]) for t in exp["tests"])
positives  = sum(1 for t in exp["tests"] for r in t["reactions"] if r["type"] == "pos")
partials   = sum(1 for t in exp["tests"] for r in t["reactions"] if r["type"] == "par")
negatives  = sum(1 for t in exp["tests"] for r in t["reactions"] if r["type"] == "neg")

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
        <div class="metric-val">{total_rxn}</div>
        <div class="metric-lbl">Total Reaksi</div>
    </div>
    <div class="metric-card">
        <div class="metric-val" style="color:#34d399">{positives}</div>
        <div class="metric-lbl">Hasil Positif</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── TABS ──
tab_struct, tab_rxn, tab_tabel = st.tabs([
    "🔬 Struktur Kimia",
    "⚗️ Reaksi & Hasil",
    "📊 Tabel Ringkasan",
])

# ── TAB 1: STRUKTUR ──
with tab_struct:
    st.markdown('<div class="sec-head">// STRUKTUR MOLEKUL SAMPEL</div>', unsafe_allow_html=True)
    mols = exp["molecules"]
    cols_per_row = min(len(mols), 3)
    for row_start in range(0, len(mols), cols_per_row):
        row_mols = mols[row_start: row_start + cols_per_row]
        cols = st.columns(len(row_mols))
        for col, mol in zip(cols, row_mols):
            with col:
                render_molecule_card(mol)

# ── TAB 2: REAKSI ──
with tab_rxn:
    st.markdown('<div class="sec-head">// UJI KIMIA & HASIL REAKSI</div>', unsafe_allow_html=True)
    for test in exp["tests"]:
        n = len(test["reactions"])
        with st.expander(f"🧬 {test['name']}  ·  {n} reaksi", expanded=True):
            st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace;font-size:.72rem;color:#64748b;
                        margin-bottom:.75rem;padding:.4rem .6rem;background:rgba(56,189,248,.04);
                        border-radius:7px;border-left:2px solid rgba(56,189,248,.3);">
                Pereaksi: {test['reagent']}
            </div>
            """, unsafe_allow_html=True)
            for rxn in test["reactions"]:
                render_reaction_card(rxn)

# ── TAB 3: TABEL ──
with tab_tabel:
    st.markdown('<div class="sec-head">// TABEL RINGKASAN SEMUA REAKSI</div>', unsafe_allow_html=True)
    df = build_dataframe(exp)

    st.dataframe(
        df,
        use_container_width=True,
        height=520,
        column_config={
            "Uji / Pereaksi":   st.column_config.TextColumn("Uji / Pereaksi",   width="medium"),
            "Sampel":           st.column_config.TextColumn("Sampel",           width="medium"),
            "Persamaan Reaksi": st.column_config.TextColumn("Persamaan Reaksi", width="large"),
            "Hasil Pengamatan": st.column_config.TextColumn("Hasil Pengamatan", width="large"),
            "Status":           st.column_config.TextColumn("Status",           width="small"),
        },
    )

    csv_bytes = df.to_csv(index=False).encode("utf-8")
    fname = selected.replace(" ", "_").replace("/","").replace("—","")[:30] + ".csv"
    st.download_button(
        label="⬇️ Download Tabel CSV",
        data=csv_bytes,
        file_name=fname,
        mime="text/csv",
    )

# ── FOOTER ──
st.markdown("""
<div style="text-align:center;padding:2rem 0 .5rem 0;
            color:#1e293b;font-family:'JetBrains Mono',monospace;font-size:.72rem;
            border-top:1px solid rgba(56,189,248,.08);margin-top:2.5rem;">
    ⚗️ Laboratorium Kimia Organik · Aplikasi Praktikum Interaktif · 2025
</div>
""", unsafe_allow_html=True)
