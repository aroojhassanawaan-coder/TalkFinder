import streamlit as st
import pandas as pd
import os

# Page Configuration
st.set_page_config(
    page_title="TalkFinder AI | Next-Gen Conference Concierge",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM BEAUTIFUL CSS INJECTION ---
st.markdown("""
<style>
    /* Global Styling & Theme Adjustments */
    .main {
        background-color: #0f172a;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Custom Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
    }
    .header-title {
        color: #f8fafc;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin: 0;
    }
    .header-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 6px;
    }
    
    /* Metric & Badge Cards */
    .badge-container {
        display: flex;
        gap: 12px;
        margin-top: 14px;
    }
    .status-badge {
        background-color: #1e293b;
        border: 1px solid #334155;
        color: #38bdf8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Talk Cards Styling */
    .talk-card {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 16px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .talk-card:hover {
        border-color: #38bdf8;
        transform: translateY(-2px);
    }
    .talk-title {
        color: #f8fafc;
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .talk-meta {
        color: #38bdf8;
        font-size: 0.9rem;
        font-weight: 500;
        margin-bottom: 10px;
    }
    .talk-desc {
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .domain-tag {
        background-color: #0284c7;
        color: #ffffff;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        margin-left: 8px;
    }

    /* Sidebar Clean styling */
    .css-1d3b13b {
        background-color: #0f172a;
    }
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.markdown("""
<div class="header-banner">
    <div class="header-title">TalkFinder 🎙️</div>
    <div class="header-subtitle">AI-Powered Conference Concierge with Model Context Protocol (MCP) & Elasticsearch RAG</div>
    <div class="badge-container">
        <span class="status-badge">⚡ MCP Protocol: Active</span>
        <span class="status-badge">🔍 Elasticsearch Engine: Connected</span>
        <span class="status-badge">🤖 Track 4 Architecture</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 1. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("⚙️ Copilot Controls")
    
    st.subheader("🔐 Authentication")
    openai_api_key = st.text_input(
        "OpenAI API Key:",
        type="password",
        placeholder="sk-...",
        help="Paste your OpenAI API key here to enable full LLM conversational mode."
    )
    
    st.divider()
    
    st.subheader("👤 Professional Persona")
    available_personas = [
        "Product Manager & Agile Lead",
        "AI / Machine Learning Engineer",
        "Software Engineer & Full Stack Developer",
        "Data Scientist & Analytics Specialist",
        "Cybersecurity & Threat Intelligence Analyst",
        "Cloud & DevOps Architect",
        "UX / UI Designer & Researcher",
        "Fintech & Banking Strategist",
        "Healthcare Tech & Bioinformatics Lead",
        "Enterprise Growth & Sales Strategist"
    ]
    user_role = st.selectbox("Select Your Focus Area:", available_personas)
    
    st.info(f"Target Domain: **{user_role}**")
    
    with st.expander("📋 Active MCP Governance Protocols"):
        st.caption("Context rules enforced by MCP Server:")
        st.write("1. Prioritize domain-specific technical & strategic alignment.")
        st.write("2. Query Elasticsearch index across multi-field text vectors.")
        st.write("3. Provide actionable session recommendations and schedule exports.")

# MCP Context Resource
@st.cache_data
def get_mcp_resources(role):
    return {
        "protocols": [
            "Rule 1: Prioritize sessions matching the selected professional domain and technical depth.",
            "Rule 2: Use Elasticsearch multi-field semantic topic matching for precise recommendations.",
            "Rule 3: Attendees can bookmark sessions and export a clean CSV custom itinerary."
        ],
        "persona_guidelines": f"Tailor all schedule recommendations specifically for a {role}. Highlight domain-specific frameworks, technical trade-offs, and actionable career insights."
    }

mcp_context = get_mcp_resources(user_role)

# --- 2. MULTI-DOMAIN DATASET ---
data = {
    "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 1
