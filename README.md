# fill_the_blank_MCQ_generator

[![Python](https://img.shields.io/badge/Python3.10.5-Python?style=for-the-badge&logo=Python)](https://www.python.org/downloads/release/python-3105/)

[![Formatter](https://img.shields.io/badge/Codestyle-Black-black?style=for-the-badge)](https://github.com/psf/black)

[![TypeChecker](https://img.shields.io/badge/%20type_checker-mypy-%231674b1?style=for-the-badge)](https://github.com/python/mypy)

[![Linter](https://img.shields.io/badge/Pylint-10.00/10-green?style=for-the-badge)](https://github.com/PyCQA/pylint)

[![ImportSorting](https://img.shields.io/badge/isort-checked-yellow?style=for-the-badge)](https://github.com/PyCQA/isort)

Illutration of an application of basic NLP tools discussed in the article [Fundamentals of NLP with multi choice question generation](https://www.sicara.fr/blog-technique).

## Pre-requisites

- Python 3.10.5

## Installation

After setting up the virtual env, downlad dependencies with poetry:

```
poetry install
```

Download the "en_core_web_sm" for spaCy using 
```
poetry run python -m spacy download en_core_web_sm
```

Finally, for the sense2vec model, here is the [link](https://github.com/explosion/sense2vec/releases/download/v1.0.0/s2v_reddit_2015_md.tar.gz) to download it. Please decompress the file and put the model in a `s2v_models` folder at the root of this repo. 

### Tree of the project

```
.
├── Makefile
├── README.md
├── poetry.lock
├── pyproject.toml
├── queries
│   └── countries_query.txt
├── s2v_models
│   └── s2v_old
│       ├── ...
│       ...
└── src
    ├── __init__.py
    ├── generator
    │   ├── __init__.py
    │   └── generator.py
    ├── sparql_utils
    │   ├── __init__.py
    │   ├── constants.py
    │   └── utils.py
    └── streamlit
        ├── __init__.py
        └── streamlit_app.py
```

## Usage

To open the Streamlit app please run:
```
poetry run streamlit run src/streamlit/streamlit_app.py 
```