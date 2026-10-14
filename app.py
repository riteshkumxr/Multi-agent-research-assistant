# app.py

import streamlit as st
import os
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from graph import app

# --- Page Configuration ---
st.set_page_config(
    page_title="Nexus Research | Multi-Agent AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Theme State Management (Default to Dark Mode) ---
if "theme" not in st.session_state:
    st.session_state["theme"] = "dark"

is_dark = st.session_state["theme"] == "dark"

# --- Dedicated CSS per Theme ---
if is_dark:
    theme_css = """
    /* ==================== DARK THEME ==================== */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #0b0f19 !important;
        color: #f1f5f9 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    [data-testid="stSidebar"] * {
        color: #e2e8f0 !important;
    }
    [data-testid="stHeader"] {
        background-color: rgba(11, 15, 25, 0.85) !important;
        backdrop-filter: blur(12px) !important;
    }
    .hero-container {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.18) 0%, rgba(168, 85, 247, 0.15) 50%, rgba(6, 182, 212, 0.15) 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.35) !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4) !important;
    }
    .hero-subtitle { color: #94a3b8 !important; }
    .agent-card {
        background: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    .agent-card:hover { border-color: rgba(99, 102, 241, 0.6) !important; }
    .agent-card-name { color: #f8fafc !important; }
    .agent-card-desc { color: #94a3b8 !important; }
    .step-card {
        background: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-left: 4px solid #6366f1 !important;
    }
    .report-box {
        background: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        color: #f1f5f9 !important;
    }
    .stat-card {
        background: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }
    .stat-label { color: #94a3b8 !important; }
    .source-card {
        background: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        color: #f1f5f9 !important;
    }
    
    /* Buttons in Dark Mode */
    div.stButton > button {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }
    div.stButton > button:hover {
        background-color: #334155 !important;
        border-color: #6366f1 !important;
        color: #ffffff !important;
    }
    
    /* Inputs in Dark Mode */
    .stTextInput input, .stTextArea textarea {
        background-color: #1e293b !important;
        color: #f8fafc !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
    }

    /* Expanders in Dark Mode */
    [data-testid="stExpander"] {
        background-color: #111827 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    [data-testid="stExpander"] summary {
        color: #e2e8f0 !important;
    }
    [data-testid="stExpander"] p {
        color: #cbd5e1 !important;
    }

    /* Tabs in Dark Mode */
    button[data-baseweb="tab"] {
        color: #94a3b8 !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #818cf8 !important;
        border-bottom-color: #818cf8 !important;
    }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #f1f5f9;
    }
    """
else:
    theme_css = """
    /* ==================== LIGHT THEME ==================== */
    .stApp, [data-testid="stAppViewContainer"] {
        background-color: #f8fafc !important;
        color: #0f172a !important;
    }
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
        border-right: 1px solid #e2e8f0 !important;
    }
    [data-testid="stSidebar"] * {
        color: #1e293b !important;
    }
    [data-testid="stHeader"] {
        background-color: rgba(248, 250, 252, 0.85) !important;
        backdrop-filter: blur(12px) !important;
    }
    .hero-container {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(168, 85, 247, 0.08) 50%, rgba(6, 182, 212, 0.08) 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.08) !important;
    }
    .hero-subtitle { color: #475569 !important; }
    .agent-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04) !important;
    }
    .agent-card:hover { border-color: #6366f1 !important; }
    .agent-card-name { color: #0f172a !important; }
    .agent-card-desc { color: #64748b !important; }
    .step-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-left: 4px solid #6366f1 !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03) !important;
    }
    .report-box {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        color: #0f172a !important;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05) !important;
    }
    .stat-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.03) !important;
    }
    .stat-label { color: #64748b !important; }
    .source-card {
        background: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        color: #0f172a !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
    }

    /* Buttons in Light Mode */
    div.stButton > button {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05) !important;
    }
    div.stButton > button:hover {
        background-color: #e2e8f0 !important;
        border-color: #6366f1 !important;
        color: #0f172a !important;
    }

    /* Inputs in Light Mode */
    .stTextInput input, .stTextArea textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #6366f1 !important;
    }

    /* Expanders in Light Mode */
    [data-testid="stExpander"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02) !important;
    }
    [data-testid="stExpander"] summary {
        color: #0f172a !important;
    }
    [data-testid="stExpander"] p {
        color: #334155 !important;
    }

    /* Tabs in Light Mode */
    button[data-baseweb="tab"] {
        color: #64748b !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        color: #6366f1 !important;
        border-bottom-color: #6366f1 !important;
    }
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {
        color: #0f172a;
    }
    """

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Plus Jakarta Sans', sans-serif;
    }}

    {theme_css}

    /* Primary Start Button (Consistent in both modes) */
    div.stButton > button[kind="primary"], button[data-testid="baseButton-primary"] {{
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: #ffffff !important;
        border: none !important;
        font-weight: 700 !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
    }}
    div.stButton > button[kind="primary"]:hover, button[data-testid="baseButton-primary"]:hover {{
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        transform: translateY(-1px) !important;
    }}

    /* Hero Banner */
    .hero-container {{
        border-radius: 20px;
        padding: 30px 34px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }}
    
    .hero-badge {{
        display: inline-block;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: #ffffff !important;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        padding: 6px 14px;
        border-radius: 9999px;
        margin-bottom: 12px;
    }}

    .hero-title {{
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #a855f7 50%, #06b6d4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
        line-height: 1.2;
    }}

    .hero-subtitle {{
        font-size: 1.02rem;
        max-width: 780px;
        line-height: 1.6;
        margin: 0;
    }}

    /* Agent Showcase Cards */
    .agent-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 14px;
        margin: 18px 0 26px 0;
    }}

    .agent-card {{
        border-radius: 14px;
        padding: 18px 20px;
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }}

    .agent-card:hover {{
        transform: translateY(-2px);
    }}

    .agent-card-icon {{
        font-size: 1.6rem;
        margin-bottom: 8px;
    }}

    .agent-card-name {{
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 4px;
    }}

    .agent-card-desc {{
        font-size: 0.82rem;
        line-height: 1.4;
    }}

    /* Activity Step Card */
    .step-card {{
        border-radius: 14px;
        padding: 16px 20px;
        margin-bottom: 14px;
    }}

    .step-badge {{
        font-size: 0.75rem;
        font-weight: 700;
        padding: 4px 12px;
        border-radius: 8px;
        display: inline-block;
        margin-bottom: 8px;
        letter-spacing: 0.05em;
    }}

    .supervisor-badge {{ background: rgba(139, 92, 246, 0.18); color: #c084fc; border: 1px solid rgba(139, 92, 246, 0.35); }}
    .researcher-badge {{ background: rgba(6, 182, 212, 0.18); color: #38bdf8; border: 1px solid rgba(6, 182, 212, 0.35); }}
    .writer-badge     {{ background: rgba(16, 185, 129, 0.18); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.35); }}
    .critiquer-badge  {{ background: rgba(245, 158, 11, 0.18); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.35); }}

    /* Report Box */
    .report-box {{
        border-radius: 16px;
        padding: 32px;
        line-height: 1.7;
    }}

    /* Metric Cards */
    .stat-card {{
        border-radius: 12px;
        padding: 18px;
        text-align: center;
    }}

    .stat-number {{
        font-size: 1.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #06b6d4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }}

    .stat-label {{
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-top: 4px;
    }}

    /* Source Card */
    .source-card {{
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }}

    /* General Buttons */
    div.stButton > button {{
        border-radius: 10px;
        font-weight: 600;
        padding: 8px 18px;
        transition: all 0.2s ease-in-out;
    }}
</style>
""", unsafe_allow_html=True)


# --- Top Bar with Theme Toggle Icon ---
top_col1, top_col2 = st.columns([5, 1.5])
with top_col1:
    st.caption("🚀 Nexus Autonomous Multi-Agent Framework • v2.0")
with top_col2:
    if is_dark:
        if st.button("☀️ Light Mode", key="top_toggle_light", use_container_width=True, help="Switch to clean light mode"):
            st.session_state["theme"] = "light"
            st.rerun()
    else:
        if st.button("🌙 Dark Mode", key="top_toggle_dark", use_container_width=True, help="Switch to sleek dark mode"):
            st.session_state["theme"] = "dark"
            st.rerun()


# --- API Key Validation & Sidebar Setup ---
def check_api_keys():
    """Verify presence of API keys with interactive sidebar entry."""
    together_key = os.environ.get("TOGETHER_API_KEY", "").strip()
    tavily_key = os.environ.get("TAVILY_API_KEY", "").strip()

    with st.sidebar:
        # Theme switcher in sidebar
        st.markdown("### 🎨 Appearance")
        if is_dark:
            if st.button("☀️ Switch to Light Mode", key="sb_toggle_light", use_container_width=True):
                st.session_state["theme"] = "light"
                st.rerun()
        else:
            if st.button("🌙 Switch to Dark Mode", key="sb_toggle_dark", use_container_width=True):
                st.session_state["theme"] = "dark"
                st.rerun()

        st.markdown("---")
        st.markdown("### 🔑 API Connections")
        
        # Self-contained, highly legible status cards (no black-on-black)
        box_bg = "#1f2937" if is_dark else "#f1f5f9"
        border_c = "rgba(255,255,255,0.1)" if is_dark else "#cbd5e1"
        txt_c = "#f1f5f9" if is_dark else "#0f172a"
        
        # Together AI card
        if together_key:
            st.markdown(f"""
            <div style="background:{box_bg}; border:1px solid {border_c}; border-radius:10px; padding:10px 14px; margin-bottom:8px; display:flex; align-items:center; justify-content:space-between;">
                <span style="font-weight:600; font-size:0.88rem; color:{txt_c};">Together AI</span>
                <span style="background:rgba(16,185,129,0.2); color:#10b981; font-size:0.75rem; font-weight:700; padding:3px 8px; border-radius:6px;">CONNECTED</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:{box_bg}; border:1px solid {border_c}; border-radius:10px; padding:10px 14px; margin-bottom:8px; display:flex; align-items:center; justify-content:space-between;">
                <span style="font-weight:600; font-size:0.88rem; color:{txt_c};">Together AI</span>
                <span style="background:rgba(239,68,68,0.2); color:#ef4444; font-size:0.75rem; font-weight:700; padding:3px 8px; border-radius:6px;">MISSING</span>
            </div>
            """, unsafe_allow_html=True)

        # Tavily card
        if tavily_key:
            st.markdown(f"""
            <div style="background:{box_bg}; border:1px solid {border_c}; border-radius:10px; padding:10px 14px; margin-bottom:12px; display:flex; align-items:center; justify-content:space-between;">
                <span style="font-weight:600; font-size:0.88rem; color:{txt_c};">Tavily Search</span>
                <span style="background:rgba(16,185,129,0.2); color:#10b981; font-size:0.75rem; font-weight:700; padding:3px 8px; border-radius:6px;">CONNECTED</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background:{box_bg}; border:1px solid {border_c}; border-radius:10px; padding:10px 14px; margin-bottom:12px; display:flex; align-items:center; justify-content:space-between;">
                <span style="font-weight:600; font-size:0.88rem; color:{txt_c};">Tavily Search</span>
                <span style="background:rgba(239,68,68,0.2); color:#ef4444; font-size:0.75rem; font-weight:700; padding:3px 8px; border-radius:6px;">MISSING</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        
        # Interactive Inputs if missing or user wants to edit
        with st.expander("⚙️ Configure API Credentials", expanded=(not together_key or not tavily_key)):
            t_input = st.text_input(
                "Together AI Key",
                value=together_key,
                type="password",
                help="Sign up free at https://www.together.ai/"
            )
            tv_input = st.text_input(
                "Tavily Search Key",
                value=tavily_key,
                type="password",
                help="Sign up free at https://tavily.com/"
            )

            # Auto-sync inputs to environment
            if t_input and t_input.strip() != together_key:
                os.environ["TOGETHER_API_KEY"] = t_input.strip()
                together_key = t_input.strip()
            if tv_input and tv_input.strip() != tavily_key:
                os.environ["TAVILY_API_KEY"] = tv_input.strip()
                tavily_key = tv_input.strip()

            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                if st.button("🧪 Test Keys", use_container_width=True):
                    with st.spinner("Testing API connections..."):
                        t_status, tv_status = False, False
                        t_msg, tv_msg = "", ""
                        try:
                            from agents import get_llm, _call_llm
                            test_llm = get_llm()
                            if not test_llm:
                                raise ValueError("Together AI key is empty.")
                            res = _call_llm(test_llm, "Reply with: OK")
                            t_status = True
                            t_msg = "Together AI is active & ready!"
                        except Exception as e:
                            t_msg = str(e)

                        try:
                            from agents import get_tavily_tool
                            test_tool = get_tavily_tool()
                            if not test_tool:
                                raise ValueError("Tavily key is empty.")
                            test_tool.invoke({"query": "AI news"})
                            tv_status = True
                            tv_msg = "Tavily search is active & ready!"
                        except Exception as e:
                            tv_msg = str(e)

                        if t_status:
                            st.success(f"✅ {t_msg}")
                        else:
                            st.error(f"❌ Together AI: {t_msg}")

                        if tv_status:
                            st.success(f"✅ {tv_msg}")
                        else:
                            st.error(f"❌ Tavily: {tv_msg}")

            with c_btn2:
                if st.button("💾 Save .env", use_container_width=True):
                    if together_key or tavily_key:
                        with open(".env", "w") as f:
                            f.write(f"TOGETHER_API_KEY={together_key}\nTAVILY_API_KEY={tavily_key}\n")
                        st.success("Saved to .env file!")
                    else:
                        st.warning("Please enter keys first.")

    if not together_key or not tavily_key:
        return False

    return True


# --- Hero Section ---
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">⚡ Autonomous Agent Swarm</div>
    <div class="hero-title">Nexus Multi-Agent Research Assistant</div>
    <div class="hero-subtitle">
        An intelligent team of four autonomous AI agents collaborating in real-time to investigate, synthesize, critique, and deliver comprehensive research reports on any subject.
    </div>
</div>
""", unsafe_allow_html=True)

# --- Agent Showcase Cards ---
st.markdown("""
<div class="agent-grid">
    <div class="agent-card">
        <div class="agent-card-icon">🎯</div>
        <div class="agent-card-name">Supervisor</div>
        <div class="agent-card-desc">Orchestrates the workflow, breaks down complex topics, and delegates tasks dynamically.</div>
    </div>
    <div class="agent-card">
        <div class="agent-card-icon">🔍</div>
        <div class="agent-card-name">Researcher</div>
        <div class="agent-card-desc">Performs real-time web searches via Tavily, retrieving current facts and sources.</div>
    </div>
    <div class="agent-card">
        <div class="agent-card-icon">✍️</div>
        <div class="agent-card-name">Writer</div>
        <div class="agent-card-desc">Transforms raw research into an engaging, structured, and comprehensive report.</div>
    </div>
    <div class="agent-card">
        <div class="agent-card-icon">🔎</div>
        <div class="agent-card-name">Critiquer</div>
        <div class="agent-card-desc">Audits report depth, accuracy, and clarity, demanding revisions until high standards are met.</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Verify API Keys
keys_ready = check_api_keys()

if not keys_ready:
    card_bg = "rgba(99, 102, 241, 0.12)" if is_dark else "rgba(99, 102, 241, 0.08)"
    card_border = "rgba(99, 102, 241, 0.35)" if is_dark else "#cbd5e1"
    st.markdown(f"""
    <div style="background:{card_bg}; border:1px solid {card_border}; border-radius:14px; padding:22px 26px; margin-bottom:24px;">
        <h4 style="margin:0 0 8px 0; color:#818cf8; font-weight:700;">🔑 API Keys Required to Run Research</h4>
        <p style="margin:0; font-size:0.95rem; line-height:1.6;">
            To generate reports, the AI agent swarm requires two free API keys. Please open <b>⚙️ Configure API Credentials</b> in the left sidebar and enter your keys:
        </p>
        <ul style="margin:10px 0 0 0; padding-left:22px; font-size:0.92rem; line-height:1.8;">
            <li><b>Together AI Key:</b> Powers the Mixtral-8x7B writing agent. Get a free key at <a href="https://www.together.ai/" target="_blank" style="color:#6366f1; font-weight:600;">together.ai</a></li>
            <li><b>Tavily Search Key:</b> Powers real-time web search. Get a free key at <a href="https://tavily.com/" target="_blank" style="color:#6366f1; font-weight:600;">tavily.com</a> (1,000 free searches/month)</li>
        </ul>
        <p style="margin:10px 0 0 0; font-size:0.85rem; opacity:0.85;">
            💡 <i>Tip: After pasting your keys in the sidebar, click <b>🧪 Test Keys</b> to verify the connection, then click <b>💾 Save .env</b> to remember them permanently!</i>
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("### 🎛️ Workflow Controls")
    max_iterations = st.slider(
        "Max Iterations",
        min_value=5,
        max_value=30,
        value=15,
        help="Maximum interaction cycles between agents before forcing completion"
    )
    
    st.markdown("---")
    st.markdown("### 🧭 Architecture")
    st.caption("Supervisor ➔ Researcher ➔ Writer ➔ Critiquer Loop")
    if os.path.exists(os.path.join("assets", "research_graph.png")):
        st.image(os.path.join("assets", "research_graph.png"), caption="LangGraph Topology", use_column_width=True)


# --- Input Section with Sample Prompts ---
st.markdown("### 🎯 Enter Research Topic")

# Quick prompt chips
sample_prompts = [
    "Impact of Quantum Computing on Cybersecurity",
    "Breakthroughs in Solid-State Battery Tech",
    "CRISPR Therapeutics: Clinical Trials & Ethics",
    "Autonomous AI Agents in Software Engineering"
]

st.markdown("<small style='opacity: 0.7;'>Try a suggested topic:</small>", unsafe_allow_html=True)
chip_cols = st.columns(4)
for i, prompt_text in enumerate(sample_prompts):
    with chip_cols[i]:
        if st.button(prompt_text, key=f"chip_{i}", use_container_width=True):
            st.session_state["topic_query"] = prompt_text
            st.rerun()

# Text input for custom topic
default_topic = st.session_state.get("topic_query", "")
topic = st.text_input(
    label="Research Topic",
    value=default_topic,
    placeholder="e.g., DeepSeek vs OpenAI architectural differences and performance analysis",
    label_visibility="collapsed"
)

# Start Button
col_btn, col_hint = st.columns([1, 3])
with col_btn:
    start_clicked = st.button("🚀 Start Deep Research", type="primary", use_container_width=True, disabled=(not keys_ready))
with col_hint:
    if not keys_ready:
        st.caption("🔒 *Configure your API keys in the left sidebar to enable research.*")
    else:
        st.caption("⚡ *The agent swarm will automatically loop until the draft is approved.*")


# --- Execution Pipeline ---
if start_clicked:
    if not topic.strip():
        st.error("⚠️ Please specify a research topic to proceed.")
    else:
        st.markdown("---")
        
        initial_state = {
            "main_task": topic.strip(),
            "research_findings": [],
            "draft": "",
            "critique_notes": "",
            "revision_number": 0,
            "next_step": "",
            "current_sub_task": ""
        }
        config = {"recursion_limit": max_iterations}

        st.subheader("📡 Live Agent Swarm Activity")
        progress_bar = st.progress(0.0)
        status_box = st.empty()
        status_box.info("🚀 Supervisor is analyzing the query and formulating the plan...")

        activity_container = st.container()

        final_state = None
        step_count = 0
        all_states = []

        agent_styles = {
            "supervisor": {"badge": "supervisor-badge", "icon": "🎯", "name": "Supervisor Agent"},
            "researcher": {"badge": "researcher-badge", "icon": "🔍", "name": "Researcher Agent"},
            "writer":     {"badge": "writer-badge",     "icon": "✍️", "name": "Writer Agent"},
            "critiquer":  {"badge": "critiquer-badge",  "icon": "🔎", "name": "Critiquer Agent"}
        }

        try:
            with activity_container:
                for step in app.stream(initial_state, config=config):
                    step_count += 1
                    progress_pct = min(step_count / max_iterations, 0.95)
                    progress_bar.progress(progress_pct)

                    node_name = list(step.keys())[0]
                    node_output = step[node_name]
                    all_states.append((node_name, node_output))
                    final_state = node_output

                    style = agent_styles.get(node_name, {"badge": "supervisor-badge", "icon": "🤖", "name": node_name.upper()})

                    with st.container():
                        col_agent, col_step = st.columns([4, 1])
                        with col_agent:
                            st.markdown(f"""
                            <div class="step-card">
                                <span class="step-badge {style['badge']}">{style['icon']} {style['name']}</span>
                            </div>
                            """, unsafe_allow_html=True)
                        with col_step:
                            st.caption(f"Iteration #{step_count}")

                        if node_name == "supervisor":
                            next_step = node_output.get("next_step", "N/A")
                            task = node_output.get("current_sub_task", "N/A")
                            st.markdown(f"**Directive:** `{next_step.upper()}` — *{task}*")

                        elif node_name == "researcher":
                            findings = node_output.get("research_findings", [])
                            if findings:
                                latest = findings[-1]
                                st.success("✅ Web intelligence gathered via Tavily")
                                with st.expander(f"📑 View Extracted Findings (Step {step_count})", expanded=False):
                                    st.markdown(latest)

                        elif node_name == "writer":
                            draft = node_output.get("draft", "")
                            rev = node_output.get("revision_number", 0)
                            st.success(f"📝 Draft Revision #{rev} generated ({len(draft)} characters)")
                            with st.expander(f"📖 Preview Draft Revision #{rev}", expanded=False):
                                st.markdown(draft)

                        elif node_name == "critiquer":
                            critique = node_output.get("critique_notes", "")
                            if "APPROVED" in critique.upper():
                                st.success("🎉 **Quality Audit: APPROVED!** Report meets all publication standards.")
                            else:
                                st.warning("🔄 **Quality Audit: Revisions Needed.** Sending back for refinement.")
                            with st.expander(f"📋 Reviewer Feedback (Step {step_count})", expanded=False):
                                st.markdown(critique)

                        st.markdown("<hr style='margin: 12px 0; border: none; border-top: 1px solid rgba(128,128,128,0.15);'>", unsafe_allow_html=True)
                        time.sleep(0.2)

            status_box.success("🎉 Research & Synthesis Complete!")
            progress_bar.progress(1.0)

        except Exception as e:
            status_box.error("❌ Workflow terminated with an error.")
            st.error(f"Error details: {str(e)}")
            final_state = None

        # --- Final Report & Analytics Section ---
        st.markdown("---")
        
        # Extract the highest quality draft from states
        final_draft = None
        if final_state and isinstance(final_state, dict):
            final_draft = final_state.get("draft", "")

        if not final_draft or len(final_draft.strip()) < 50:
            for node_name, state in reversed(all_states):
                if isinstance(state, dict) and state.get("draft"):
                    cand = state.get("draft", "")
                    if len(cand.strip()) > 50:
                        final_draft = cand
                        final_state = state
                        break

        if final_draft and len(final_draft.strip()) > 50:
            st.markdown("## 📚 Final Intelligence Report")

            # Metrics Row
            revision_count = final_state.get("revision_number", 0) if isinstance(final_state, dict) else 0
            sources_list = final_state.get("research_findings", []) if isinstance(final_state, dict) else []
            word_count = len(final_draft.split())
            read_time = max(1, round(word_count / 200))

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{word_count}</div>
                    <div class="stat-label">Total Words</div>
                </div>
                """, unsafe_allow_html=True)
            with m2:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{len(sources_list)}</div>
                    <div class="stat-label">Research Blocks</div>
                </div>
                """, unsafe_allow_html=True)
            with m3:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{revision_count}</div>
                    <div class="stat-label">Review Cycles</div>
                </div>
                """, unsafe_allow_html=True)
            with m4:
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-number">{read_time} min</div>
                    <div class="stat-label">Reading Time</div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Presentation Tabs
            tab_report, tab_sources, tab_download = st.tabs(["📄 Full Document", "🔍 Knowledge Base", "📥 Export Options"])

            with tab_report:
                st.markdown(f"""
                <div class="report-box">
                    {final_draft}
                </div>
                """, unsafe_allow_html=True)

            with tab_sources:
                if sources_list:
                    for s_idx, src in enumerate(sources_list, 1):
                        st.markdown(f"""
                        <div class="source-card">
                            <strong>Source Packet #{s_idx}</strong>
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(src)
                        st.divider()
                else:
                    st.info("No raw sources available.")

            with tab_download:
                st.markdown("### Export Your Report")
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    st.download_button(
                        label="📥 Download as Markdown (.md)",
                        data=final_draft,
                        file_name=f"{topic.replace(' ', '_').lower()}_report.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                with col_d2:
                    st.download_button(
                        label="📄 Download as Plain Text (.txt)",
                        data=final_draft,
                        file_name=f"{topic.replace(' ', '_').lower()}_report.txt",
                        mime="text/plain",
                        use_container_width=True
                    )

        else:
            st.error("❌ No final report was generated.")
            with st.expander("🛠️ Why did this happen? (Troubleshooting)", expanded=True):
                st.markdown("""
                **Most Common Causes:**
                1. **Together AI API Key or Credits**:
                   - Make sure your Together AI key is valid and has active trial credits at [together.ai](https://www.together.ai/).
                   - Test your connection anytime using the **🧪 Test Keys** button in the sidebar.
                2. **Tavily Search API Key**:
                   - Verify that your Tavily key is entered and not rate-limited at [tavily.com](https://tavily.com/).
                3. **Check Activity Feed**:
                   - Review the agent activity logs above for any specific error messages returned by the models.
                """)

# --- Footer ---
st.markdown("""
<div style='text-align: center; opacity: 0.65; font-size: 0.85rem; padding: 40px 0 20px 0;'>
    Nexus Multi-Agent Research Assistant • Built with <b>LangGraph</b>, <b>LangChain</b>, <b>Together AI</b> & <b>Tavily Search</b>
</div>
""", unsafe_allow_html=True)