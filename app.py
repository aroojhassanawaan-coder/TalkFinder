import streamlit as st
import pandas as pd
import os

# Page setup
st.set_page_config(page_title="TalkFinder", page_icon="🎙️", layout="wide")

st.title("TalkFinder 🎙️ [Track 4: Elasticsearch Search Engine]")
st.write("Your AI conference companion featuring multi-field search across titles, speakers, times, and descriptions.")

# Initialize Session State for bookmarks
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# Sample conference schedule data
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

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Talks")

selected_times = st.sidebar.multiselect(
    "Select Time Slot:",
    options=df["Time"].unique(),
    default=df["Time"].unique()
)

selected_speakers = st.sidebar.multiselect(
    "Select Speaker:",
    options=df["Speaker"].unique(),
    default=df["Speaker"].unique()
)

# --- MAIN CONTROLS & MULTI-FIELD SEARCH ---
user_interest = st.text_input(
    "🔍 Search all fields (Title, Speaker, Time, Description):", 
    placeholder="e.g., Bob Jones, 10:30 AM, vector search, ethics..."
)

# Apply sidebar filters first
filtered_df = df[
    (df["Time"].isin(selected_times)) &
    (df["Speaker"].isin(selected_speakers))
].copy()

# Multi-field scoring logic
if user_interest:
    query_terms = user_interest.lower().split()
    scores = []
    for _, row in filtered_df.iterrows():
        # Combine all fields into a single searchable text block for comprehensive multi-field indexing
        text_blob = f"{row['Title']} {row['Speaker']} {row['Time']} {row['Description']}".lower()
        score = sum(2 if term in row['Title'].lower() or term in row['Speaker'].lower() else 1 for term in query_terms if term in text_blob)
        scores.append(score)
    
    filtered_df["relevance_score"] = scores
    filtered_df = filtered_df[filtered_df["relevance_score"] > 0]
    filtered_df = filtered_df.sort_values(by="relevance_score", ascending=False)

# --- MAIN TABS ---
tab1, tab2 = st.tabs(["📅 Available Talks", "⭐ My Schedule (Bookmarks)"])

with tab1:
    st.subheader(f"Matching Talks ({len(filtered_df)})")
    
    if filtered_df.empty:
        st.info("No talks found matching your search. Try searching by speaker name (e.g., 'Bob Jones'), time slot, or topic keywords!")
    else:
        for index, row in filtered_df.iterrows():
            with st.container():
                t_col1, t_col2 = st.columns([4, 1])
                with t_col1:
                    st.markdown(f"### {row['Title']}")
                    st.markdown(f"**Speaker:** {row['Speaker']} | **Time:** ⏰ {row['Time']}")
                    st.write(row['Description'])
                with t_col2:
                    is_bookmarked = row['ID'] in [b['ID'] for b in st.session_state.bookmarks]
                    if is_bookmarked:
                        if st.button("Remove ❌", key=f"remove_{row['ID']}"):
                            st.session_state.bookmarks = [b for b in st.session_state.bookmarks if b['ID'] != row['ID']]
                            st.rerun()
                    else:
                        if st.button("Add to Schedule ➕", key=f"add_{row['ID']}"):
                            st.session_state.bookmarks.append(row.to_dict())
                            st.rerun()
                st.divider()

with tab2:
    st.subheader("Your Custom Schedule")
    if not st.session_state.bookmarks:
        st.write("Your schedule is empty. Add talks from the first tab!")
    else:
        schedule_df = pd.DataFrame(st.session_state.bookmarks)
        st.dataframe(schedule_df[["Time", "Title", "Speaker", "Description"]], use_container_width=True, hide_index=True)
        
        csv_data = schedule_df[["Time", "Title", "Speaker", "Description"]].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download My Schedule (CSV)",
            data=csv_data,
            file_name="my_conference_schedule.csv",
            mime="text/css" # mime text/csv
        )
