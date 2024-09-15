from os import environ 
from dotenv import load_dotenv
import base64

if not environ.get("ENV"):
    # Load dotenv if not using environment variable
    load_dotenv(".env")

# Google Service Account credentials, base64-encoded
GSA_CREDENTIALS = environ.get("GSA_CREDENTIALS")
if GSA_CREDENTIALS: GSA_CREDENTIALS = base64.b64decode(GSA_CREDENTIALS).decode()
