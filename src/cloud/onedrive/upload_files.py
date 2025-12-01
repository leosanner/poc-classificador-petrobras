import datetime
import streamlit as st
import pandas as pd
import io
from azure.storage.blob import BlobServiceClient

TOML_BLOB_STORAGE = "azure-blob-storage"


# Carregar credencias para upload
def load_azure_credentials():
    azure_toml = TOML_BLOB_STORAGE
    connection_str_toml = "AZURE_STORAGE_CONNECTION_STRING"
    container_name_toml = "AZURE_STORAGE_CONTAINER_NAME"
    azure_credentials = st.secrets[azure_toml]

    connection_string = azure_credentials.get(connection_str_toml)
    if not connection_string:
        raise ValueError("Connection string não foi encontrada")

    container_name = azure_credentials.get(container_name_toml)

    return {
        "connection_string": connection_string,
        "container_name": container_name,
    }


def load_client():
    azure_credentials = load_azure_credentials()
    blob_service_client = BlobServiceClient.from_connection_string(
        azure_credentials.get("connection_string")
    )
    container_client = blob_service_client.get_container_client(
        azure_credentials.get("container_name")
    )

    return container_client


def generate_blob_name(folder_name: str = None):
    user_id = st.secrets[TOML_BLOB_STORAGE]["USER_ID"]
    time = datetime.datetime.now(tz=datetime.UTC)

    if not folder_name:
        folder_name = time.strftime("%Y-%m-%d")

    timestamp = time.strftime("%Y%m%d_%H%M%S")

    file_name = f"dataframe_{timestamp}.csv"
    blob_name = f"{user_id}/{folder_name}/{file_name}"

    return blob_name


def encode_dataframe(df: pd.DataFrame) -> bytes:
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    csv_str = buffer.getvalue()

    return csv_str.encode("utf-8")


def upload_dataframe(df: pd.DataFrame):
    encoded_df = encode_dataframe(df)
    file_name = generate_blob_name()
    container_client = load_client()

    try:
        blob_client = container_client.get_blob_client(file_name)
        blob_client.upload_blob(encoded_df, overwrite=True)

    except RuntimeError as e:
        print(f"Ocorreu um problema no upload do dataframe: {e}")

    return False
