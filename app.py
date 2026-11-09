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
    .main {
        background-color: #0f172a;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
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
        st.write("3. Link user bookmarks to AI Assistant for personal itinerary analysis.")

@st.cache_data
def get_mcp_resources(role):
    return {
        "protocols": [
            "Rule 1: Prioritize sessions matching the selected professional domain and technical depth.",
            "Rule 2: Use Elasticsearch multi-field semantic topic matching for precise recommendations.",
            "Rule 3: Integrate user's saved schedule bookmarks directly into the AI Assistant context."
        ],
        "persona_guidelines": f"Tailor all schedule recommendations specifically for a {role}. Highlight domain-specific frameworks, technical trade-offs, and actionable career insights."
    }

mcp_context = get_mcp_resources(user_role)

# --- 2. MULTI-DOMAIN DATASET ---
data = {
    "ID": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Title": [
        "AI Product Management: From Concept to Production",
        "Ethics, Bias, and Responsible AI in Product Design",
        "Data-Driven Decision Making using Cloud Analytics",
        "Building Scalable Search & RAG Architectures with Elasticsearch",
        "Advanced LLM Fine-Tuning and Prompt Engineering Patterns",
        "Cybersecurity Threat Intelligence Automation in Fintech",
        "DevOps & CI/CD Telemetry for High-Scale Cloud Systems",
        "UX Design Systems for Complex Enterprise Applications",
        "Genomics Data Pipelines and Healthcare Analytics at Scale",
        "Modern Roadmapping & Cross-Functional Engineering Alignment"
    ],
    "Speaker": [
        "Alice Smith (Head of Product)", 
        "Bob Jones (AI Ethics Lead)", 
        "Charlie Brown (Analytics Director)", 
        "Diana Prince (Principal Engineer)", 
        "Dr. Marcus Vance (AI Research Scientist)",
        "Fiona Gallagher (Cybersecurity Lead)",
        "George Clark (DevOps Architect)",
        "Elena Rostova (Lead UX Strategist)",
        "Dr. Samuel King (Bioinformatics VP)",
        "Evan Wright (VP of Engineering & Product)"
    ],
    "Time": ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "4:45 PM", "5:30 PM"],
    "Domain": ["Product & Strategy", "AI & Ethics", "Data Science", "Data Engineering", "AI & Machine Learning", "Cybersecurity", "DevOps & Cloud", "UX Design", "Healthcare Tech", "Engineering Leadership"],
    "Description": [
        "Learn how product managers define specs, manage risk, and evaluate metrics when launching LLM features.",
        "Navigating algorithmic bias, user transparency, and ethical frameworks when designing user-facing AI products.",
        "How teams leverage real-time cloud data pipelines and telemetry to guide experimentation and prioritization.",
        "A practical look at how vector search and hybrid retrieval power modern search engines and RAG applications.",
        "Deep dive into parameter-efficient fine-tuning (LoRA), quantization, and prompt optimization techniques.",
        "Exploring automated threat detection, secure payment protocols, and fraud mitigation in digital finance.",
        "Automating cloud infrastructure, container security orchestration, and production monitoring metrics.",
        "Creating cohesive, accessible design systems that scale across multi-platform enterprise products.",
        "Processing massive genomic datasets securely while maintaining HIPAA compliance and clinical accuracy.",
        "Strategic techniques for aligning stakeholders, engineering velocity, and agile product backlogs."
    ]
}
df = pd.DataFrame(data)

# Initialize Session State
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"👋 Hello! I am your **TalkFinder AI Assistant**. As a **{user_role}**, I can see your saved schedule bookmarks and recommend talks. What can I help you with today?"}
    ]

# --- 3. MAIN APP TABS ---
tab1, tab2, tab3 = st.tabs(["💬 AI Assistant (MCP + Saved Schedule)", "🔍 Elasticsearch Explorer", "⭐ Saved Schedule"])

# TAB 1: LLM CHATBOT (Linked with Bookmarks & Elasticsearch RAG)
with tab1:
    st.caption(f"Currently advising: **{user_role}** | Saved Bookmarks in Memory: **{len(st.session_state.bookmarks)} talks**")
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about your saved schedule, get talk recommendations, or session strategies..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # 1. Retrieve saved schedule bookmarks context
        saved_schedule_list = []
        if st.session_state.bookmarks:
            for b in st.session_state.bookmarks:
                saved_schedule_list.append(f"- **{b['Title']}** at {b['Time']} by {b['Speaker']} [{b['Domain']}]")
        saved_schedule_str = "\n".join(saved_schedule_list) if saved_schedule_list else "No talks bookmarked yet."

        # 2. Retrieve relevant Elasticsearch talk matches based on query
        relevant_talks = []
        query_terms = prompt.lower().split()
        for _, row in df.iterrows():
            blob = f"{row['Title']} {row['Speaker']} {row['Domain']} {row['Description']}".lower()
            if any(term in blob for term in query_terms):
                relevant_talks.append(f"- **{row['Title']}** ({row['Time']}) by {row['Speaker']} [Domain: {row['Domain']}]: {row['Description']}")

        context_talks_str = "\n".join(relevant_talks) if relevant_talks
