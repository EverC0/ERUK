from flask_app import create_app
import os
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"  
app = create_app()