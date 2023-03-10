import streamlit as st
import helper.call_func as call
import streamlit_authenticator as st_auth
from streamlit_option_menu import option_menu
from show_home import show
from helper import db


st.set_page_config(
    page_title="JobBoards",
    page_icon="clipboard",
    initial_sidebar_state="expanded",
    layout="centered",
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

if "authentication_status" in st.session_state and st.session_state["authentication_status"] == True:
    options = ["Home Page"]
else:
    options = ["Login", "Register"]

selected = option_menu(menu_title="", options=options, orientation="horizontal")

user_creds = db.get_all_user_details()
cookie = st.secrets["cookie"]
preauth = st.secrets["preauthorized"]
creds = {"usernames": user_creds}


authenticator = st_auth.Authenticate(
    credentials=creds,
    cookie_name=cookie["name"],
    key=cookie["key"],
    cookie_expiry_days=cookie["expiry_days"],
    preauthorized=preauth,
)


if selected == "Login":
    (
        st.session_state["name"],
        st.session_state["authentication_status"],
        st.session_state["username"],
    ) = authenticator.login("Login", "main")

    if st.session_state["authentication_status"]:
        st.header(f'Welcome {st.session_state["name"]}')
        options = ["Home Page"]

    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")

    elif st.session_state["authentication_status"] == None:
        st.warning("Please enter your username and password")


elif selected == "Register":
    try:
        if authenticator.register_user("Register user", preauthorization=False):
            previous_users = list(creds["usernames"].keys())
            db.create_user(
                usernames=creds["usernames"],
            )
            st.success("User registered successfully. Please Log In")
    except Exception as e:
        st.error(e)


elif selected == "Home Page":
    st.header(f'Welcome {st.session_state["name"]} :grinning:')
    show()
    authenticator.logout("Logout", "main")
