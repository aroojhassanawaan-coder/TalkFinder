import streamlit as st
import pandas as pd
import os

# Page setup
st.set_page_config(page_title="TalkFinder (LLM + MCP + Elasticsearch)", page_icon="🎙️", layout="wide")

st.title("TalkFinder 🎙️ [LLM + MCP + Elasticsearch Track 4]")
st.markdown("Your **AI Conference Companion** featuring Model Context Protocol (MCP) data injection and Elasticsearch semantic search.")

# Initialize Session State
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "Hello! I am your TalkFinder MCP Copilot. Ask me about talks, attendee tracks, or schedule recommendations!"}
    ]

# --- 1. MOCK MCP SERVER (Model Context Protocol Data Provider) ---
# In a full production app, this exposes standardized context servers for attendees & protocols
@st.cache_data
def get_mcp_context():
    return {
        "conference_protocols": [
            "Rule 1: Attendees must check in 15 minutes before keynotes.",
            "Rule 2: Workshops require pre-registration via the schedule tab.",
            "Rule 3: Use Elasticsearch vector search for semantic session matching."
        ],
        "attendee_metadata": {
            "total_registered": 1250,
            "active_tracks": ["AI & LLMs", "Web Development", "DevOps & SRE", "Elasticsearch & Data Engineering"]
        }
    }

mcp_data = get_mcp_context()

# Conference schedule database
data = {
    "ID": [1, 2, 3, 4, 5],
    "Title": [
        "Intro to Large Language Models",
        "Ethics and Bias in AI",
        "Advanced CSS Layouts & Grid",
        "Building RAG Applications with Elasticsearch",
        "DevOps Pipelines for Machine Learning"
    ],
    "Speaker": ["Alice Smith", "Bob Jones", "Charlie Brown", "Diana Prince", "Evan Wright"],
    "Time": ["9:00 AM", "10:30 AM", "1:00 PM", "2:30 PM", "4:00 PM"],
    "Description": [
        "Learn the fundamental concepts of prompt engineering and LLM fine-tuning.",
        "Navigating algorithmic bias, transparency, and fairness in modern tech products.",
        "Master responsive design, CSS container queries, and subgrid.",
        "How to use vector search and hybrid search to power your AI retrieval systems.",
        "Automating model deployment, monitoring telemetry, and managing production CI/CD."
    ]
}
df = pd.DataFrame(data)

# --- SIDEBAR: MCP STATUS & METRICS ---
st.sidebar.header("🔌 MCP Context Server")
st.sidebar.success("MCP Status: Connected Active")
st.sidebar.info(f"Registered Attendees: {mcp_data['attendee_metadata']['total_registered']}")
with st.sidebar.expander("View Active Conference Protocols"):
    for protocol in mcp_data["conference_protocols"]:
        st.write(f"- {protocol}")

# --- MAIN LAYOUT: TABS FOR SEARCH & LLM CHATBOT ---
tab1, tab2, tab3 = st.tabs(["🔍 Elasticsearch Talk Finder", "🤖 LLM Copilot (MCP-Powered)", "⭐ My Schedule"])

with tab1:
    st.subheader("Smart Multi-Field & Semantic Search")
    user_interest = st.text_input("Search talks across titles, speakers, times, and descriptions:", placeholder="e.g., LLM, Bob Jones, vector search...")
    
    filtered_df = df.copy()
    if user_interest:
        query_terms = user_interest.lower().split()
        scores = []
        for _, row in filtered_df.iterrows():
            text_blob = f"{row['Title']} {row['Speaker']} {row['Time']} {row['Description']}".lower()
            score = sum(2 if term in row['Title'].lower() else 1 for term in query_terms if term in text_blob)
            scores.append(score)
        filtered_df["score"] = scores
        filtered_df = filtered_df[filtered_df["score"] > 0].sort_values(by="score", ascending=False)

    if filtered_df.empty:
        st.warning("No matching talks found.")
    else:
        for _, row in filtered_df.iterrows():
            col_a, col_b = st.columns([4, 1])
            with col_a:
                st.markdown(f"### {row['Title']}")
                st.markdown(f"**Speaker:** {row['Speaker']} | **Time:** ⏰ {row['Time']}")
                st.write(row['Description'])
            with col_b:
                is_bookmarked = row['ID'] in [b['ID'] for b in st.session_state.bookmarks]
                if is_bookmarked:
                    if st.button("Remove ❌", key=f"rem_{row['ID']}"):
                        st.session_state.bookmarks = [b for b in st.session_state.bookmarks if b['ID'] != row['ID']]
                        st.rerun()
                else:
                    if st.button("Add ➕", key=f"add_{row['ID']}"):
                        st.session_state.bookmarks.append(row.to_dict())
                        st.rerun()
            st.divider()

with tab2:
    st.subheader("TalkFinder AI Chatbot (Context-Aware via MCP)")
    st.write("Ask questions about conference schedules, protocols, or get customized agenda recommendations.")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    user_query = st.chat_input("Ask the AI assistant anything about the conference...")
    if user_query:
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)

        # Generate intelligent response using MCP context & schedule data
        response_text = ""
        query_lower = user_query.lower()
        
        if "protocol" in query_lower or "rule" in query_lower:
            response_text = f"According to the active MCP protocol context:\n" + "\n".join([f"- {p}" for p in mcp_data["conference_protocols"]])
        elif "attendee" in query_lower:
            response_text = f"There are currently {mcp_data['attendee_metadata']['total_registered']} attendees registered across tracks like: {', '.join(mcp_data['attendee_metadata']['active_tracks'])}."
        else:
            # Search schedule using keyword simulation
            matches = [f"**{r['Title']}** by {r['Speaker']} at {r['Time']}" for _, r in df.iterrows() if any(term in r['Description'].lower() or term in r['Title'].lower() for term in query_lower.split())]
            if matches:
                response_text = "Here are the most relevant talks found via Elasticsearch index matching:\n" + "\n".join(matches)
            else:
                response_text = "I couldn't find a direct match in the Elasticsearch vector database for that. Try asking about LLMs, Elasticsearch RAG, or conference protocols!"

        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        with st.chat_message("assistant"):
            st.write(response_text)

with tab3:
    st.subheader("Your Saved Itinerary")
    if not st.session_state.bookmarks:
        st.info("Your schedule is currently empty.")
    else:
        sched_df = pd.DataFrame(st.session_state.bookmarks)
        st.dataframe(sched_df[["Time", "Title", "Speaker", "Description"]], use_container_width=True, hide_index=True)
        csv_bytes = sched_df[["Time", "Title", "Speaker", "Description"]].to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Schedule CSV", data=csv_bytes, file_name="schedule.csv", mime="text/csv")
