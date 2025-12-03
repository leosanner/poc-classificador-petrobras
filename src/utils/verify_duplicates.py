import re
from pathlib import Path
import pandas as pd

PARENT = Path(__file__).parent
DATA_PATH = PARENT.parent / "data/dataset.csv"


def tokenize_text(text: str) -> list[str]:
    regex_words = r"[.,!?;:]+"
    regex_spaces = r"\s+"

    text = re.sub(regex_words, "", text)
    text = re.sub(regex_spaces, " ", text).strip()

    return text.split()


def text_similarity(text1: str, text2: str) -> float:
    tokenized_1 = tokenize_text(text1)
    tokenized_2 = tokenize_text(text2)

    if (len(tokenized_1) == 0) or (len(tokenized_2) == 0):
        return 0

    token_match = 0

    for token in tokenized_1:
        if token in tokenized_2:
            token_match += 1

    return token_match / len(tokenized_2)


# Carregar conjunto de dados total retornando uma lista
def load_text_dataset() -> list[str]:
    df = pd.read_csv(DATA_PATH).fillna(" ")

    return list(df["Title"])


def verify_duplicates(new_text, threshold: float = 0.9):
    dataset_titles = load_text_dataset()
    idxs_relateded = []

    for idx, title in enumerate(dataset_titles):
        sim = text_similarity(new_text, title)

        if sim >= threshold:
            idxs_relateded.append([idx, sim])

    return idxs_relateded


def return_duplicated_elements(df: pd.DataFrame):
    """Funcão que retorna um dataframe contendo o títtulo do banco original com o dos novos dados de entrada, demonstrando possíveis arquivos existentes,
    Colunas: Título Banco || Título Recebido || Similaridade
    """
    data = {"titulo_banco": [], "titulo_recebido": [], "similaridade": []}

    df_titles = df["Title"].fillna(" ")
    df_dataset_titles = load_text_dataset()

    for title in df_titles:
        duplicates = verify_duplicates(title)

        if len(duplicates) > 0:
            for idx, sim in duplicates:
                data["titulo_banco"].append(df_dataset_titles[idx])
                data["titulo_recebido"].append(title)
                data["similaridade"].append(sim)

    return pd.DataFrame(data)
