import pandas as pd
import streamlit as st


@st.cache_data(show_spinner=False)
def read_data(selected):
    if selected == "1000+ Companies":
        df = pd.read_csv(f"assets/remote_jobs.csv")
        df.fillna("Not Specified", inplace=True)
    elif selected == "Reviewed Global Companies":
        df = pd.read_csv("assets/curated_jobs.csv", dtype={"Company": str})
        df["Comments"].fillna("", inplace=True)
        df.fillna("Not Specified", inplace=True)

    return df