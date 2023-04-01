import streamlit as st
from st_pages import Page, show_pages, add_page_title
from streamlit_extras.switch_page_button import switch_page


st.set_page_config(
    page_title="JobBoards",
    page_icon="clipboard",
    initial_sidebar_state="expanded",
    layout="wide",
)

show_pages(
    [
        Page("app.py", "Home", "🏠"),
        Page("other_pages/global_companies.py", "Global Companies", "🏢"),
        Page("other_pages/top_boards.py", "Personalized Search", "🎯"),
        Page("other_pages/custom_search.py", "Custom Google Search", "🔎"),
    ]
)

# Header section with app name and emoji
st.title("🔍 Job Search App")

# Explanation section with emojis
st.write("Find your dream job faster with this job search app! 🚀")
st.write("🌟The app features a job catalogue and custom Google search 🔎 to help you find relevant job posts quickly. 💪")
st.write("🌟Customize your search by location and industry get personalized job recommendations. 🎯")
st.write("Save time and effort by accessing a wide range of job posts from top companies in real-time. ⏰")

# Search button to redirect to search results page
st.write("")
st.write("")
st.write("")
st.write("")
if st.button("Get Started", type="primary", use_container_width=True):
        switch_page("Global Companies")



# Made by section - footer in the sidebar
st.sidebar.markdown(
    """
### Made with ❤️ by:
- [Andrews Asamoah Boateng](https://www.linkedin.com/in/aaboateng/)
- [Joel Kojo Abaka Anaman](https://www.linkedin.com/in/joelanaman/)


"""
)
