from inference.voting_classifier.main import predicitons
import pandas as pd
import numpy as np
import os

FILE_NAME_PATTERN = "new_insert_data_"


def retrain_model(df: pd.DataFrame, threshold=0.99, num_iters=1):
    """
    Re-treinar modelo baseado nos novos dados de predição
    Caso a probabilidade seja maior ou igual a do corte,
    novos dados são inseridos para treino.
    """

    df = df.copy()

    for i in range(num_iters):
        preds = predicitons(df)
        idxs, _predicitons = np.where(preds > threshold, axis=1)

        if len(idxs) == 0:
            break

        new_X = df[idxs]
        new_y = _predicitons.squeeze()

        # carregar modelo
        # pegar dados anteriores
        # inserir novos dados e atualizar df da função
        # retreinar modelo com novos dados
