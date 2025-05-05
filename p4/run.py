from dotenv import load_dotenv
import os

load_dotenv()  # This must be before create_app()

from flask_app import create_app

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
app = create_app()
