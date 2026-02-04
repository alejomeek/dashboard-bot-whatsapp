"""
Sidebar Component
Displays conversation list with filters, search, and status indicators.
"""

import streamlit as st
from datetime import datetime
from services.firebase_service import get_all_conversations


def format_timestamp(timestamp):
    """
    Format timestamp to human-readable format.

    Args:
        timestamp: datetime object or Firestore timestamp

    Returns:
        str: Formatted time string (e.g., "11:30 AM", "Yesterday", "Jan 15")
    """
    try:
        if timestamp is None:
            return ""

        # Convert Firestore timestamp to datetime if needed
        if hasattr(timestamp, 'replace'):
            dt = timestamp
        else:
            dt = timestamp
        
        # Adjust for Timezone (UTC to UTC-5 for Colombia)
        from datetime import timedelta
        
        # If naive (no tz), assume it's UTC or whatever DB stored
        # If aware, confirm logic. Assuming DB sends UTC and we want UTC-5
        dt = dt - timedelta(hours=5)

        # Remove timezone info for comparison if present (make naive for calc)
        if hasattr(dt, 'replace') and dt.tzinfo is not None:
            dt = dt.replace(tzinfo=None)

        now = datetime.now()
        diff = now - dt

        # Today - show time
        if diff.days == 0:
            return dt.strftime("%I:%M %p")

        # Yesterday
        elif diff.days == 1:
            return "Ayer"

        # This week - show day name
        elif diff.days < 7:
            days = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']
            return days[dt.weekday()]

        # Older - show date
        else:
            return dt.strftime("%d %b")

    except Exception as e:
        print(f"[Sidebar] Error formatting timestamp: {e}")
        return ""


def get_last_message_preview(conversation, max_length=30):
    """
    Get preview of last message in conversation.

    Args:
        conversation (dict): Conversation data
        max_length (int): Maximum length of preview

    Returns:
        str: Message preview
    """
    try:
        messages = conversation.get('messages', [])
        if not messages:
            return "Sin mensajes"

        # Get last message
        last_message = messages[-1]
        text = last_message.get('text', '')

        # Truncate if too long
        if len(text) > max_length:
            return text[:max_length] + "..."

        return text

    except Exception as e:
        print(f"[Sidebar] Error getting message preview: {e}")
        return ""


def get_status_indicator(conversation):
    """
    Get status indicator emoji based on conversation mode.

    Args:
        conversation (dict): Conversation data

    Returns:
        str: Emoji indicator
    """
    mode = conversation.get('mode', 'bot')
    status = conversation.get('status', 'active')

    # Red dot for human mode or escalated
    if mode == 'human':
        return "🔴"

    # Gray for resolved
    if status == 'resolved':
        return "⚪"

    # White dot for normal bot mode
    return "⚪"


def render_conversation_item(conversation, is_selected=False):
    """
    Render a single conversation item in the sidebar.

    Args:
        conversation (dict): Conversation data
        is_selected (bool): Whether this conversation is selected

    Returns:
        str: Formatted conversation item text
    """
    phone = conversation.get('phone_number', '')
    indicator = get_status_indicator(conversation)
    preview = get_last_message_preview(conversation)
    timestamp = format_timestamp(conversation.get('lastMessage'))
    mode = conversation.get('mode', 'bot')
    status = conversation.get('status', 'active')

    # Bold text for human mode or unresolved
    is_bold = mode == 'human' and status == 'active'

    # Format phone number (show full number)
    display_phone = phone

    # Build conversation text
    if is_bold:
        conv_text = f"{indicator} **{display_phone}**"
    else:
        conv_text = f"{indicator} {display_phone}"

    return conv_text, preview, timestamp, mode


def render_sidebar():
    """
    Render the sidebar with conversation list, filters, and search.

    Returns:
        str: Selected phone number, or None if no selection
    """
    st.sidebar.title("💬 Conversaciones")

    # Theme Toggle
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'

    # Use a callback to update theme immediately
    def on_theme_change():
        st.session_state.theme = 'dark' if st.session_state.toggle_dark_mode else 'light'
    
    st.sidebar.toggle(
        "Modo Oscuro 🌙",
        value=(st.session_state.theme == 'dark'),
        key="toggle_dark_mode",
        on_change=on_theme_change
    )

    # Filters section
    st.sidebar.subheader("Filtros")

    # Initialize filter states in session state if not exists
    if 'filter_bot' not in st.session_state:
        st.session_state.filter_bot = True
    if 'filter_human' not in st.session_state:
        st.session_state.filter_human = True
    if 'filter_resolved' not in st.session_state:
        st.session_state.filter_resolved = False

    # Filter checkboxes
    filter_bot = st.sidebar.checkbox(
        "Bot activo",
        value=st.session_state.filter_bot,
        key="cb_filter_bot"
    )
    filter_human = st.sidebar.checkbox(
        "Humano respondiendo",
        value=st.session_state.filter_human,
        key="cb_filter_human"
    )
    filter_resolved = st.sidebar.checkbox(
        "Resueltas",
        value=st.session_state.filter_resolved,
        key="cb_filter_resolved"
    )

    # Update session state
    st.session_state.filter_bot = filter_bot
    st.session_state.filter_human = filter_human
    st.session_state.filter_resolved = filter_resolved

    # Search box
    st.sidebar.subheader("Buscar")
    search_term = st.sidebar.text_input(
        "Número de teléfono",
        placeholder="Buscar...",
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")

    # Build filters dict for Firebase query
    filters = {}

    # Apply search filter
    if search_term:
        filters['search'] = search_term

    # Get conversations from Firebase
    try:
        all_conversations = get_all_conversations(filters=filters)

        # Apply mode/status filters (client-side filtering)
        filtered_conversations = []

        for conv in all_conversations:
            mode = conv.get('mode', 'bot')
            status = conv.get('status', 'active')

            # Check if conversation matches filters
            should_include = False

            if status == 'resolved' and filter_resolved:
                should_include = True
            elif status == 'active':
                if mode == 'bot' and filter_bot:
                    should_include = True
                elif mode == 'human' and filter_human:
                    should_include = True

            if should_include:
                filtered_conversations.append(conv)

        # Display conversation count
        st.sidebar.caption(f"📊 {len(filtered_conversations)} conversaciones")

        # Initialize selected conversation in session state
        if 'selected_phone' not in st.session_state:
            st.session_state.selected_phone = None

        # Render conversation list
        if filtered_conversations:
            for conv in filtered_conversations:
                phone = conv.get('phone_number', '')
                conv_text, preview, timestamp, mode = render_conversation_item(conv)

                # Create a container for each conversation
                with st.sidebar.container():
                    # Use button for selection
                    is_selected = st.session_state.selected_phone == phone

                    # Button with conversation info
                    if st.button(
                        conv_text,
                        key=f"conv_{phone}",
                        use_container_width=True,
                        type="primary" if is_selected else "secondary"
                    ):
                        st.session_state.selected_phone = phone
                        st.rerun()

                    # Show preview and timestamp below button
                    col1, col2 = st.sidebar.columns([3, 1])
                    with col1:
                        st.caption(f'"{preview}"')
                    with col2:
                        st.caption(timestamp)

                    # Show mode badge
                    if mode == 'human':
                        st.sidebar.caption("🔴 Bot Pausado")

                    st.sidebar.markdown("---")

            return st.session_state.selected_phone

        else:
            st.sidebar.info("No hay conversaciones que coincidan con los filtros")
            return None

    except Exception as e:
        st.sidebar.error(f"Error cargando conversaciones: {str(e)}")
        print(f"[Sidebar] Error loading conversations: {e}")
        return None


def get_selected_conversation():
    """
    Get the currently selected conversation phone number.

    Returns:
        str: Selected phone number, or None
    """
    return st.session_state.get('selected_phone', None)
