import streamlit as st
from helper import styles, data_parser, footer
import streamlit.components.v1 as components
import pandas as pd
from streamlit_option_menu import option_menu
import itertools
from streamlit_extras.no_default_selectbox import selectbox
from streamlit_extras.switch_page_button import switch_page
import numpy as np

st.set_page_config(
    page_title="JobBoards",
    page_icon="clipboard",
    initial_sidebar_state="expanded",
    layout="wide",
)

styles.load_css_file("styles/main.css")
st.header("🏢 Global Companies")
st.write("")


col1, col2 = st.sidebar.columns([2, 1])
with col1:
    if st.button("Custom Google Search", type="primary"):
        switch_page("Custom Google Search")

with col2:
    # st.markdown("###")

    if st.button("Home", type="primary"):
        switch_page("Home")


selected = option_menu(
    "",
    options=["Reviewed Global Companies", "1000+ Companies"],
    orientation="horizontal",
    icons=["cloud-upload", "list-task"],
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "15px"},
        "nav-link": {
            "font-size": "15px",
            "text-align": "left",
            "margin": "0px",
            "--hover-color": "#eee",
        },
        "nav-link-selected": {"background-color": "#029e16"},
    },
)

if selected == "Reviewed Global Companies":
    st.session_state.page_number_one = (
        0
        if "page_number_one" not in st.session_state
        else st.session_state.page_number_one
    )
    df = data_parser.read_data(selected)

    st.sidebar.subheader("**Filters**")

    st.sidebar.write("Select Number of Jobs to Display Per Page")
    num = st.sidebar.slider(
        "Number of Jobs Per Page",
        min_value=5,
        max_value=10,
        label_visibility="collapsed",
    )

    comp = df["Company"].unique()
    st.sidebar.write("**Select Company**")
    sel_comp = st.sidebar.multiselect(
        "Select Company", options=comp, label_visibility="collapsed"
    )

    if len(sel_comp) > 0:
        df = df[df["Company"].isin(sel_comp)]

    industry = df["Industry"].unique()
    ind_list = list(itertools.chain.from_iterable([x.split(",") for x in industry]))
    ind_list = np.unique(ind_list)
    
    st.sidebar.write("**Select Industry**")
    sel_ind = st.sidebar.multiselect(
        "Select Industry", options=ind_list, label_visibility="collapsed"
    )

    if sel_ind:
        matx = [df[df["Industry"].str.contains(i.strip())] for i in sel_ind]
        df = pd.concat(matx)

    df = df.reset_index()

    last_page = df.shape[0] // num

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    if col1.button("Previous Page ⬅️"):
        if st.session_state.page_number_one - 1 < 0:
            st.session_state.page_number_one = last_page
        else:
            st.session_state.page_number_one -= 1
    if col2.button("Next Page ➡️"):
        if st.session_state.page_number_one + 1 > last_page:
            st.session_state.page_number_one = 0
        else:
            st.session_state.page_number_one += 1

    if col3.button("First Page 🔝"):
        st.session_state.page_number_one = 0

    if col4.button("Last Page 🔙"):
        st.session_state.page_number_one = last_page

    st.caption(f"Page {st.session_state.page_number_one + 1} Out of {last_page}")

    start_index = st.session_state.page_number_one * num
    end_index = (
        (1 + st.session_state.page_number_one) * num
        if st.session_state.page_number_one != 0
        else num
    )

    df = df.iloc[start_index:end_index, :]

    for index, row in df.iterrows():
        with st.expander(
            label=f"**{index +1}**.  {row['Company'].title()}",
            expanded=False,
        ):
            st.markdown(f"Confirmed Locations: {row['Confirmed Locations']}")
            col1, col2, col3 = st.columns(3)
            col1.markdown(f"Status: {row['Remote/Relocation']}")
            col2.markdown(f"Internship Eligibility: {row['Internship Eligibility']}")
            col3.markdown(f"Additional Comments: {row['Comments']}")

            st.markdown(f"[Visit Website]({row['Link'].strip()})")
            components.iframe(f"{row['Link']}", height=500, scrolling=True)


elif selected == "1000+ Companies":
    st.session_state.page_number = (
        0 if "page_number" not in st.session_state else st.session_state.page_number
    )
    df = data_parser.read_data(selected)
    df = pd.read_csv("assets/remote_jobs.csv")
    df.fillna("Not Specified", inplace=True)

    st.sidebar.info(
        "Please Do Your Own Due Diligence Before Applying for Any of These Jobs"
    )

    st.sidebar.subheader("**Filters**")
    st.sidebar.write("Select Number of Jobs to Display Per Page")
    num = st.sidebar.slider(
        "Number of Jobs Per Page",
        min_value=5,
        max_value=20,
        label_visibility="collapsed",
    )

    comp = df["Company"].unique()
    st.sidebar.write("**Select Company**")
    sel_comp = st.sidebar.multiselect(
        "Select Company", options=comp, label_visibility="collapsed"
    )

    if len(sel_comp) > 0:
        df = df[df["Company"].isin(sel_comp)]

    locations = df["Location/Eligibility"].unique()
    locations = list(itertools.chain.from_iterable([x.split(",") for x in locations]))
    locations = np.unique(locations)

    st.sidebar.write("**Select Location**")
    sel_loc = st.sidebar.multiselect(
        "Select Location", options=locations, label_visibility="collapsed"
    )
    if sel_loc:
        matx = [df[df["Location/Eligibility"].str.contains(i.strip())] for i in sel_loc]
        df = pd.concat(matx)

    last_page = df.shape[0] // num

    df = df.reset_index()

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    if col1.button("Previous Page ⬅️"):
        if st.session_state.page_number - 1 < 0:
            st.session_state.page_number = last_page
        else:
            st.session_state.page_number -= 1
    if col2.button("Next Page ➡️"):
        if st.session_state.page_number + 1 > last_page:
            st.session_state.page_number = 0
        else:
            st.session_state.page_number += 1

    if col3.button("First Page 🔝"):
        st.session_state.page_number = 0

    if col4.button("Last Page 🔙"):
        st.session_state.page_number = last_page

    st.caption(f"Page {st.session_state.page_number + 1} Out of {last_page}")

    start_index = st.session_state.page_number * num
    end_index = (
        (1 + st.session_state.page_number) * num
        if st.session_state.page_number != 0
        else num
    )

    df = df.iloc[start_index:end_index, :]

    for index, row in df.iterrows():
        with st.expander(
            label=f"**{index +1}**.  {row['Company'].title()} ",
            expanded=False,
        ):
            st.write("#### More Info")
            st.markdown(f"*{row['About'].title()}*")
            st.markdown(f"Confirmed Locations: {row['Location/Eligibility'].title()}")

            options = [
                "Website",
                "Job portal",
                "Linkedin (jobs)",
            ]

            tab1, tab2, tab3 = st.tabs(tabs=options)
            with tab1:
                link = row[options[0]]
                if link != "Not Specified":
                    with st.spinner("Loading Web Page..."):
                        st.markdown(f"[Visit {options[0]}]({link})")
                        components.iframe(
                            f"{row[options[0]]}",
                            height=500,
                            scrolling=True,
                        )
                else:
                    st.write("No link available for Website")

            with tab2:
                link = row[options[1]]
                if link != "Not Specified":
                    with st.spinner("Loading Web Page..."):
                        st.markdown(f"[Visit {options[1]}]({link})")

                        components.iframe(
                            f"{link}",
                            height=500,
                            scrolling=True,
                        )
                else:
                    st.write("No link available for Job Portal.")
            with tab3:
                link = row[options[2]]
                if link != "Not Specified":
                    st.markdown(f"[Visit {options[2]}]({link})")
                else:
                    st.write("No link available for LinkedIn Jobs.")



footer.credit()
