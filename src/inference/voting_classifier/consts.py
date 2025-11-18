from pathlib import Path

OUTPUT = {0: "not eia", 1: "eia"}
ROOT = Path(__file__).parent.parent.parent
STOPWORDS_PATH = ROOT / "resources/voting_classifier/stopwords"
MODELS_PATH = ROOT / "models/voting_classifier"
FILE_NAME_PATTERN = "new_insert_data"
DATA_PATH = ROOT / "data/new_data"
LAST_IDX_PATH = ROOT / "data/last_idx.txt"


class Consts:
    def __init__(self):
        self.model_output = OUTPUT
        self.root = ROOT
        self.stopwords_path = STOPWORDS_PATH
        self.models_path = MODELS_PATH
        self.file_name_pattern = FILE_NAME_PATTERN
        self.data_path = DATA_PATH
        self.last_idx_path = LAST_IDX_PATH
