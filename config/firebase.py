import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Path to service account credentials (local)
CREDENTIALS_PATH = PROJECT_ROOT / "firebase-service-account.json"


def get_firebase_credentials():
    """
    Get Firebase credentials from Streamlit Cloud secrets or local file.

    Returns:
        credentials.Certificate: Firebase credentials object
    """
    try:
        # Try Streamlit Cloud secrets first
        import streamlit as st

        # Check if we're in Streamlit Cloud (secrets available)
        if hasattr(st, 'secrets'):
            try:
                if 'firebase' in st.secrets:
                    print("[Firebase] Using Streamlit Cloud secrets")

                    # Build credentials dict from secrets
                    cred_dict = {
                        "type": st.secrets["firebase"]["type"],
                        "project_id": st.secrets["firebase"]["project_id"],
                        "private_key_id": st.secrets["firebase"]["private_key_id"],
                        "private_key": st.secrets["firebase"]["private_key"],
                        "client_email": st.secrets["firebase"]["client_email"],
                        "client_id": st.secrets["firebase"]["client_id"],
                        "auth_uri": st.secrets["firebase"]["auth_uri"],
                        "token_uri": st.secrets["firebase"]["token_uri"],
                        "auth_provider_x509_cert_url": st.secrets["firebase"]["auth_provider_x509_cert_url"],
                        "client_x509_cert_url": st.secrets["firebase"]["client_x509_cert_url"],
                        "universe_domain": st.secrets["firebase"]["universe_domain"]
                    }

                    return credentials.Certificate(cred_dict)
            except Exception as secrets_error:
                # Secrets file doesn't exist or firebase key not found
                print(f"[Firebase] Streamlit secrets not configured: {secrets_error}")
                pass

    except (ImportError, KeyError, AttributeError) as e:
        # Streamlit not available or secrets not configured
        print(f"[Firebase] Streamlit not available: {e}")
        pass

    # Fall back to local JSON file
    print("[Firebase] Using local service account file")

    if not CREDENTIALS_PATH.exists():
        raise FileNotFoundError(
            f"Firebase credentials file not found at {CREDENTIALS_PATH}. "
            "Please ensure firebase-service-account.json exists or configure Streamlit secrets."
        )

    return credentials.Certificate(str(CREDENTIALS_PATH))


# Initialize Firebase Admin SDK
def initialize_firebase():
    """
    Initialize Firebase Admin SDK with service account credentials.
    Works in both local development and Streamlit Cloud.
    Only initializes once, subsequent calls return existing app.
    """
    if not firebase_admin._apps:
        try:
            cred = get_firebase_credentials()
            firebase_admin.initialize_app(cred)
            print("[Firebase] Initialized successfully")
        except Exception as e:
            print(f"[Firebase] Error initializing: {e}")
            raise
    return firebase_admin.get_app()

def get_db():
    """
    Get Firestore database instance.
    Initializes Firebase if not already initialized.

    Returns:
        firestore.Client: Firestore database client
    """
    initialize_firebase()
    return firestore.client()
