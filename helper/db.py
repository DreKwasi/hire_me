import streamlit as st
from deta import Deta

# Initialize Deta Key
deta_cred = st.secrets["db_credentials"]
deta = Deta(deta_cred["deta_key"])


def get_all_user_details():
    usernames = {}
    users = deta.Base("users")
    all_users_obj = users.fetch()
    users = all_users_obj.items
    for user in users:
        usernames[user["username"]] = user
    return usernames


def create_user(usernames):
    users = deta.Base("users")
    previous_users = users.fetch().items
    previous_usernames = [x["username"] for x in previous_users]

    # Use the difference() method to remove common elements
    usernames = {
        key: value for key, value in usernames.items() if key not in previous_usernames
    }

    key = list(usernames.keys())[0]
    insert_user = usernames[key]
    insert_user["username"] = key
    users.insert(insert_user)
    
    # Creating Row for Entries
    search_requests = deta.Base("search_requests")
    
    search_requests.insert(
            {
                "username": key,
                "request_entries": [],
                "search_query": {},
                "counter": {'search_count':0},
            }
        )


def call_user_entries():
    search_requests = deta.Base("search_requests")
    try:
        username = st.session_state['username']
        res = search_requests.fetch({"username": username}).items[0]
        return res['counter'], res['search_query'], res['request_entries']
    except Exception:
        st.write("Perform A Search")
        st.stop()
    

def update_user_entries(request_entries, search_query, counter):
    username = st.session_state["username"]
    search_requests = deta.Base("search_requests")
    # Check if user is already in search_requests table and get key
    
    try:
        res = search_requests.fetch({"username": username}).items[0]

        search_requests.put(
            {
                "username": username,
                "request_entries": request_entries,
                "search_query": search_query,
                "counter": counter,
            },
            key=res["key"],
        )
    except IndexError:
        search_requests.insert(
            {
                "username": username,
                "request_entries": request_entries,
                "search_query": search_query,
                "counter": counter,
            }
        )


def store_user_query(roles, locations):
    username = st.session_state["username"]
    keywords = deta.Base("keywords")
    keywords.insert(
        {
            "username": username,
            "location": {},
            "roles": {},
        }
    )
