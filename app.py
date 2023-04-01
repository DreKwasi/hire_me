import streamlit as st
from st_pages import Page, show_pages


show_pages(
    [
        Page("app.py", "Home", "🏠"),
        Page("other_pages/global_companies.py", "Global Companies", "📖"),
        Page("other_pages/custom_search.py", "Custom Job Search", "🔎"),
    ]
)


# About the JobBoard Project
with st.expander("About this App"):
    st.markdown(
        """
                This App Is for Searching for Open Roles on Various Job Boards Across the Internet.
                This Filter Search section allows for tailored job postings based on your search criteria.
                """
    )

# How to use the app
with st.expander("How to use the app"):
    st.markdown(
        """
    JobBoard Page
    - Under the Sidebar, Select Any of the Roles Under the Filter Search Results
    - Add Keywords if Necessary e.g. 'Python, Health, Supply Chain etc.'
    - Include the Location for the Role i.e 'global, remote global, hire from anywhere'
    - Select the Start Date of the Search.
    - You can also exclude certain locations from the search by using the Exclude Location Section
    - Once you are comfortable with the options, Click on the Start Search Button.
    - Each search result shows only 10 entries per page, to get more search result Click on the "Get More Job Posts" button
    - The Next Page and Previous Page Allows for Navigation between the Pages.
    
    
    """
    )

# Made by section - footer in the sidebar
st.sidebar.markdown(
    """
### Made with ❤️ by:
- [Andrews Asamoah Boateng](https://www.linkedin.com/in/aaboateng/)
- [Joel Kojo Abaka Anaman](https://www.linkedin.com/in/joelanaman/)


"""
)
