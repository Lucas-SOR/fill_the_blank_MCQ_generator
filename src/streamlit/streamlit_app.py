import random

import pandas as pd

import streamlit as st
from sparql_utils.utils import query_sparql

path_to_query = "queries/countries_query.txt"


@st.cache()
def load_data_from_sparql_query(path_to_query) -> pd.DataFrame:
    return query_sparql(path_to_query)


country_dataframe = load_data_from_sparql_query(path_to_query)


country = random.choice(list(country_dataframe.country))
