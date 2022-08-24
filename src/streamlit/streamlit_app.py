"""Streamlit Module"""
import random

import pandas as pd

import streamlit as st
from src.sparql_utils.utils import query_sparql

PATH_TO_QUERY = "queries/countries_query.txt"


@st.cache()
def load_data_from_sparql_query(path_to_query) -> pd.DataFrame:
    return query_sparql(path_to_query)


country_dataframe = load_data_from_sparql_query(PATH_TO_QUERY)


country = random.choice(list(country_dataframe.country))
