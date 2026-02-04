"""
Firebase Service Layer
CRUD operations for conversations and messages in Firestore.
"""

from config.firebase import get_db
from datetime import datetime
from google.cloud.firestore_v1 import FieldFilter
import uuid


def get_all_conversations(filters=None):
    """
    Get all conversations from Firestore.

    Args:
        filters (dict, optional): Filter options
            - mode: "bot" | "human" | None
            - status: "active" | "resolved" | None
            - search: phone number search string

    Returns:
        list: List of conversation dictionaries with phone_number as key
    """
    try:
        db = get_db()
        conversations_ref = db.collection('conversations')

        # Apply filters if provided
        query = conversations_ref

        if filters:
            if filters.get('mode'):
                query = query.where(filter=FieldFilter('mode', '==', filters['mode']))
            if filters.get('status'):
                query = query.where(filter=FieldFilter('status', '==', filters['status']))

        # Get all documents
        docs = query.stream()

        conversations = []
        for doc in docs:
            data = doc.to_dict()
            data['phone_number'] = doc.id

            # Apply search filter (phone number)
            if filters and filters.get('search'):
                if filters['search'].lower() not in doc.id.lower():
                    continue

            conversations.append(data)

        # Sort by lastMessage (newest first)
        conversations.sort(key=lambda x: x.get('lastMessage', datetime.min), reverse=True)

        return conversations

    except Exception as e:
        print(f"[Firebase Service] Error getting conversations: {e}")
        return []


def get_conversation(phone_number):
    """
    Get a single conversation with all messages.

    Args:
        phone_number (str): Phone number (document ID)

    Returns:
        dict: Conversation data with messages, or None if not found
    """
    try:
        db = get_db()
        doc_ref = db.collection('conversations').document(phone_number)
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            data['phone_number'] = phone_number
            return data
        else:
            return None

    except Exception as e:
        print(f"[Firebase Service] Error getting conversation {phone_number}: {e}")
        return None


def update_conversation_mode(phone_number, mode):
    """
    Update conversation mode (bot or human).

    Args:
        phone_number (str): Phone number (document ID)
        mode (str): "bot" or "human"

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if mode not in ['bot', 'human']:
            print(f"[Firebase Service] Invalid mode: {mode}. Must be 'bot' or 'human'")
            return False

        db = get_db()
        doc_ref = db.collection('conversations').document(phone_number)

        update_data = {
            'mode': mode,
            'lastMessage': datetime.now()
        }

        # If switching to human mode, set escalatedAt
        if mode == 'human':
            update_data['escalatedAt'] = datetime.now()

        doc_ref.set(update_data, merge=True)
        print(f"[Firebase Service] Updated mode to '{mode}' for {phone_number}")
        return True

    except Exception as e:
        print(f"[Firebase Service] Error updating conversation mode: {e}")
        return False


def add_message(phone_number, from_type, text, message_id=None):
    """
    Add a message to conversation history.

    Args:
        phone_number (str): Phone number (document ID)
        from_type (str): "user" | "bot" | "human"
        text (str): Message text
        message_id (str, optional): WhatsApp message ID (auto-generated if not provided)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        if from_type not in ['user', 'bot', 'human']:
            print(f"[Firebase Service] Invalid from_type: {from_type}")
            return False

        db = get_db()
        doc_ref = db.collection('conversations').document(phone_number)

        # Generate message ID if not provided
        if not message_id:
            message_id = str(uuid.uuid4())

        # Create message object
        message = {
            'from': from_type,
            'text': text,
            'timestamp': datetime.now(),
            'messageId': message_id
        }

        # Check if conversation exists
        doc = doc_ref.get()

        if doc.exists:
            # Append message to existing conversation
            doc_ref.update({
                'messages': firestore.ArrayUnion([message]),
                'lastMessage': datetime.now()
            })
        else:
            # Create new conversation with first message
            doc_ref.set({
                'mode': 'bot',
                'status': 'active',
                'lastMessage': datetime.now(),
                'escalatedAt': None,
                'messages': [message]
            })

        print(f"[Firebase Service] Added message from '{from_type}' to {phone_number}")
        return True

    except Exception as e:
        print(f"[Firebase Service] Error adding message: {e}")
        return False


def delete_conversation(phone_number):
    """
    Delete a conversation from Firestore.

    Args:
        phone_number (str): Phone number (document ID)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        db = get_db()
        doc_ref = db.collection('conversations').document(phone_number)

        # Check if conversation exists
        if doc_ref.get().exists:
            doc_ref.delete()
            print(f"[Firebase Service] Deleted conversation: {phone_number}")
            return True
        else:
            print(f"[Firebase Service] Conversation not found: {phone_number}")
            return False

    except Exception as e:
        print(f"[Firebase Service] Error deleting conversation: {e}")
        return False


def mark_resolved(phone_number):
    """
    Mark a conversation as resolved.

    Args:
        phone_number (str): Phone number (document ID)

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        db = get_db()
        doc_ref = db.collection('conversations').document(phone_number)

        doc_ref.set({
            'status': 'resolved',
            'lastMessage': datetime.now()
        }, merge=True)

        print(f"[Firebase Service] Marked conversation as resolved: {phone_number}")
        return True

    except Exception as e:
        print(f"[Firebase Service] Error marking conversation as resolved: {e}")
        return False


# Import firestore for ArrayUnion
from google.cloud import firestore
