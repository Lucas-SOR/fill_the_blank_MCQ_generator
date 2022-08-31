"""Streamlit Module"""
import random
from typing import Dict, List

import pandas as pd

import streamlit as st
from src.generator.generator import Generator
from src.sparql_utils.utils import query_sparql

SICARA_ARTICLE_LINK = "https://www.sicara.fr/blog-technique"
SICARA_LOGO_LINK = "https://www.actuia.com/wp-content/uploads/2018/02/logo_sicara.png"
PATH_TO_MODEL = "s2v_models/s2v_old"
PATH_TO_QUERY = "queries/countries_query.txt"
TITLE = "Fundamentals of NLP with multi choice question generation"


@st.cache()
def load_data_from_sparql_query(path_to_query: str) -> pd.DataFrame:
    """
    Load the data using a sparql query
    Args:
        path_to_query (str): the path to the file containing the query

    Returns:
        pd.DataFrame: the formated data
    """
    return query_sparql(path_to_query)


def check_relevance_mcq(mcq: Dict, country: str) -> bool:
    """Return a bool assessing the relevance of the mcq

    Args:
        mcq (Dict): the mcq
        country (str): a string containing the country

    Returns:
        bool: True if the mcq is relevant, False else
    """
    if mcq:
        return mcq["answer"].lower() != country.lower()
    return False


def get_relevant_mcq(mcq_list: List, country: str) -> Dict:
    """
    Return an mcq which answer is not the country
    Args:
        mcq_list (List): the list of mcq
        country (str): the country name

    Returns:
        Dict: the mcq whish answer is not country
    """
    mcq_addapted_to_country = [
        mcq for mcq in mcq_list if check_relevance_mcq(mcq, country)
    ]
    return random.choice(mcq_addapted_to_country)


def display_question() -> None:
    """
    Compute the question and set the display session state to True
    """
    st.session_state.current_country = random.choice(
        list(country_dataframe.country_name)
    )
    current_country_abstract = country_dataframe[
        country_dataframe["country_name"] == st.session_state.current_country
    ]["country_abstract"].iloc[0]
    st.session_state.mcq = st.session_state.mcq_generator.generate_single_mcq(
        current_country_abstract,
    )
    while not (
        check_relevance_mcq(st.session_state.mcq, st.session_state.current_country)
    ):
        st.session_state.mcq = st.session_state.mcq_generator.generate_single_mcq(
            current_country_abstract,
        )
    st.session_state.sentence = st.session_state.mcq["sentence"]
    st.session_state.answer = st.session_state.mcq["answer"]
    st.session_state.distractors = st.session_state.mcq["distractors"]
    st.session_state.proposals = st.session_state.distractors + [
        st.session_state.answer
    ]
    random.shuffle(st.session_state.proposals)
    st.session_state.show_answer = False
    st.session_state.display = True


def show_answer() -> None:
    """
    Set the show_answer session state to True
    """
    st.session_state.show_answer = True


def validate_solution(answer_index: int):
    """
    Set the user_input value to answer index and show answer
    Args:
        answer_index (int): the index of the chosen solution
    """
    st.session_state.user_input = answer_index
    show_answer()


def hide_answer() -> None:
    """
    Set the show_answer session state to False
    """
    st.session_state.show_answer = False


country_dataframe = load_data_from_sparql_query(PATH_TO_QUERY)


if "display" not in st.session_state:
    st.session_state.display = False

if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

if "sentence" not in st.session_state:
    st.session_state.sentence = ""

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "distractors" not in st.session_state:
    st.session_state.distractors = []

if "proposals" not in st.session_state:
    st.session_state.proposals = []

if "current_country" not in st.session_state:
    st.session_state.current_country = ""

if "mcq" not in st.session_state:
    st.session_state.mcq = {}

if "mcq_generator" not in st.session_state:
    st.session_state.mcq_generator = Generator(path_to_model=PATH_TO_MODEL)

with st.sidebar:
    st.image(SICARA_LOGO_LINK)
    st.title(f"[{TITLE}]({SICARA_ARTICLE_LINK})")
    st.write("How to use this app:")
    st.write('- to generate a MCQ click on the "Generate country MCQ" button.')
    st.write(
        "- an MCQ will be displayed with 4 answers, click on one to see if it was the right one!"
    )
    st.write("- you can generate another MCQ by clicking on the button again.")

st.button("Generate country MCQ", on_click=display_question)

if st.session_state.display:
    st.write(f"Current country is {st.session_state.current_country}.")
    st.write(f"Fill the sentence : {st.session_state.sentence}")
    c1, c2 = st.columns(2)
    c1.button(
        str(0) + ". " + st.session_state.proposals[0],
        on_click=lambda: validate_solution(0),
    )
    c1.button(
        str(2) + ". " + st.session_state.proposals[2],
        on_click=lambda: validate_solution(2),
    )
    c2.button(
        str(1) + ". " + st.session_state.proposals[1],
        on_click=lambda: validate_solution(1),
    )
    c2.button(
        str(3) + ". " + st.session_state.proposals[3],
        on_click=lambda: validate_solution(3),
    )

    if st.session_state.show_answer:
        is_answer_true = (
            st.session_state.proposals[int(st.session_state.user_input)]
            == st.session_state.answer
        )
        if is_answer_true:
            st.write("Correct Answer !")
        else:
            st.write(f"Wrong Answer ! Correct Answer was : {st.session_state.answer}")
