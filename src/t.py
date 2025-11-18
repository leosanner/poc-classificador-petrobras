from dotenv import load_dotenv
import os
import json

load_dotenv()

print(json.loads(os.getenv("GOOGLE_CREDS_JSON")))
