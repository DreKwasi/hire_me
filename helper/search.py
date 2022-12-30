from googleapiclient.discovery import build
import streamlit as st
from functools import reduce
import json
import helper.call_func as call
from helper.db import update_user_entries, call_user_entries


cred = st.secrets["credentials"]
service = build(
    "customsearch",
    "v1",
    developerKey=cred["key"],
    cache_discovery=False,
)
service_call = service.cse().siterestrict()

# counter = call.load_counter()
# query = call.load_query()
# prev_res = call.load_items()


def run_search(
    roles,
    locations,
    exclude_locations,
    date: str,
    next_page=False,
    start_num=0,
    **kwargs,
):
    
    counter, query, prev_res = call_user_entries()
    exclude_locations = [f"-{x}" for x in exclude_locations]
    search_term = f"""({reduce(lambda x,y: x + " OR " + y, roles)}) AND  \n
                    ({reduce (lambda x,y: x + " OR " + y, locations)})\n
                    {"" if len(exclude_locations) ==0 else
                    reduce(lambda x,y: x + " " + y, exclude_locations)} after:{date} 
                """

    if next_page:
        results = service_call.list(
            q=search_term,
            cx=cred["search_engine_id"],
            start=start_num,
        ).execute()
        
        prev_res.extend(results["items"])
        

        counter["search_count"] += 1
        # call.save_counter(counter)

        # call.save_query(results["queries"])

        update_user_entries(
            request_entries=prev_res, search_query=results["queries"], counter=counter
        )
        

        return prev_res, counter

    else:
        results = service_call.list(
            q=search_term,
            cx=cred["search_engine_id"],
        ).execute()
        try:
            with open("assets/res.json", "w") as f:
                json.dump(results, f)

            counter["search_count"] += 1

            # call.save_counter(counter)

            # call.save_query(results["queries"])

            update_user_entries(
                request_entries=results["items"].copy(),
                search_query=results["queries"].copy(),
                counter=counter.copy(),
            )

            return results["items"].copy(), counter, results["queries"].copy()
        
        except KeyError:
            st.info(
                "Include More Keywords (Try Using A Longer Date Range). No Job Posts Found"
            )
