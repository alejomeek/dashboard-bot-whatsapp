"""
WhatsApp Service Layer
Send messages via WhatsApp Cloud API.
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# WhatsApp API credentials
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_ID')

# WhatsApp Cloud API endpoint
WHATSAPP_API_URL = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages"


def send_message(phone_number, text):
    """
    Send a text message via WhatsApp Cloud API.

    Args:
        phone_number (str): Recipient phone number (E.164 format, e.g., "+573001234567")
        text (str): Message text to send

    Returns:
        dict: Response with success status and details
            - success (bool): True if message sent successfully
            - message_id (str): WhatsApp message ID if successful
            - error (str): Error message if failed
    """
    try:
        # Validate inputs
        if not phone_number or not text:
            return {
                'success': False,
                'error': 'Phone number and text are required'
            }

        # Check if credentials are configured
        if not WHATSAPP_TOKEN or WHATSAPP_TOKEN == 'your_whatsapp_token':
            return {
                'success': False,
                'error': 'WhatsApp API credentials not configured in .env file'
            }

        if not WHATSAPP_PHONE_ID or WHATSAPP_PHONE_ID == 'your_phone_id':
            return {
                'success': False,
                'error': 'WhatsApp Phone ID not configured in .env file'
            }

        # Clean phone number (remove spaces, dashes, etc.)
        clean_phone = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

        # Ensure phone number starts with '+'
        if not clean_phone.startswith('+'):
            clean_phone = '+' + clean_phone

        # Prepare request headers
        headers = {
            'Authorization': f'Bearer {WHATSAPP_TOKEN}',
            'Content-Type': 'application/json'
        }

        # Prepare request payload
        payload = {
            'messaging_product': 'whatsapp',
            'recipient_type': 'individual',
            'to': clean_phone,
            'type': 'text',
            'text': {
                'preview_url': False,
                'body': text
            }
        }

        # Send request to WhatsApp Cloud API
        print(f"[WhatsApp Service] Sending message to {clean_phone}...")
        response = requests.post(
            WHATSAPP_API_URL,
            headers=headers,
            json=payload,
            timeout=10
        )

        # Check response status
        if response.status_code == 200:
            response_data = response.json()
            message_id = response_data.get('messages', [{}])[0].get('id', '')

            print(f"[WhatsApp Service] Message sent successfully. ID: {message_id}")
            return {
                'success': True,
                'message_id': message_id,
                'phone_number': clean_phone
            }
        else:
            error_data = response.json()
            error_message = error_data.get('error', {}).get('message', 'Unknown error')

            print(f"[WhatsApp Service] Error sending message: {error_message}")
            return {
                'success': False,
                'error': error_message,
                'status_code': response.status_code
            }

    except requests.exceptions.Timeout:
        error_msg = 'Request timeout - WhatsApp API did not respond in time'
        print(f"[WhatsApp Service] {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }

    except requests.exceptions.ConnectionError:
        error_msg = 'Connection error - Could not reach WhatsApp API'
        print(f"[WhatsApp Service] {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }

    except Exception as e:
        error_msg = f'Unexpected error: {str(e)}'
        print(f"[WhatsApp Service] {error_msg}")
        return {
            'success': False,
            'error': error_msg
        }


def validate_phone_number(phone_number):
    """
    Validate phone number format.

    Args:
        phone_number (str): Phone number to validate

    Returns:
        dict: Validation result
            - valid (bool): True if valid
            - clean_number (str): Cleaned phone number
            - error (str): Error message if invalid
    """
    try:
        if not phone_number:
            return {
                'valid': False,
                'error': 'Phone number is required'
            }

        # Clean phone number
        clean_phone = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

        # Ensure phone number starts with '+'
        if not clean_phone.startswith('+'):
            clean_phone = '+' + clean_phone

        # Basic validation: should be at least 10 digits (excluding '+')
        digits_only = clean_phone.replace('+', '')
        if not digits_only.isdigit():
            return {
                'valid': False,
                'error': 'Phone number should contain only digits'
            }

        if len(digits_only) < 10:
            return {
                'valid': False,
                'error': 'Phone number too short (minimum 10 digits)'
            }

        return {
            'valid': True,
            'clean_number': clean_phone
        }

    except Exception as e:
        return {
            'valid': False,
            'error': f'Validation error: {str(e)}'
        }


def get_api_status():
    """
    Check if WhatsApp API credentials are configured.

    Returns:
        dict: Status information
            - configured (bool): True if credentials are set
            - token_set (bool): True if token is configured
            - phone_id_set (bool): True if phone ID is configured
    """
    token_set = WHATSAPP_TOKEN and WHATSAPP_TOKEN != 'your_whatsapp_token'
    phone_id_set = WHATSAPP_PHONE_ID and WHATSAPP_PHONE_ID != 'your_phone_id'

    return {
        'configured': token_set and phone_id_set,
        'token_set': token_set,
        'phone_id_set': phone_id_set
    }
