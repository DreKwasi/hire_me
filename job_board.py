import streamlit as st
from search import run_search
import json
from functools import reduce
from bs4 import BeautifulSoup
import requests
import datetime as dt
import call_func as call


startIndex = 0
count = 10

counter = call.load_counter()
items = call.load_items()
query = call.load_query()


st.set_page_config(
    page_title="JobBoards",
    page_icon="clipboard",
    initial_sidebar_state="expanded",
    layout="wide",
)

st.header("Job Boards")

placeholder = st.empty()
placeholder.metric("Number of Searches", value=counter["search_count"])

st.sidebar.header("Filter Search Results")


roles = st.sidebar.multiselect(
    "Select Role/Keyword",
    options=[
        "Data Analyst",
        "Product Manager",
        "UI/UX Designer",
        "Data Scientist",
        "Business Intelligence Analyst",
    ],
    default="Data Scientist",
)

text = st.sidebar.text_input(
    "Add keywords related to the role above (Optional)", help="Optional"
)

roles.extend(text.split(","))
roles = [x.strip() for x in roles]

locations = st.sidebar.multiselect(
    "Search Location",
    options=["remote global", "remote worldwide", "hire from anywhere"],
    default="remote global",
)
date = st.sidebar.slider(
    "Filter Start Date",
    min_value=dt.date.today(),
    max_value=dt.date(year=2022, month=1, day=1),
)
exclude_locations = st.sidebar.multiselect(
    "Exclude Location",
    options=["Europe", "LATAM", "Americas", "APAC"],
    default=None,
)
# st.date_input("Filter Start Date")


search_button = st.sidebar.button("Start Search", type="secondary")

next_page_button = st.sidebar.button("Next Page", type="secondary")
prev_page_button = st.sidebar.button("Previous Page", type="secondary")

if search_button:
    items, counter, query = run_search(
        roles, locations, exclude_locations, date=dt.datetime.strftime(date, "%Y-%m-%d")
    )

    placeholder.metric("Number of Searches", value=counter["search_count"])
    total_page_count = 1


if next_page_button and len(items) < 20 and query["nextPage"]:
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
        st.info("Only One Page Available for the Role. Try Other Keywords")
        st.stop()
    query = call.load_query()
    placeholder.metric("Number of Searches", value=counter["search_count"])
    startIndex = query["request"][0]["startIndex"]


if prev_page_button and query["previousPage"]:
    items = call.load_items()
    startIndex = query["request"][0]["startIndex"] - 10
    print(startIndex)


with st.spinner("Loading Jobs..."):
    endIndex = count + startIndex
    print(startIndex, endIndex)

    display_res = items[startIndex:endIndex]

    for index, result in enumerate(display_res, start=startIndex):
        link_address = result["link"]
        link_address.replace("()", "")

        snippet = result["snippet"]
        try:
            title = result["metatags"]["twitter:title"]
        except KeyError:
            title = result["title"]

        st.write(f"#### {index+1}. {title}")
        with st.expander("View Post"):
            st.markdown(
                f"""
                        {snippet} \n
                        <a href="{link_address}">Apply Here</a>
                        """,
                unsafe_allow_html=True,
            )
