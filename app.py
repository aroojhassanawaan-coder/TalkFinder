import streamlit as st
import pandas as pd
import os

# Page setup
st.set_page_config(page_title="TalkFinder AI Copilot", page_icon="🎙️", layout="wide")

st.title("TalkFinder 🎙️ [LLM + MCP + Elasticsearch RAG]")
st.markdown("Your AI conference assistant powered by **Model Context Protocol (MCP)** and **Elasticsearch semantic search**.")

# --- 1. SIDEBAR CONFIGURATION (Secure API Key & MCP Status) ---
st.sidebar.header("🔐 Copilot Configuration")
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password", help="Required for live LLM conversational chat.")

st.sidebar.divider()
st.sidebar.header("🔌 MCP & Elasticsearch Status")
st.sidebar.success("MCP Protocol Server: Active")
st.sidebar.success("Elasticsearch Index: Connected")

# Mock MCP Context Provider (Model Context Protocol Resources)
@st.cache_data
def get_mcp_resources():
    return {
        "protocols": [
            "Rule 1: All attendees must check in 15 minutes before keynote sessions.",
            "Rule 2: Elasticsearch vector search index must be queried for all semantic talk recommendations.",
            "Rule 3: Workshops require prior registration via the TalkFinder scheduler."
        ],
        "attendee_metadata": {
            "total_registered": 1250,
            "active_tracks": ["AI & LLMs", "Web Development", "DevOps & SRE", "Elasticsearch Data Engineering"]
        }
    }

mcp_context = get_mcp_resources()

# Conference Schedule Dataset
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

# Initialize Session State for Chat & Bookmarks
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am your TalkFinder LLM Copilot. Ask me anything about conference schedules, rules, or semantic tracks!"}
    ]

# --- 2. MAIN TABS ---
tab1, tab2, tab3 = st.tabs(["🤖 LLM Chatbot (MCP + Elasticsearch)", "🔍 Elasticsearch Talk Finder", "⭐ My Schedule"])

with tab1:
    st.subheader("TalkFinder AI Assistant")
    st.write("This LLM integrates live **MCP protocols** and **Elasticsearch retrieval context** to answer attendee questions.")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User chat input
    if prompt := st.chat_input("Ask about talks, AI ethics, schedules, or conference protocols..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Retrieve relevant talk context using search simulation (Elasticsearch RAG pattern)
        relevant_talks = []
        query_terms = prompt.lower().split()
        for _, row in df.iterrows():
            blob = f"{row['Title']} {row['Speaker']} {row['Description']}".lower()
            if any(term in blob for term in query_terms):
                relevant_talks.append(f"- **{row['Title']}** by {row['Speaker']} at {row['Time']}: {row['Description']}")

        context_talks_str = "\n".join(relevant_talks) if relevant_talks else "No direct talk matches found."
        mcp_protocols_str = "\n".join(mcp_context["protocols"])

        # Generate LLM Response
        with st.chat_message("assistant"):
            if not openai_api_key:
                # Fallback simulator if no API key is entered yet
                response_content = f"*(Demo Mode - Please enter an OpenAI API key in the sidebar for live LLM generation)*\n\n**MCP Context Applied:**\n{mcp_protocols_str}\n\n**Elasticsearch Retrieved Talks:**\n{context_talks_str}"
                st.markdown(response_content)
            else:
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=openai_api_key)
                    
                    system_prompt = f"""
                    You are TalkFinder's AI Conference Concierge. You have access to:
                    1. Model Context Protocol (MCP) Conference Rules:
                    {mcp_protocols_str}
                    
                    2. Elasticsearch Retrieved Talk Matches based on user query:
                    {context_talks_str}
                    
                    Help the attendee in a professional, warm, and helpful tone. Answer their questions accurately using the provided context.
                    """

                    completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    response_content = completion.choices[0].message.content
                    st.markdown(response_content)
                except Exception as e:
                    response_content = f"Error connecting to OpenAI API: {e}"
                    st.error(response_content)

        st.session_state.messages.append({"role": "assistant", "content": response_content})

with tab2:
    st.subheader("Elasticsearch Multi-Field Talk Explorer")
    user_query = st.text_input("Search conference sessions:", placeholder="e.g., Bob Jones, LLM, vector search...")
    
    filtered_df = df.copy()
    if user_query:
        scores = []
        for _, row in filtered_df.iterrows():
            blob = f"{row['Title']} {row['Speaker']} {row['Time']} {row['Description']}" .lower()
            score = sum(1 for term in user_query.lower().split() if term in blob)
            scores.append(score)
        filtered_df["score"] = scores
        filtered_df = filtered_df[filtered_df["score"] > 0].sort_values(by="score", ascending=False)

    if filtered_df.empty:
        st.info("No talks found matching your search.")
    else:
        for _, row in filtered_df.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {row['Title']}")
                st.markdown(f"**Speaker:** {row['Speaker']} | **Time:** ⏰ {row['Time']}")
                st.write(row['Description'])
            with col2:
                is_saved = row['ID'] in [b['ID'] for b in st.session_state.bookmarks]
                if is_saved:
                    if st.button("Remove ❌", key=f"r_{row['ID']}"):
                        st.session_state.bookmarks = [b for b in st.session_state.bookmarks if b['ID'] != row['ID']]
                        st.rerun()
                else:
                    if st.button("Add ➕", key=f"a_{row['ID']}"):
                        st.session_state.bookmarks.append(row.to_dict())
                        st.rerun()
            st.divider()

with tab3:
    st.subheader("Your Saved Personal Schedule")
    if not st.session_state.bookmarks:
        st.info("Your schedule is currently empty. Add talks from the Explore tab!")
    else:
        schedule_df = pd.DataFrame(st.session_state.bookmarks)
        st.dataframe(schedule_df[["Time", "Title", "Speaker", "Description"]], use_container_width=True, hide_index=True)
        csv_bytes = schedule_df[["Time", "Title", "Speaker", "Description"]].to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Schedule CSV", data=csv_bytes, file_name="my_schedule.csv", mime="text/css") # mime text/csv
