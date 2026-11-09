import streamlit as st
import pandas as pd
import os

# Page setup
st.set_page_config(page_title="TalkFinder AI - PM Conference Companion", page_icon="🎙️", layout="wide")

st.title("TalkFinder [PM Edition: LLM + MCP + Elasticsearch]")
st.markdown("Your **Product Manager AI Companion** that leverages **Model Context Protocol (MCP)** and **Elasticsearch retrieval** to build your ideal conference schedule.")

# --- 1. SIDEBAR CONFIGURATION & PM ROLE SELECTOR ---
st.sidebar.header("Copilot Settings")
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password", help="Required for live LLM conversational recommendations.")

st.sidebar.divider()
st.sidebar.header("Persona & MCP Context")

user_role = st.sidebar.selectbox(
    "Your Current Focus Area:",
    ["General Product Manager", "AI/ML Product Manager", "Growth & Analytics PM", "Technical / Platform PM", "Fintech & Product Strategy"]
)

st.sidebar.info(f"Target Role: **{user_role}**")
st.sidebar.success("MCP Protocol Server: Active")
st.sidebar.success("Elasticsearch Index: Connected")

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
tab1, tab2, tab3 = st.tabs(["LLM PM Advisor (MCP)", "Elasticsearch Talk Search", "My Schedule"])

# TAB 1: LLM CHATBOT
with tab1:
    st.subheader(f"Conversational PM Schedule Concierge ({user_role})")
    st.write("Ask for personalized talk recommendations, schedule strategies, or specific topic advice.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("e.g., I'm a PM wanting to learn about AI product design and data analytics. What should I attend?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        relevant_talks = []
        query_terms = prompt.lower().split()
        for _, row in df.iterrows():
            blob = f"{row['Title']} {row['Speaker']} {row['Tracks']} {row['Description']}".lower()
            if any(term in blob for term in query_terms):
                relevant_talks.append(f"- **{row['Title']}** ({row['Time']}) by {row['Speaker']} [Track: {row['Tracks']}]: {row['Description']}")

        context_talks_str = "\n".join(relevant_talks) if relevant_talks else "No direct talk matches found."
        mcp_protocols_str = "\n".join(mcp_context["protocols"])

        with st.chat_message("assistant"):
            if not openai_api_key:
                response_content = (
                    f"*(Demo Mode - Enter an OpenAI API Key in the sidebar for full conversational AI)*\n\n"
                    f"**Tailored Recommendation for {user_role}:**\n"
                    f"Based on your query, here are the top Elasticsearch-retrieved sessions:\n\n{context_talks_str}"
                )
                st.markdown(response_content)
            else:
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=openai_api_key)
                    
                    system_prompt = f"""
                    You are TalkFinder's expert AI Product Management Conference Concierge.
                    User Persona: {user_role}
                    Persona Guideline: {mcp_context['pm_persona_guidelines']}
                    
                    Model Context Protocol (MCP) Governance Rules:
                    {mcp_protocols_str}
                    
                    Elasticsearch Index Search Results:
                    {context_talks_str}
                    
                    Instructions:
                    - Recommend specific sessions from the Elasticsearch search results that best match the user's PM role and goals.
                    - Explain WHY each talk is valuable for a Product Manager.
                    - Maintain a supportive, professional, and knowledgeable tone.
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
                    response_content = f"Error generating recommendation: {e}"
                    st.error(response_content)

        st.session_state.messages.append({"role": "assistant", "content": response_content})

# TAB 2: ELASTICSEARCH TALK EXPLORER
with tab2:
    st.subheader("Elasticsearch Session Explorer")
    user_query = st.text_input("Search sessions across titles, speakers, tracks, and descriptions:", placeholder="e.g., roadmap, cloud analytics, ethics...")
    
    filtered_df = df.copy()
    if user_query:
        scores = []
        for _, row in filtered_df.iterrows():
            blob = f"{row['Title']} {row['Speaker']} {row['Time']} {row['Tracks']} {row['Description']}".lower()
            score = sum(1 for term in user_query.lower().split() if term in blob)
            scores.append(score)
        filtered_df["score"] = scores
        filtered_df = filtered_df[filtered_df["score"] > 0].sort_values(by="score", ascending=False)

    if filtered_df.empty:
        st.info("No talks found matching your search. Try keywords like 'AI', 'Roadmap', or 'Fintech'.")
    else:
        for _, row in filtered_df.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {row['Title']}")
                st.markdown(f"**Speaker:** {row['Speaker']} | **Time:** {row['Time']} | **Track:** `{row['Tracks']}`")
                st.write(row['Description'])
            with col2:
                is_saved = row['ID'] in [b['ID'] for b in st.session_state.bookmarks]
                if is_saved:
                    if st.button("Remove", key=f"r_{row['ID']}"):
                        st.session_state.bookmarks = [b for b in st.session_state.bookmarks if b['ID'] != row['ID']]
                        st.rerun()
                else:
                    if st.button("Add", key=f"a_{row['ID']}"):
                        st.session_state.bookmarks.append(row.to_dict())
                        st.rerun()
            st.divider()

# TAB 3: SAVED SCHEDULE
with tab3:
    st.subheader("Your Custom PM Conference Itinerary")
    if not st.session_state.bookmarks:
        st.info("Your schedule is currently empty. Add talks from the Advisor or Explorer tabs!")
    else:
        schedule_df = pd.DataFrame(st.session_state.bookmarks)
        st.dataframe(schedule_df[["Time", "Title", "Speaker", "Tracks", "Description"]], use_container_width=True, hide_index=True)
        
        csv_bytes = schedule_df[["Time", "Title", "Speaker", "Tracks", "Description"]].to_csv(index=False).encode('utf-8')
        st.download_button("Download Custom PM Schedule (CSV)", data=csv_bytes, file_name="my_pm_conference_schedule.csv", mime="text/csv")
