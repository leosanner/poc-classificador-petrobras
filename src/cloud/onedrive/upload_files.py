
import requests
import msal
import streamlit as st
import pandas as pd
import io


def get_azure_credentials():
    if "azure-test" not in st.secrets:
        raise ValueError("Secrets 'azure-test' not found in st.secrets")
        
    azure_credentials = st.secrets["azure-test"]
    
    required_keys = ["TENANT_ID", "CLIENT_ID", "CLIENT_SECRET", "USER_UPN"]
    missing_keys = [key for key in required_keys if key not in azure_credentials]
    
    if missing_keys:
        raise ValueError(f"Missing keys in azure-test secrets: {missing_keys}")

    return {
        "tenant_id": azure_credentials["TENANT_ID"],
        "client_id": azure_credentials["CLIENT_ID"],
        "client_secret": azure_credentials["CLIENT_SECRET"],
        "user_upn": azure_credentials["USER_UPN"],
    }


@st.cache_data(ttl=3000)
def get_access_token():
    credentials = get_azure_credentials()
    tenant = credentials.get("tenant_id")

    authority = f"https://login.microsoftonline.com/{tenant}"
    app = msal.ConfidentialClientApplication(
        client_id=credentials.get("client_id"),
        authority=authority,
        client_credential=credentials.get("client_secret"),
    )

    scopes = ["https://graph.microsoft.com/.default"]
    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" not in result:
        raise RuntimeError(f"Erro em obter token: {result}")

    return result["access_token"]


def upload_file(file_bytes: bytes, file_name: str, content_type="text/csv"):
    credentials = get_azure_credentials()
    access_token = get_access_token()

    folder_path = st.secrets["azure-test"]["FOLDER_PATH"]

    path = f"{folder_path}/{file_name}"

    url = (
        "https://graph.microsoft.com/v1.0"
        f"/users/{credentials['user_upn']}/drive/root:/{path}:/content"
    )

    print(url)

    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": content_type}

    print(headers)

    response = requests.put(url, headers=headers, data=file_bytes)

    if response.status_code in (200, 201):
        return response.json()

    else:
        raise RuntimeError(f"Erro ({response.status_code}): {response.text}")


def encode_dataframe(df: pd.DataFrame) -> bytes:
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    csv_str = buffer.getvalue()

    return csv_str.encode("utf-8")


def upload_dataframe(df: pd.DataFrame, file_name: str = "teste_1.csv"):
    encoded_df = encode_dataframe(df)

    try:
        upload_file(encoded_df, file_name=file_name)
        return True

    except RuntimeError as e:
        print(f"Ocorreu um problema no upload do dataframe: {e}")

    return False
