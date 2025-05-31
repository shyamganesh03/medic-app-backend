from firebase_admin import credentials, initialize_app
from decouple import config


def initialize_firebase():
    firebaseConfig = {
    "type": "service_account",
    "project_id": config('PROJECT_ID'),
    "private_key_id": config('PRIVATE_KEY_ID'),
    "private_key": config('PRIVATE_KEY').replace('\\n', '\n'), 
    "client_email": config('CLIENT_EMAIL'),
    "client_id": config('CLIENT_ID'),
    "auth_uri": config('AUTH_URI'),
    "token_uri": config('TOKEN_URI'),
    "auth_provider_x509_cert_url": config('AUTH_PROVIDER_CERT_URL'),
    "client_x509_cert_url": config('CLIENT_CERT_URL'),
    "universe_domain": config('UNIVERSE_DOMAIN')
    }
    cred = credentials.Certificate(firebaseConfig)
    initialize_app(cred)
