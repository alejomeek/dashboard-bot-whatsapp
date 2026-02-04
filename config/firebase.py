import firebase_admin
from firebase_admin import credentials, firestore
import os
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Path to service account credentials
CREDENTIALS_PATH = PROJECT_ROOT / "firebase-service-account.json"

# Initialize Firebase Admin SDK
def initialize_firebase():
    """
    Initialize Firebase Admin SDK with service account credentials.
    Only initializes once, subsequent calls return existing app.
    """
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(str(CREDENTIALS_PATH))
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
