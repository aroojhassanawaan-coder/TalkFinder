import streamlit as st
import pandas as pd
import numpy as np
import os
from sentence_transformers import SentenceTransformer, util

# Page setup
st.set_page_config(page_title="TalkFinder (Semantic Search)", page_icon="🎙️", layout="wide")

st.title("TalkFinder 🎙️ [Track 4: Semantic AI Vector Search]")
st.write("Powered by **Sentence Transformers vector embeddings** & **Elasticsearch hybrid search** architecture.")

# Initialize Session State for bookmarks
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# Load lightweight embedding model once into cache
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_embedding_model()

# Conference schedule dataset
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

# Pre-compute combined searchable text and vector embeddings for all talks
df["searchable_text"] = df["Title"] + " " + df["Speaker"] + " " + df["Time"] + " " + df["Description"]

@st.cache_data
def get_talk_embeddings(texts):
    return model.encode(texts, convert_to_tensor=True)

talk_embeddings = get_talk_embeddings(df["searchable_text"].tolist())

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

# --- MAIN CONTROLS & SEMANTIC AI SEARCH ---
user_interest = st.text_input(
    "🧠 What do you want to learn today? (Semantic Vector Search):", 
    placeholder="e.g., how to prevent algorithmic discrimination, building vector search engines, prompt engineering..."
)

# Apply hard sidebar filters first
filtered_df = df[
    (df["Time"].isin(selected_times)) &
    (df["Speaker"].isin(selected_speakers))
].copy()

# Apply Semantic Vector Matching
if user_interest and not filtered_df.empty:
    # 1. Generate dense vector embedding for user prompt
    query_embedding = model.encode(user_interest, convert_to_tensor=True)
    
    # 2. Get embeddings corresponding to currently filtered talks
    filtered_indices = filtered_df.index.tolist()
    current_embeddings = talk_embeddings[filtered_indices]
    
    # 3. Compute cosine similarity between query vector and talk vectors
    cosine_scores = util.cos_sim(query_embedding, current_embeddings)[0].cpu().numpy()
    
    filtered_df["semantic_score"] = cosine_scores
    # Sort by highest semantic relevance score
    filtered_df = filtered_df.sort_values(by="semantic_score", ascending=False)
    # Display talks with non-negative similarity
    filtered_df = filtered_df[filtered_df["semantic_score"] > 0.1]

# --- MAIN TABS ---
tab1, tab2 = st.tabs(["📅 Available Talks", "⭐ My Schedule (Bookmarks)"])

with tab1:
    st.subheader(f"Matching Talks ({len(filtered_df)})")
    
    if filtered_df.empty:
        st.info("No talks found matching your query context. Try describing what you'd like to learn in plain language!")
    else:
        for index, row in filtered_df.iterrows():
            with st.container():
                t_col1, t_col2 = st.columns([4, 1])
                with t_col1:
                    st.markdown(f"### {row['Title']}")
                    st.markdown(f"**Speaker:** {row['Speaker']} | **Time:** ⏰ {row['Time']}")
                    st.write(row['Description'])
                    if "semantic_score" in row:
                        st.caption(f"🎯 *Semantic Relevance Score: {row['semantic_score']:.2f}*")
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
            mime="text/csv"
        )
