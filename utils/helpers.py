"""
Helper Functions
Utility functions for the dashboard application.
"""


def format_phone_display(phone_number):
    """
    Format phone number for display.

    Args:
        phone_number (str): Full phone number

    Returns:
        str: Formatted phone number
    """
    if not phone_number:
        return ""

    # Show last 7 digits for brevity
    if len(phone_number) > 7:
        return "..." + phone_number[-7:]

    return phone_number


def truncate_text(text, max_length=30):
    """
    Truncate text to specified length.

    Args:
        text (str): Text to truncate
        max_length (int): Maximum length

    Returns:
        str: Truncated text with ellipsis if needed
    """
    if not text:
        return ""

    if len(text) <= max_length:
        return text

    return text[:max_length] + "..."


def validate_phone_format(phone_number):
    """
    Validate phone number format.

    Args:
        phone_number (str): Phone number to validate

    Returns:
        bool: True if valid format
    """
    if not phone_number:
        return False

    # Remove common formatting characters
    clean = phone_number.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

    # Should start with + and contain only digits after that
    if not clean.startswith('+'):
        return False

    digits = clean[1:]
    return digits.isdigit() and len(digits) >= 10
