"""Module providing sparql utils"""
from typing import Dict

import pandas as pd
from SPARQLWrapper import JSON, SPARQLWrapper

from src.sparql_utils.constants import DBPEDIA_URL


def sparql_to_df(results: Dict) -> pd.DataFrame:
    """
    This function transform a SPARQL result into a DataFrame
    Args:
        - results : the object returned by sparql.query().convert()
    Return:
        - data : The DataFrame
    """
    columns = results["head"]["vars"]
    sparql_dict = {}
    for col_name in columns:
        sparql_dict[col_name] = []

    for result in results["results"]["bindings"]:
        for col_name in columns:
            sparql_dict[col_name].append(result[col_name]["value"])

    return pd.DataFrame(sparql_dict)


def query_sparql(path_to_query: str) -> pd.DataFrame:
    """
    This function makes the SPARQL request to DBpedia to get the desired information
    Returns :
    - data : The DataFrame of countries information
    """
    sparql = SPARQLWrapper(DBPEDIA_URL)

    with open(path_to_query, encoding="utf-8") as file:
        query = file.read()
        sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data = sparql_to_df(results)
    return data
