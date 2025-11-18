from dotenv import load_dotenv
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import json
import pandas as pd
import io
from inference.voting_classifier.consts import Consts

CONSTS = Consts()
SCOPES = ["https://www.googleapis.com/auth/drive"]


def load_google_credentials():
    with open("service_credentials.json", "r", encoding="utf8") as file:
        return json.load(file)


def load_necessary_credentials():
    load_dotenv()

    return {
        "folder_id": os.getenv("FOLDER_ID"),
        "scopes": SCOPES,
        "google_creds_json": load_google_credentials(),
    }


def load_file_name():
    """Last idx corresponde ao número do arquivo atual,
    o qual o novo arquivo deve ser salvo"""

    with open(CONSTS.last_idx_path, "r", encoding="utf-8") as file:
        content = file.read().strip()
        last_idx = int(content) if content else 0

    new_idx = last_idx + 1

    # Salva o novo índice
    with open(CONSTS.last_idx_path, "w", encoding="utf-8") as file:
        file.write(str(new_idx))

    # Ex.: "predicoes_1.csv"
    return f"{CONSTS.file_name_pattern}_{new_idx}.csv"


def get_service():
    google_creds = load_necessary_credentials()["google_creds_json"]
    # google_creds = json.loads(google_creds)
    creds = Credentials.from_service_account_info(google_creds, scopes=SCOPES)
    service = build("drive", "v3", credentials=creds)

    return service


def upload_dataframe(df: pd.DataFrame):
    service = get_service()

    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)

    # Carregamento de pasta local para registrar último csv listado e atualizar += 1
    file_name = load_file_name()
    folder_id = load_necessary_credentials()["folder_id"]

    file_metadata = {
        "name": file_name,
        "parents": [folder_id],
    }

    media = MediaIoBaseUpload(csv_buffer, mimetype="text/csv", resumable=True)

    return (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
