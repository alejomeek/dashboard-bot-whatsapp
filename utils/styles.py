"""
Custom CSS Styles
Styling definitions for the dashboard application.
"""

def get_custom_css():
    """
    Get custom CSS for the application.

    Returns:
        str: CSS styles as string
    """
    return """
    <style>
    /* Global Styles */
    .stApp {
        background-color: #f5f7fa;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e1e8ed;
    }

    section[data-testid="stSidebar"] .stMarkdown {
        padding: 0.5rem 0;
    }

    /* Main Content Area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Headers */
    h1 {
        color: #1a202c;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }

    h2 {
        color: #2d3748;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    h3 {
        color: #4a5568;
        font-weight: 600;
        margin-top: 1rem;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
        border: none;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }

    .stButton > button:active {
        transform: translateY(0);
    }

    /* Primary Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);
    }

    /* Secondary Buttons */
    .stButton > button[kind="secondary"] {
        background-color: #f7fafc;
        border: 1px solid #e2e8f0;
        color: #4a5568;
    }

    .stButton > button[kind="secondary"]:hover {
        background-color: #edf2f7;
        border-color: #cbd5e0;
    }

    /* Text Input & Text Area */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        transition: border-color 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }

    /* Checkboxes */
    .stCheckbox {
        padding: 0.25rem 0;
    }

    .stCheckbox > label {
        font-weight: 500;
        color: #4a5568;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.5rem;
        font-weight: 700;
        color: #2d3748;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.875rem;
        font-weight: 600;
        color: #718096;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Success Messages */
    .stSuccess {
        background-color: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1rem;
        border-radius: 8px;
    }

    /* Error Messages */
    .stError {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 8px;
    }

    /* Warning Messages */
    .stWarning {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
    }

    /* Info Messages */
    .stInfo {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
    }

    /* Dividers */
    hr {
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid #e2e8f0;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #f7fafc;
        border-radius: 8px;
        font-weight: 600;
        color: #2d3748;
    }

    .streamlit-expanderHeader:hover {
        background-color: #edf2f7;
    }

    /* Caption Text */
    .caption {
        color: #718096;
        font-size: 0.875rem;
    }

    /* Spinner */
    .stSpinner > div {
        border-color: #667eea !important;
    }

    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* Custom Message Bubbles */
    .message-bubble {
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        max-width: 75%;
        word-wrap: break-word;
        animation: fadeIn 0.3s ease-in;
    }

    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .message-user {
        background: linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%);
        color: #2d3748;
        border-bottom-left-radius: 4px;
    }

    .message-bot {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        color: #1565c0;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }

    .message-human {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        color: #2e7d32;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }

    .message-header {
        font-size: 0.75rem;
        font-weight: 600;
        opacity: 0.8;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 4px;
    }

    .message-time {
        font-size: 0.7rem;
        opacity: 0.6;
        margin-left: 8px;
    }

    /* Status Badges */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 4px 0;
    }

    .status-active {
        background-color: #dcfce7;
        color: #166534;
    }

    .status-resolved {
        background-color: #e0e7ff;
        color: #3730a3;
    }

    .status-escalated {
        background-color: #fee2e2;
        color: #991b1b;
    }

    /* Conversation Item Styling */
    .conversation-item {
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        transition: all 0.2s ease;
        cursor: pointer;
    }

    .conversation-item:hover {
        background-color: #f7fafc;
        transform: translateX(4px);
    }

    .conversation-item-selected {
        background-color: #eff6ff;
        border-left: 4px solid #3b82f6;
    }

    /* Loading States */
    .loading-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-color: rgba(255, 255, 255, 0.9);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }

    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb {
        background: #cbd5e0;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #a0aec0;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .message-bubble {
            max-width: 85%;
        }
    }
    </style>
    """


def get_message_html(from_type, text, timestamp):
    """
    Generate HTML for a styled message bubble.

    Args:
        from_type (str): Type of sender (user/bot/human)
        text (str): Message text
        timestamp (str): Formatted timestamp

    Returns:
        str: HTML string for the message
    """
    icons = {
        'user': '👤',
        'bot': '🤖',
        'human': '🧑'
    }

    labels = {
        'user': 'Cliente',
        'bot': 'Bot',
        'human': 'Humano'
    }

    bubble_class = f"message-bubble message-{from_type}"
    icon = icons.get(from_type, '💬')
    label = labels.get(from_type, 'Mensaje')

    # Escape HTML in text
    text_escaped = text.replace('<', '&lt;').replace('>', '&gt;')

    html = f"""
    <div class="{bubble_class}">
        <div class="message-header">
            <span>{icon} {label}</span>
            <span class="message-time">{timestamp}</span>
        </div>
        <div>{text_escaped}</div>
    </div>
    """

    return html


def get_status_badge_html(status, mode):
    """
    Generate HTML for a status badge.

    Args:
        status (str): Conversation status
        mode (str): Conversation mode

    Returns:
        str: HTML string for the badge
    """
    if mode == 'human' and status == 'active':
        badge_class = 'status-escalated'
        text = '🔴 Bot Pausado'
    elif status == 'resolved':
        badge_class = 'status-resolved'
        text = '✓ Resuelta'
    else:
        badge_class = 'status-active'
        text = '🟢 Bot Activo'

    return f'<span class="status-badge {badge_class}">{text}</span>'
