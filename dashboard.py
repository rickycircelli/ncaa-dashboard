import streamlit as st
from scraper import scrape_tfrrs_results
from data_cleaning import clean_tfrrs_data
from visualizations import plot_time_progression, plot_placement_distribution

st.set_page_config(page_title="NCAA Athlete Dashboard", page_icon="🏃", layout="wide")

st.title("NCAA Athlete Dashboard")

st.markdown("""
Welcome! This dashboard lets you:
- Scrape race results for any NCAA athlete on TFRRS.
- Visualize their time progression for a selected event.
- Analyze their placement distribution across all races.
""")

# User inputs TFRRS URL
st.subheader("Enter Athlete TFRRS URL")
url = st.text_input("Paste TFRRS Athlete Profile URL below:")


# Save atlhete data in cache to avoid re-scraping
@st.cache_data(show_spinner=False)
def get_athlete_data(url):
    df_scraped = scrape_tfrrs_results(url, wait_time=15)
    return clean_tfrrs_data(df_scraped)

if url:
    with st.spinner("Scraping athlete data..."):
        df_cleaned = get_athlete_data(url)


        # Show data preview
        st.subheader("Meet Results Preview")
        st.dataframe(df_cleaned[['Meet_Info', 'Event', 'Race_Date', 'Mark', 'Time_seconds', 'Placement_Number']])

        # Dropdown to select event from available races
        st.subheader("Select Event for Time Progression Graph")
        unique_events = df_cleaned['Event'].unique().tolist()
        event_filter = st.selectbox("Select Event for Time Progression Graph:", unique_events)

        # Button to plot time progression graph
        if st.button("📈 Show Time Progression Graph"):
            fig = plot_time_progression(df_cleaned, event_filter)
            st.pyplot(fig)  
        
        # Button to plot placement distribution graph
        if st.button("📊 Show Placement Distribution Graph"):
            fig = plot_placement_distribution(df_cleaned)
            st.pyplot(fig)  
