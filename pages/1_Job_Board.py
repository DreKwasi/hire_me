import streamlit as st
from helper import job_board_func


if "authentication_status" in st.session_state or "username" in st.session_state :

    if st.session_state["authentication_status"]:
        job_board_func.view_jobboard()
    
    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")
    
    elif st.session_state["authentication_status"] == None:
        st.warning("Visit Home Screen To Login or Register")


else:
    st.warning("Visit Home Screen To Login or Register")