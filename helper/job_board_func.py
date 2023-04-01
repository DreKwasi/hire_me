import streamlit as st
from . import db
import datetime as dt
from helper.search import run_search
import json

with open("assets/criteria.json", "r") as file:
    criteria = json.load(file)


def view_jobboard():
    st.header("Advanced Google Search 🔎")
    info_holder = st.empty()
    
    startIndex = 0

    counter, query, items = db.call_user_entries()
    last_page = len(items) // 10

    if "page_number" not in st.session_state:
        st.session_state.page_number = 0
    st.sidebar.markdown(
        """
        #### *Build Your Career with [Career Wheel](https://mycareerwheel.com/)*
                """
    )
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        placeholder = st.empty()
        placeholder.metric("Number of Queries", value=counter["search_count"])

    with col2:
        entry_holder = st.empty()
        entry_holder.metric("Number of Job Posts", value=len(items))
    col3.metric("Page Number", value=st.session_state.page_number + 1)

    st.sidebar.header("Filter Search Results")
    st.sidebar.write("**Select Role/Keyword**")
    roles = st.sidebar.multiselect(
        "Select Role/Keyword",
        options=criteria["roles"],
        default="Data Analyst",
        help="Multiple Roles can be selected",
        label_visibility="collapsed",
    )

    st.sidebar.write("**Add keywords related to the role above (Optional)**")
    text = st.sidebar.text_input(
        "Add keywords related to the role above (Optional)",
        help="Keywords should be separated by commas",
        label_visibility="collapsed",
    )

    roles.extend(text.split(","))
    roles = [x.strip() for x in roles]

    st.sidebar.write("**Search Location**")
    locations = st.sidebar.multiselect(
        "Search Location",
        options=["remote global", "remote worldwide", "hire from anywhere"],
        default="remote global",
        help="Multiple locations can be selected",
        label_visibility="collapsed"
    )

    st.sidebar.write("**Exclude Location**")
    exclude_locations = st.sidebar.multiselect(
        "Exclude Location",
        options=criteria["exclude_locations"],
        default=None,
        help="Multiple locations can be selected",
        label_visibility="collapsed"
    )

    st.sidebar.write("**Select Start Date**")
    date = st.sidebar.date_input("Select Start Date", label_visibility="collapsed")


    search, generate = st.sidebar.columns([1, 1])

    prev, next = st.sidebar.columns([1, 1])

    if search.button("Start Search", type="primary"):
        try:
            items, counter, query = run_search(
                roles,
                locations,
                exclude_locations,
                date=dt.datetime.strftime(date, "%Y-%m-%d"),
            )
        except Exception:
            st.info("No More Entries")
            entry_holder.metric("Number of Job Posts", value=0)
            st.stop()
        placeholder.metric("Number of Searches", value=counter["search_count"])
        entry_holder.metric("Number of Job Posts", value=len(items))
        st.session_state.page_number = 0

    if generate.button("Get More Posts", type="secondary"):
        try:
            items, counter = run_search(
                roles,
                locations,
                exclude_locations,
                date=dt.datetime.strftime(date, "%Y-%m-%d"),
                query=query,
                next_page=True,
                start_num=query["nextPage"][0]["startIndex"] - 1,
            )
        except Exception:
            st.info("No More Entries")
        placeholder.metric("Number of Searches", value=counter["search_count"])
        entry_holder.metric("Number of Job Posts", value=len(items))

    if next.button("Next Page :arrow_forward:", type="secondary"):
        if st.session_state.page_number + 1 > last_page:
            st.session_state.page_number = 0
        else:
            st.session_state.page_number += 1

    if prev.button(":arrow_backward: Previous Page", type="secondary"):
        if st.session_state.page_number - 1 < 0:
            st.session_state.page_number = last_page
        else:
            st.session_state.page_number -= 1

    startIndex = st.session_state.page_number * 10
    endIndex = (
        (1 + st.session_state.page_number) * 10
        if st.session_state.page_number != 0
        else 10
    )

    with st.spinner("Loading Jobs..."):
        display_res = items[startIndex:endIndex]

        if len(display_res) > 0:
            for index, result in enumerate(display_res, start=startIndex):
                link_address = result["link"]
                link_address.replace("()", "")

                snippet = result["snippet"]
                try:
                    title = result["metatags"]["twitter:title"]
                except KeyError:
                    title = result["title"]

                col1, col2 = st.columns([1, 20])
                col1.write(f"#### {index+1}.")
                with col2.expander(f"**{title}**"):
                    st.markdown(
                        f"""
                                {snippet} \n
                                <a href="{link_address}">Apply Here</a>
                                """,
                        unsafe_allow_html=True,
                    )
        else:
            st.info("Click 'Get More Job Posts' or 'Include More Keywords'")

    info_holder.info("Reduce Search Frequency")

    # Made by section - footer in the sidebar
    st.sidebar.markdown(
        """
    ### Made with ❤️ by:
    - [Andrews Asamoah Boateng](https://www.linkedin.com/in/aaboateng/)
    - [Joel Kojo Abaka Anaman](https://www.linkedin.com/in/joelanaman/)
    

    """
    )
