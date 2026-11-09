import streamlit as st
import pandas as pd

st.title("TalkFinder 🎙️")
st.write("Your personalized AI conference companion.")

# Sample conference schedule data
data = {
    "Title": ["Intro to LLMs", "Ethics in Tech", "Advanced CSS Tricks"],
    "Speaker": ["Alice Smith", "Bob Jones", "Charlie Brown"],
    "Time": ["9:00 AM", "10:30 AM", "1:00 PM"],
    "Description": ["Learn the basics of Large Language Models", "Navigating bias and fairness", "Master modern web layouts"]
}
df = pd.DataFrame(data)

# User input box
user_interest = st.text_input("What do you want to learn today?")

if user_interest:
    st.subheader("Your Personalized Schedule:")
    # Filter talks based on user input
    results = df[df['Description'].str.contains(user_interest, case=False, na=False)]
    
    if not results.empty:
        for index, row in results.iterrows():
            st.markdown(f"**{row['Title']}** by {row['Speaker']} at *{row['Time']}*")
            st.write(row['Description'])
            st.write("---")
    else:
        st.write("No matching talks found. Try a different keyword like 'LLMs' or 'Ethics'!")