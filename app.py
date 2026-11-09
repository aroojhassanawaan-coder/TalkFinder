import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="TalkFinder", page_icon="🎙️", layout="wide")

st.title("TalkFinder 🎙️")
st.write("Your personalized AI conference companion. Search topics, filter sessions, build your custom itinerary, and download it!")

# Initialize Session State for bookmarks if it doesn't exist yet
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

# Time Filter
selected_times = st.sidebar.multiselect(
    "Select Time Slot:",
    options=df["Time"].unique(),
    default=df["Time"].unique()
)

# Speaker Filter
selected_speakers = st.sidebar.multiselect(
    "Select Speaker:",
    options=df["Speaker"].unique(),
    default=df["Speaker"].unique()
)

# --- MAIN CONTROLS & SEARCH ---
col1, col2 = st.columns([3, 1])

with col1:
    user_interest = st.text_input("🔍 What do you want to learn today?", placeholder="e.g., vector search, ethics, LLMs...")

# Filter DataFrame based on sidebar filters and keyword search
filtered_df = df[
    (df["Time"].isin(selected_times)) &
    (df["Speaker"].isin(selected_speakers))
]

if user_interest:
    filtered_df = filtered_df[
        filtered_df["Description"].str.contains(user_interest, case=False, na=False) |
        filtered_df["Title"].str.contains(user_interest, case=False, na=False)
    ]

# --- MAIN CONTENT TABS ---
tab1, tab2 = st.tabs(["📅 Available Talks", "⭐ My Schedule (Bookmarks)"])

# TAB 1: Display Available Talks
with tab1:
    st.subheader(f"Matching Talks ({len(filtered_df)})")
    
    if filtered_df.empty:
        st.info("No talks found matching your search and filter criteria.")
    else:
        for index, row in filtered_df.iterrows():
            with st.container():
                t_col1, t_col2 = st.columns([4, 1])
                with t_col1:
                    st.markdown(f"### {row['Title']}")
                    st.markdown(f"**Speaker:** {row['Speaker']} | **Time:** ⏰ {row['Time']}")
                    st.write(row['Description'])
                with t_col2:
                    # Check if talk is already bookmarked
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

# TAB 2: Bookmarked Personal Schedule
with tab2:
    st.subheader("Your Custom Schedule")
    
    if not st.session_state.bookmarks:
        st.write("You haven't added any talks to your schedule yet. Click **Add to Schedule ➕** on any talk to save it here!")
    else:
        schedule_df = pd.DataFrame(st.session_state.bookmarks)
        
        # Display the custom schedule
        st.dataframe(
            schedule_df[["Time", "Title", "Speaker", "Description"]], 
            use_container_width=True,
            hide_index=True
        )
        
        # Download Schedule as CSV
        csv_data = schedule_df[["Time", "Title", "Speaker", "Description"]].to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download My Schedule (CSV)",
            data=csv_data,
            file_name="my_conference_schedule.csv",
            mime="text/csv"
        )
