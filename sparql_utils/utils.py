from sparql_utils.constants import DBPEDIA_URL
from SPARQLWrapper import SPARQLWrapper, JSON, XML
import pandas as pd


def sparql_to_df(results):
    """
    This function transform a SPARQL result into a DataFrame
    Args:
        - results : the object returned by sparql.query().convert()
    Return:
        - data : The DataFrame
    """
    columns = results["head"]["vars"]
    d = {}
    for col_name in columns:
        d[col_name] = []

    for result in results["results"]["bindings"]:
        for col_name in columns:
            d[col_name].append(result[col_name]["value"])

    return pd.DataFrame(d)


def query_sparql(path_to_query: str):
    """
    This function makes the SPARQL request to DBpedia to get the desired information
    Returns :
    - data : The DataFrame of countries information
    """
    sparql = SPARQLWrapper(DBPEDIA_URL)

    with open(path_to_query) as f:
        query = f.read()
        sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    data = sparql_to_df(results)
    return data
