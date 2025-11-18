import joblib
import json
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import Dict, List
import numpy as np
from nltk.stem import PorterStemmer
import re
import pandas as pd
from inference.voting_classifier.consts import Consts

CONST = Consts()
SW_DEFAULT = "default.json"
SW_EXTRA = "index.json"
TF_IDF_FILE = "tf_idf.joblib"


# Transformar dataframe em lista de textos
def turn_df_into_text(df: pd.DataFrame):
    rows_text = []
    for _, row in df.iterrows():
        rows_text.append(" ".join(row.fillna("").astype(str)))

    return rows_text


# Carregar stopwords default nltk + inseridas manualmente
def load_stopwords(
    stopwords_path=CONST.stopwords_path / SW_EXTRA,
    default_sw_path=CONST.stopwords_path / SW_DEFAULT,
    extra_sw: List = None,
    allow_extra_sw=False,  # permissão de inserir stowords encontradas manualmente
    batch_sw=2,
) -> List[str]:

    default_stopwords = []
    stopwords = []

    with open(default_sw_path, "r") as file:
        default_stopwords = json.load(file)["english_stopwords"]

    if allow_extra_sw:
        with open(stopwords_path, "r") as file:
            extra_sw_json = json.load(file)

            for k, v in extra_sw_json.items():
                if int(k) != batch_sw:
                    stopwords.extend(v)
                else:
                    break

    if extra_sw:
        stopwords.extend(extra_sw)

    return [default_stopwords, stopwords]


# Carregar Tf-idf vectorizer
def load_tf_idf(
    tf_idf_path=CONST.models_path / TF_IDF_FILE,
) -> TfidfVectorizer:

    return joblib.load(tf_idf_path)


# Limpar texto retornando lista com tokens stemmatizados
def preprocess_text(text: str) -> List[str]:
    stopwords, extra_stopwords = load_stopwords()
    stemmer = PorterStemmer()
    regex_words = r"[^A-Za-zÀ-ÖØ-öø-ÿ\s]+"
    regex_spaces = r"\s+"

    text = re.sub(regex_words, "", text)
    text = re.sub(regex_spaces, " ", text).strip()

    text = [
        stemmer.stem(word)
        for word in text.lower().split()
        if word not in stopwords and len(word) > 2
    ]

    if len(extra_stopwords) > 0:
        text = [token for token in text if token not in extra_stopwords]

    return text


# Transforma o texto pré-processado em um vetor (representação numérica)
def vectorize_text(text: str):
    tf_idf = load_tf_idf()

    return tf_idf.transform(text).toarray()


# Preprocessamento completo, recebe texto e retorna vetor
def preprocess(text: str) -> np.array:
    preprocessed_text = preprocess_text(text)
    preprocessed_text = " ".join(preprocessed_text)

    return vectorize_text([preprocessed_text])
