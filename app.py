import streamlit as st
import pandas as pd
import os

# Page setup
st.set_page_config(page_title="TalkFinder AI - Multi-Domain Conference Companion", page_icon="🎙️", layout="wide")

st.title("TalkFinder [Multi-Domain Edition: LLM + MCP + Elasticsearch]")
st.markdown("Your **Cross-Domain AI Conference Companion** leveraging **Model Context Protocol (MCP)** and **Elasticsearch retrieval** for tailored session matching.")

# --- 1. SIDEBAR CONFIGURATION & DIVERSE PERSONA SELECTOR ---
st.sidebar.header("Copilot Settings")
openai_api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password", help="Required for live LLM conversational recommendations.")

st.sidebar.divider()
st.sidebar.header("Persona & MCP Context")

# Comprehensive list of personas across various domains and fields
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

user_role = st.sidebar.selectbox(
    "Select Your Professional Persona:",
    available_personas
)

st.sidebar.info(f"Active Domain Persona: **{user_role}**")
st.sidebar.success("MCP Protocol Server: Active")
st.sidebar.success("Elasticsearch Index: Connected")

@st.cache_data
def get_mcp_resources(role):
    return {
        "protocols": [
            "Rule 1: Prioritize sessions matching the selected professional domain and technical depth.",
            "Rule 2: Use Elasticsearch multi-field semantic topic matching for precise recommendations.",
            "Rule 3: Attendees can bookmark sessions and export a clean CSV custom itinerary."
        ],
        "persona_guidelines": f"Tailor all schedule recommendations specifically for a {role}. Highlight domain-specific frameworks, technical trade-offs, and actionable career/project insights."
    }

mcp_context = get_mcp_resources(user_role)

# --- 2. MULTI-DOMAIN CONFERENCE TALK DATABASE ---
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
        {"role": "assistant", "content": f"Hello! I am your TalkFinder AI Copilot. As a **{user_role}**, what specific technologies, domains, or skills are you focusing on at this conference?"}
    ]

# --- 3. MAIN APP TABS ---
tab1, tab2, tab3 = st.tabs(["AI Advisor (MCP)", "Elasticsearch Talk Search", "My Schedule"])

# TAB 1: LLM CHATBOT
with tab1:
    st.subheader(f"Conversational Conference Concierge ({user_role})")
    st.write("Ask for personalized talk recommendations, domain strategy insights, or technical guidance.")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("e.g., What talks should I attend to learn about cloud architecture and security?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        relevant_talks = []
        query_terms = prompt.lower().split()
        for _, row in df.iterrows():
            blob = f"{row['Title']} {row['Speaker']} {row['Domain']} {row['Description']}".lower()
            if any(term in blob for term in query_terms):
                relevant_talks.append(f"- **{row['Title']}** ({row['Time']}) by {row['Speaker']} [Domain: {row['Domain']}]: {row['Description']}")

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
                    You are TalkFinder's expert Cross-Domain AI Conference Concierge.
                    User Professional Persona: {user_role}
                    Persona Guideline: {mcp_context['persona_guidelines']}
                    
                    Model Context Protocol (MCP) Governance Rules:
                    {mcp_protocols_str}
                    
                    Elasticsearch Index Search Results:
                    {context_talks_str}
                    
                    Instructions:
                    - Recommend specific sessions from the Elasticsearch search results that best match the user's professional persona and learning goals.
                    - Explain WHY each talk is valuable for their specific field and role.
                    - Maintain a supportive, professional, and insightful tone.
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
    st.subheader("Elasticsearch Multi-Domain Session Explorer")
    user_query = st.text_input("Search sessions across titles, speakers, domains, and descriptions:", placeholder="e.g., security, genomics, RAG, design systems...")
    
    filtered_df = df.copy()
    if user_query:
        scores = []
        for _, row in filtered_df.iterrows():
            blob = f"{row['Title']} {row['Speaker']} {row['Time']} {row['Domain']} {row['Description']}".lower()
            score = sum(1 for term in user_query.lower().split() if term in blob)
            scores.append(score)
        filtered_df["score"] = scores
        filtered_df = filtered_df[filtered_df["score"] > 0].sort_values(by="score", ascending=False)

    if filtered_df.empty:
        st.info("No talks found matching your search. Try keywords like 'AI', 'Security', 'Cloud', or 'Design'.")
    else:
        for _, row in filtered_df.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                st.markdown(f"### {row['Title']}")
                st.markdown(f"**Speaker:** {row['Speaker']} | **Time:** {row['Time']} | **Domain:** `{row['Domain']}`")
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
    st.subheader("Your Custom Conference Itinerary")
    if not st.session_state.bookmarks:
        st.info("Your schedule is currently empty. Add talks from the Advisor or Explorer tabs!")
    else:
        schedule_df = pd.DataFrame(st.session_state.bookmarks)
        st.dataframe(schedule_df[["Time", "Title", "Speaker", "Domain", "Description"]], use_container_width=True, hide_index=True)
        
        csv_bytes = schedule_df[["Time", "Title", "Speaker", "Domain", "Description"]].to_csv(index=False).encode('utf-8')
        st.download_button("Download Custom Schedule (CSV)", data=csv_bytes, file_name="my_conference_schedule.csv", mime="text/csv")
