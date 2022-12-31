import streamlit as st
from helper import job_board_func
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="JobBoards",
    page_icon="clipboard",
    initial_sidebar_state="expanded",
    layout="wide",
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if "authentication_status" in st.session_state or "username" in st.session_state :

    if st.session_state["authentication_status"]:
        job_board_func.view_jobboard()
    
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")
    
    elif st.session_state["authentication_status"] == None:
        st.warning("Visit Home Screen To Login or Register")


else:
    login_btn = st.button("Login")
    if login_btn:
        switch_page("Home")
    st.warning("Visit Home Page To Login or Register")
