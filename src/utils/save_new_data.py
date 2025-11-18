import os
from inference.voting_classifier.consts import Consts
import pandas as pd

CONSTS = Consts()


def save_new_file(df: pd.DataFrame):
    files = os.listdir(CONSTS.data_path)

    if not files:
        df.to_csv(f"{CONSTS.data_path / CONSTS.file_name_pattern}_0")
        return

    last_file = files[-1]
    last_num = int(last_file.split("_")[-1])

    print(last_file)
    print(last_num)

    df.to_csv(f"{CONSTS.data_path / CONSTS.file_name_pattern}_{last_num + 1}")
