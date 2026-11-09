import streamlit as st
import pandas as pd
import os

# Page setup
st.set_page_config(page_title="TalkFinder AI - PM Conference Companion", page_icon="🎙️", layout="wide")

st.title("TalkFinder 🎙️ [PM Edition: LLM + MCP + Elasticsearch]")
st.markdown("Your **Product Manager AI Companion** that leverages **Model Context Protocol (MCP)** and **Elasticsearch retrieval** to build your ideal conference schedule.")

# --- 1. SIDEBAR CONFIGURATION & PM ROLE SELECTOR ---
st.sidebar.header("🔐 Copilot Settings")
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password", help="Required for live LLM conversational recommendations.")

st.sidebar.divider()
st.sidebar.header("👤 Persona & MCP Context")

# Persona customization for tailored recommendations
user_role = st.sidebar.selectbox(
    "Your Current Focus Area:",
    ["General Product Manager", "AI/ML Product Manager", "Growth & Analytics PM", "Technical / Platform PM", "Fintech & Product Strategy"]
)

st.sidebar.info(f"Target Role: **{user_role}**")
st.sidebar.success("MCP Protocol Server: Active")
st.sidebar.success("Elasticsearch Index: Connected")

# Mock MCP Context Provider (Model Context Protocol Resources)
@st.cache_data
def get_mcp_resources(role):
    return {
        "protocols": [
            "Rule 1: Prioritize sessions matching product management frameworks and strategic outcomes.",
            "Rule 2: Use Elasticsearch vector search for multi-field semantic topic matching.",
            "Rule 3: Attendees can bookmark sessions and export a clean CSV itinerary."
        ],
        "pm_persona_guidelines": f"Tailor all schedule recommendations specifically for a {role}. Highlight actionable takeaways, metrics, and cross-functional leadership techniques."
    }

mcp_context = get_mcp_resources(user_role)

# --- 2. EXPANDED CONFERENCE TALK DATABASE ---
data = {
    "ID": [1, 2, 3, 4, 5, 6, 7],
    "Title": [
        "AI Product Management: From Concept to Production",
        "Ethics, Bias, and Responsible AI in Product Design",
        "Data-Driven Decision Making using Cloud Analytics",
        "Building Scalable Search & RAG Architectures with Elasticsearch",
        "Modern Roadmapping & Agile Alignment for Product Leaders",
        "Fintech Innovation & Threat Intelligence Automation",
        "DevOps & CI/CD Pipelines for Product Managers"
    ],
    "Speaker": [
        "Alice Smith (Head of Product)", 
        "Bob Jones (AI Ethics Lead)", 
        "Charlie Brown (Analytics Director)", 
        "Diana Prince (Principal Engineer)", 
        "Evan Wright (VP of Product)",
        "Fiona Gallagher (Fintech Strategy Lead)",
        "George Clark (DevOps Lead)"
    ],
    "Time": ["9:00 AM", "10:30 AM", "11:45 AM", "1:00 PM", "2:30 PM", "3:45 PM", "5:00 PM"],
    "Tracks": ["AI & LLMs", "Ethics & Governance", "Analytics & Data", "Elasticsearch & RAG", "Product Leadership", "Fintech & Strategy", "DevOps & Platform"],
    "Description": [
        "Learn how product managers define specs, manage risk, and evaluate metrics when launching LLM-powered features.",
        "Navigating algorithmic bias, user transparency, and ethical frameworks when designing user-facing AI products.",
        "How PMs can leverage real-time cloud data pipelines and telemetry to guide product experimentation and roadmap prioritization.",
        "A practical look at how vector search and hybrid retrieval power modern AI applications and search engines.",
        "Strategic techniques for aligning stakeholders, managing executive expectations, and maintaining agile product backlogs.",
        "Exploring automated threat intelligence, compliance automation, and secure payment systems in fintech product development.",
        "Understanding infrastructure automation, CI/CD telemetry, and deployment metrics to better collaborate with engineering teams."
    ]
}
df = pd.DataFrame(data)

# Initialize Session State
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hello! I am your TalkFinder PM Copilot. As a **{user_role}**, what key topics or skills are you looking to master at this conference?"}
    ]

# --- 3. MAIN APP TABS ---
tab1, tab2, tab3 = st.tabs(["🤖
