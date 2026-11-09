# TalkFinder
AI conference companion that builds a personalized talk schedule from what you want to learn

# TalkFinder 🎙️

An AI-powered conference companion that builds a personalized talk schedule based on what attendees want to learn.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/aroojhassanawaan-coder/TalkFinder.git](https://github.com/aroojhassanawaan-coder/TalkFinder.git)
   cd TalkFinder

Install dependencies:

Bash
pip install -r requirements.txt

Run the application:

Bash
streamlit run app.py

Tech Stack & Tools
Frontend/UI: Streamlit

Data Processing: Pandas

Search & Recommendation Engine: Elasticsearch Vector Search / Python

AI Assistance Disclosure: Built using AI-assisted pair programming for learning and development.


Sidebar (st.sidebar.multiselect): Adds filter controls on the left side of the screen so attendees can isolate specific speakers or timeslots.

Session State (st.session_state): Stores bookmarked talks in memory while the user interacts with the web app without losing their selections on screen refreshes.

Tabs (st.tabs): Separates browsing available talks from viewing the personal itinerary into distinct tabs for a clean UI.

Download Button (st.download_button): Converts the bookmarked dataframe into a UTF-8 encoded CSV file downloadable directly to the attendee's computer.
