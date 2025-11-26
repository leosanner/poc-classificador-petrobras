from inference.voting_classifier.predict import model_prediction
from inference.voting_classifier.preprocessing import preprocess, turn_df_into_text, load_tf_idf
import pandas as pd
import numpy as np
from typing import List


def preprocess_df(df: pd.DataFrame):
    text_df = turn_df_into_text(df)
    
    # Load TF-IDF once
    tf_idf = load_tf_idf()

    return np.vstack([preprocess(text, tf_idf=tf_idf) for text in text_df])


def predictions(
    df: pd.DataFrame, preprocess_fn=preprocess_df, prediction_fn=model_prediction
):
    """Precisa receber função de pré-processamento que retorne um array
    e função de predições que retorne o predict proba de cada uma"""

    preprocessed_df = preprocess_fn(df)
    preds = prediction_fn(preprocessed_df)

    return preds


def predictions_df(df: pd.DataFrame):
    preds = predictions(df)

    df_user = df.copy()
    df_user["prediction (eia)"] = np.argmax(preds, axis=1)

    df["prob_not_eia"] = preds[:, 0]
    df["prob_eia"] = preds[:, 1]

    return (df, df_user)
