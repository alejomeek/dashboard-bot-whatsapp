import firebase_admin
from firebase_admin import credentials, firestore
import os


def get_firebase_credentials():
    """
    Get Firebase credentials from Streamlit Cloud secrets or local file.

    Returns:
        credentials.Certificate: Firebase credentials object
    """
    # Try Streamlit Cloud secrets first
    try:
        import streamlit as st

        print("[Firebase] Checking for Streamlit secrets...")

        # Check if secrets are configured
        if hasattr(st, 'secrets') and 'firebase' in st.secrets:
            print("[Firebase] ✓ Using Streamlit Cloud secrets")

            # Build credentials dict from secrets
            firebase_creds = {
                "type": st.secrets["firebase"]["type"],
                "project_id": st.secrets["firebase"]["project_id"],
                "private_key_id": st.secrets["firebase"]["private_key_id"],
                "private_key": st.secrets["firebase"]["private_key"],
                "client_email": st.secrets["firebase"]["client_email"],
                "client_id": st.secrets["firebase"]["client_id"],
                "auth_uri": st.secrets["firebase"].get("auth_uri", "https://accounts.google.com/o/oauth2/auth"),
                "token_uri": st.secrets["firebase"].get("token_uri", "https://oauth2.googleapis.com/token"),
                "auth_provider_x509_cert_url": st.secrets["firebase"].get("auth_provider_x509_cert_url", "https://www.googleapis.com/oauth2/v1/certs"),
                "client_x509_cert_url": st.secrets["firebase"].get("client_x509_cert_url", ""),
                "universe_domain": st.secrets["firebase"].get("universe_domain", "googleapis.com")
            }

            return credentials.Certificate(firebase_creds)

    except Exception as e:
        print(f"[Firebase] Could not use Streamlit secrets: {e}")

    # Fallback to local JSON file
    json_path = os.path.join(os.path.dirname(__file__), '..', 'firebase-service-account.json')

    if os.path.exists(json_path):
        print(f"[Firebase] ✓ Using local service account file: {json_path}")
        return credentials.Certificate(json_path)
    else:
        raise FileNotFoundError(
            f"Firebase credentials file not found at {json_path}. "
            "Please ensure firebase-service-account.json exists or configure Streamlit secrets."
        )


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
