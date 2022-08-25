"""Module providing sparql utils"""
from typing import Any, Dict

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
    return pd.DataFrame(
        {
            col_name: [
                result[col_name]["value"] for result in results["results"]["bindings"]
            ]
            for col_name in results["head"]["vars"]
        }
    )


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

    data = sparql_to_df(results)  # type: ignore
    return data
