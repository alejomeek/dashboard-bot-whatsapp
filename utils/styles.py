"""
Custom CSS Styles
Styling definitions for the dashboard application.
"""

THEMES = {
    'light': {
        'bg_app': '#f5f7fa',
        'bg_sidebar': '#ffffff',
        'border_color': '#e1e8ed',
        'text_h1': '#1a202c',
        'text_h2': '#2d3748',
        'text_h3': '#4a5568',
        'text_body': '#4a5568',
        'btn_secondary_bg': '#f7fafc',
        'btn_secondary_border': '#e2e8f0',
        'btn_secondary_text': '#4a5568',
        'btn_secondary_hover': '#edf2f7',
        'input_bg': '#ffffff',
        'input_border': '#e2e8f0',
        'metric_value': '#2d3748',
        'metric_label': '#718096',
        'expander_header': '#f7fafc',
        'expander_hover': '#edf2f7',
        'message_user_bg': 'linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%)',
        'message_user_text': '#2d3748',
        'message_bot_bg': 'linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%)',
        'message_bot_text': '#1565c0',
        'message_human_bg': 'linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%)',
        'message_human_text': '#2e7d32',
        'conv_hover': '#f7fafc',
        'conv_selected_bg': '#eff6ff',
        'conv_selected_border': '#3b82f6',
        'scrollbar_track': '#f1f1f1',
        'scrollbar_thumb': '#cbd5e0',
        'scrollbar_thumb_hover': '#a0aec0',
        'alert_success_bg': '#f0fdf4',
        'alert_success_border': '#22c55e',
        'alert_success_text': '#166534',
        'alert_error_bg': '#fef2f2',
        'alert_error_border': '#ef4444',
        'alert_error_text': '#991b1b',
        'alert_warning_bg': '#fffbeb',
        'alert_warning_border': '#f59e0b',
        'alert_warning_text': '#92400e',
        'alert_info_bg': '#eff6ff',
        'alert_info_border': '#3b82f6',
        'alert_info_text': '#1e40af',
    },
    'dark': {
        'bg_app': '#0e1117',
        'bg_sidebar': '#262730',
        'border_color': '#4a4a4a',
        'text_h1': '#fafafa',
        'text_h2': '#e0e0e0',
        'text_h3': '#c0c0c0',
        'text_body': '#c0c0c0',
        'btn_secondary_bg': '#262730',
        'btn_secondary_border': '#4a4a4a',
        'btn_secondary_text': '#e0e0e0',
        'btn_secondary_hover': '#333333',
        'input_bg': '#262730',
        'input_border': '#4a4a4a',
        'metric_value': '#fafafa',
        'metric_label': '#a0a0a0',
        'expander_header': '#262730',
        'expander_hover': '#333333',
        'message_user_bg': 'linear-gradient(135deg, #333333 0%, #2c2c2c 100%)',
        'message_user_text': '#e0e0e0',
        'message_bot_bg': 'linear-gradient(135deg, #1e3a8a 0%, #172554 100%)',
        'message_bot_text': '#bfdbfe',
        'message_human_bg': 'linear-gradient(135deg, #064e3b 0%, #065f46 100%)',
        'message_human_text': '#a7f3d0',
        'conv_hover': '#333333',
        'conv_selected_bg': '#1e293b',
        'conv_selected_border': '#60a5fa',
        'scrollbar_track': '#262730',
        'scrollbar_thumb': '#4a4a4a',
        'scrollbar_thumb_hover': '#666666',
        'alert_success_bg': '#064e3b',
        'alert_success_border': '#059669',
        'alert_success_text': '#d1fae5',
        'alert_error_bg': '#450a0a',
        'alert_error_border': '#dc2626',
        'alert_error_text': '#fecaca',
        'alert_warning_bg': '#451a03',
        'alert_warning_border': '#d97706',
        'alert_warning_text': '#fde68a',
        'alert_info_bg': '#172554',
        'alert_info_border': '#2563eb',
        'alert_info_text': '#bfdbfe',
    }
}

def get_custom_css(theme_name='light'):
    """
    Get custom CSS for the application based on the selected theme.

    Args:
        theme_name (str): Theme name ('light' or 'dark')

    Returns:
        str: CSS styles as string
    """
    if theme_name not in THEMES:
        theme_name = 'light'
    
    t = THEMES[theme_name]

    return f"""
    <style>
    /* Global Styles */
    .stApp {{
        background-color: {t['bg_app']};
    }}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: {t['bg_sidebar']};
        border-right: 1px solid {t['border_color']};
    }}

    section[data-testid="stSidebar"] .stMarkdown {{
        padding: 0.5rem 0;
    }}

    /* Main Content Area */
    .main .block-container {{
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }}

    /* Headers */
    h1 {{
        color: {t['text_h1']};
        font-weight: 700;
        margin-bottom: 0.5rem;
    }}

    h2 {{
        color: {t['text_h2']};
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }}

    h3 {{
        color: {t['text_h3']};
        font-weight: 600;
        margin-top: 1rem;
    }}
    
    p, li, small, span {{
        color: {t['text_body']};
    }}

    /* Buttons */
    .stButton > button {{
        border-radius: 8px;
        font-weight: 500;
        transition: all 0.2s ease;
        border: none;
    }}

    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }}

    .stButton > button:active {{
        transform: translateY(0);
    }}

    /* Primary Buttons */
    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }}

    .stButton > button[kind="primary"]:hover {{
        background: linear-gradient(135deg, #5568d3 0%, #6a3f8f 100%);
    }}

    /* Secondary Buttons */
    .stButton > button[kind="secondary"] {{
        background-color: {t['btn_secondary_bg']};
        border: 1px solid {t['btn_secondary_border']};
        color: {t['btn_secondary_text']};
    }}

    .stButton > button[kind="secondary"]:hover {{
        background-color: {t['btn_secondary_hover']};
        border-color: #cbd5e0;
    }}

    /* Text Input & Text Area */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {{
        background-color: {t['input_bg']};
        color: {t['text_body']};
        border-radius: 8px;
        border: 2px solid {t['input_border']};
        padding: 0.75rem;
        transition: border-color 0.2s ease;
    }}

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {{
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }}

    /* Checkboxes */
    .stCheckbox {{
        padding: 0.25rem 0;
    }}

    .stCheckbox > label {{
        font-weight: 500;
        color: {t['text_body']};
    }}

    /* Metrics */
    [data-testid="stMetricValue"] {{
        font-size: 1.5rem;
        font-weight: 700;
        color: {t['metric_value']};
    }}

    [data-testid="stMetricLabel"] {{
        font-size: 0.875rem;
        font-weight: 600;
        color: {t['metric_label']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}

    /* Success Messages */
    .stSuccess {{
        background-color: {t['alert_success_bg']};
        border-left: 4px solid {t['alert_success_border']};
        padding: 1rem;
        border-radius: 8px;
        color: {t['alert_success_text']};
    }}

    /* Error Messages */
    .stError {{
        background-color: {t['alert_error_bg']};
        border-left: 4px solid {t['alert_error_border']};
        padding: 1rem;
        border-radius: 8px;
        color: {t['alert_error_text']};
    }}

    /* Warning Messages */
    .stWarning {{
        background-color: {t['alert_warning_bg']};
        border-left: 4px solid {t['alert_warning_border']};
        padding: 1rem;
        border-radius: 8px;
        color: {t['alert_warning_text']};
    }}

    /* Info Messages */
    .stInfo {{
        background-color: {t['alert_info_bg']};
        border-left: 4px solid {t['alert_info_border']};
        padding: 1rem;
        border-radius: 8px;
        color: {t['alert_info_text']};
    }}

    /* Dividers */
    hr {{
        margin: 1.5rem 0;
        border: none;
        border-top: 1px solid {t['border_color']};
    }}

    /* Expanders */
    .streamlit-expanderHeader {{
        background-color: {t['expander_header']};
        border-radius: 8px;
        font-weight: 600;
        color: {t['text_h2']};
    }}

    .streamlit-expanderHeader:hover {{
        background-color: {t['expander_hover']};
    }}

    /* Caption Text */
    .caption {{
        color: {t['metric_label']};
        font-size: 0.875rem;
    }}

    /* Spinner */
    .stSpinner > div {{
        border-color: #667eea !important;
    }}

    /* Hide Streamlit Branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}

    /* Custom Message Bubbles */
    .message-bubble {{
        padding: 12px 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        max-width: 75%;
        word-wrap: break-word;
        animation: fadeIn 0.3s ease-in;
    }}

    @keyframes fadeIn {{
        from {{
            opacity: 0;
            transform: translateY(10px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    .message-user {{
        background: {t['message_user_bg']};
        color: {t['message_user_text']};
        border-bottom-left-radius: 4px;
    }}

    .message-bot {{
        background: {t['message_bot_bg']};
        color: {t['message_bot_text']};
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }}

    .message-human {{
        background: {t['message_human_bg']};
        color: {t['message_human_text']};
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }}

    .message-header {{
        font-size: 0.75rem;
        font-weight: 600;
        opacity: 0.8;
        margin-bottom: 4px;
        display: flex;
        align-items: center;
        gap: 4px;
    }}

    .message-time {{
        font-size: 0.7rem;
        opacity: 0.6;
        margin-left: 8px;
    }}

    /* Status Badges */
    .status-badge {{
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin: 4px 0;
    }}

    .status-active {{
        background-color: #dcfce7;
        color: #166534;
    }}

    .status-resolved {{
        background-color: #e0e7ff;
        color: #3730a3;
    }}

    .status-escalated {{
        background-color: #fee2e2;
        color: #991b1b;
    }}

    /* Conversation Item Styling */
    .conversation-item {{
        padding: 12px;
        margin: 8px 0;
        border-radius: 8px;
        transition: all 0.2s ease;
        cursor: pointer;
    }}

    .conversation-item:hover {{
        background-color: {t['conv_hover']};
        transform: translateX(4px);
    }}

    .conversation-item-selected {{
        background-color: {t['conv_selected_bg']};
        border-left: 4px solid {t['conv_selected_border']};
    }}

    /* Loading States */
    .loading-overlay {{
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
    }}

    /* Scrollbar Styling */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}

    ::-webkit-scrollbar-track {{
        background: {t['scrollbar_track']};
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb {{
        background: {t['scrollbar_thumb']};
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: {t['scrollbar_thumb_hover']};
    }}

    /* Responsive Design */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}

        .message-bubble {{
            max-width: 85%;
        }}
    }}
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
