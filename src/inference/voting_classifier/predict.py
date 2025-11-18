import joblib
from pathlib import Path
from pydantic import BaseModel
from typing import List, Union
from sklearn.ensemble import VotingClassifier
import numpy as np
from inference.voting_classifier.consts import Consts

CONSTS = Consts()
MODEL_FILE = "model_soft.joblib"


# Carregar modelo treinado
def load_model(
    model_path=CONSTS.models_path / MODEL_FILE,
) -> VotingClassifier:

    return joblib.load(model_path)


# Gerar predições com modelo (probabilidade de classes [0; 1])
def model_prediction(arr: np.array, model_path=None) -> np.array:
    if model_path:
        model = load_model(model_path)
    else:
        model = load_model()

    return model.predict_proba(arr)


def model_classification(text: str, threshold=0.99) -> int:
    prediction = model_prediction(text)

    if prediction[-1] >= threshold:
        return CONSTS.model_output[1]

    return CONSTS.model_output[0]
