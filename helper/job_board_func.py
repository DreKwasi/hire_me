import streamlit as st
from . import db
import datetime as dt
from helper.search import run_search
    
    
def view_jobboard():
    startIndex = 0

    # counter = call.load_counter()
    # items = call.load_items()
    # query = call.load_query()

    counter, query, items = db.call_user_entries()
    print(len(items))
    last_page = len(items) // 10

    if "page_number" not in st.session_state:
        st.session_state.page_number = 0

    st.header("Job Boards")
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        placeholder = st.empty()
        placeholder.metric("Number of Queries", value=counter["search_count"])

    with col2:
        entry_holder = st.empty()
        entry_holder.metric("Number of Job Posts", value=len(items))
    col3.metric("Page Number", value=st.session_state.page_number + 1)

    st.sidebar.header("Filter Search Results")
    roles = st.sidebar.multiselect(
        "Select Role/Keyword",
        options=[
            "Data Analyst",
            "Product Manager",
            "UI/UX Designer",
            "Data Scientist",
            "Business Intelligence Analyst",
            "Backend Developer",
            "Frontend Developer",
            "Inventory Analyst",
            "Billing Analyst",
        ],
        default="Data Analyst",
    )

    text = st.sidebar.text_input(
        "Add keywords related to the role above (Optional)", help="Optional"
    )
    
    st.sidebar.markdown("-----")

    roles.extend(text.split(","))
    roles = [x.strip() for x in roles]

    locations = st.sidebar.multiselect(
        "Search Location",
        options=["remote global", "remote worldwide", "hire from anywhere", "Accra"],
        default="remote global",
    )
    
    exclude_locations = st.sidebar.multiselect(
        "Exclude Location",
        options=["Europe", "LATAM", "Americas", "APAC"],
        default=None,
    )
    
    
    st.sidebar.markdown("-----")
    
    # date = st.sidebar.slider(
    #     "Filter Start Date",
    #     min_value=dt.date.today(),
    #     max_value=dt.date(year=2022, month=1, day=1),
    # )
    date = st.sidebar.date_input("Select Start Date")
    
    st.sidebar.markdown("-----")

    search, generate = st.sidebar.columns([1, 1])
        
    prev, next = st.sidebar.columns([1, 1])
    
    st.sidebar.markdown("-----")

    if search.button("Start Search", type="primary"):
        try:
            items, counter, query = run_search(
                roles,
                locations,
                exclude_locations,
                date=dt.datetime.strftime(date, "%Y-%m-%d"),
            )
        except TypeError:
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
            st.info("No More Entries. Try Other Keywords")
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

                st.write(f"#### {index+1}. {title}")
                with st.expander("View Job Post"):
                    st.markdown(
                        f"""
                                {snippet} \n
                                <a href="{link_address}">Apply Here</a>
                                """,
                        unsafe_allow_html=True,
                    )
        else:
            st.info(
                "No More Job Post. Click 'Get More Job Posts' or 'Include More Keywords'"
            )
            

    # Made by section - footer in the sidebar
    st.sidebar.markdown(
        """
    ### Made with ❤️ by:
    - [Andrews Asamoah Boateng](https://www.linkedin.com/in/aaboateng/)
    - [Joel Kojo Abaka Anaman](https://www.linkedin.com/in/joelanaman/)
    

    """
    )