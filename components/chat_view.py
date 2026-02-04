"""
Chat View Component
Displays conversation messages and interaction controls.
"""

import streamlit as st
from datetime import datetime
from services.firebase_service import (
    get_conversation,
    update_conversation_mode,
    add_message,
    delete_conversation
)
from services.whatsapp_service import send_message
from utils.styles import get_message_html, get_status_badge_html


def format_message_time(timestamp):
    """
    Format message timestamp.
    
    Args:
        timestamp: datetime object or Firestore timestamp
        
    Returns:
        str: Formatted time (e.g., "11:30 AM")
    """
    try:
        if timestamp is None:
            return ""

        # Convert Firestore timestamp to datetime if needed
        dt = timestamp
        
        # If it's a Firestore Timestamp, convert to datetime
        if hasattr(dt, 'to_datetime'):
            dt = dt.to_datetime()
        
        # Check if naive (no timezone info), assume UTC and localize
        if dt.tzinfo is None:
            # We assume stored timestamps are in UTC if naive
            # Or handle as server local time if preferred, but usually databases store UTC
            pass
        
        # Basic conversion: Adjust UTC to Local Time (Colombia is UTC-5)
        # We'll use a simple timedelta adjustment for now to avoid pytz dependency if not installed
        # But ideally we'd use pytz: dt.astimezone(pytz.timezone('America/Bogota'))
        
        from datetime import timedelta
        # If it's UTC (tz-aware), convert to naive by subtracting 5 hours
        if dt.tzinfo is not None:
             # Convert to UTC-5 manually
             dt = dt - timedelta(hours=5)
        else:
             # If naive, we assume it was UTC but lost tzinfo, or check logic
             # In this case user says DB is 11:52PM (UTC-5) but UI shows 5:52AM (UTC)
             # So we need to subtract 5 hours from the display
             dt = dt - timedelta(hours=5)

        return dt.strftime("%I:%M %p")

    except Exception as e:
        print(f"[Chat View] Error formatting time: {e}")
        return ""


def render_message(message, index):
    """
    Render a single message with appropriate styling using custom CSS.

    Args:
        message (dict): Message data
        index (int): Message index for unique key
    """
    from_type = message.get('from', '')
    text = message.get('text', '')
    timestamp = message.get('timestamp')
    time_str = format_message_time(timestamp)

    # Use the styled HTML from styles module
    message_html = get_message_html(from_type, text, time_str)
    st.markdown(message_html, unsafe_allow_html=True)


def render_chat_view(phone_number):
    """
    Render the chat view for a conversation.

    Args:
        phone_number (str): Phone number of the conversation
    """
    if not phone_number:
        st.info("👈 Selecciona una conversación del sidebar")
        return

    # Get conversation data
    conversation = get_conversation(phone_number)

    if not conversation:
        st.error(f"No se encontró la conversación: {phone_number}")
        return

    # Header with conversation info
    col1, col2 = st.columns([3, 1])

    with col1:
        st.header(f"💬 Conversación: {phone_number}")

    with col2:
        # Delete conversation button
        if st.button("🗑️ Borrar", type="secondary", key="delete_btn"):
            st.session_state.show_delete_confirm = True

    # Show delete confirmation dialog
    if st.session_state.get('show_delete_confirm', False):
        st.warning("⚠️ ¿Estás seguro de que deseas borrar esta conversación?")
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            if st.button("✓ Sí, borrar", type="primary", key="confirm_delete"):
                if delete_conversation(phone_number):
                    st.success("✓ Conversación borrada")
                    st.session_state.selected_phone = None
                    st.session_state.show_delete_confirm = False
                    st.rerun()
                else:
                    st.error("Error al borrar la conversación")

        with col2:
            if st.button("✗ Cancelar", key="cancel_delete"):
                st.session_state.show_delete_confirm = False
                st.rerun()

    st.markdown("---")

    # Conversation metadata
    mode = conversation.get('mode', 'bot')
    status = conversation.get('status', 'active')
    messages = conversation.get('messages', [])

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Mensajes", len(messages))

    with col2:
        st.metric("Estado", status.upper())

    with col3:
        # Bot mode toggle
        is_bot_active = mode == 'bot'

        if is_bot_active:
            toggle_label = "Pausar Bot"
        else:
            toggle_label = "Reactivar Bot"

        st.metric("Modo", "")
        # Show status badge with custom styling
        badge_html = get_status_badge_html(status, mode)
        st.markdown(badge_html, unsafe_allow_html=True)

    st.markdown("---")

    # Bot mode toggle button
    col1, col2 = st.columns([1, 3])

    with col1:
        if st.button(toggle_label, type="primary", use_container_width=True, key="toggle_mode"):
            new_mode = 'bot' if mode == 'human' else 'human'
            if update_conversation_mode(phone_number, new_mode):
                st.success(f"✓ Modo cambiado a: {new_mode.upper()}")
                st.rerun()
            else:
                st.error("Error al cambiar el modo")

    st.markdown("---")

    # Message history
    st.subheader("📜 Historial de mensajes")

    if messages:
        # Create a scrollable container for messages
        message_container = st.container()

        with message_container:
            for idx, message in enumerate(messages):
                render_message(message, idx)

        # Scroll to bottom effect (shows newest messages)
        st.markdown("<div id='bottom'></div>", unsafe_allow_html=True)

    else:
        st.info("No hay mensajes en esta conversación")

    st.markdown("---")

    # Message input section
    st.subheader("✍️ Enviar respuesta")

    # Initialize message input in session state
    message_key = f"message_input_{phone_number}"
    if message_key not in st.session_state:
        st.session_state[message_key] = ""

    # Text area for message
    message_text = st.text_area(
        "Escribe tu respuesta...",
        value=st.session_state.get(message_key, ""),
        height=100,
        key=f"textarea_{phone_number}",
        placeholder="Escribe un mensaje para enviar al cliente..."
    )

    # Send button
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        send_button = st.button("📤 Enviar", type="primary", use_container_width=True, key="send_btn")

    with col2:
        clear_button = st.button("🗑️ Limpiar", use_container_width=True, key="clear_btn")

    # Handle clear button
    if clear_button:
        st.session_state[message_key] = ""
        st.rerun()

    # Handle send button
    if send_button:
        if not message_text or not message_text.strip():
            st.error("⚠️ Por favor escribe un mensaje antes de enviar")
        else:
            with st.spinner("Enviando mensaje..."):
                # Send via WhatsApp
                result = send_message(phone_number, message_text)

                if result['success']:
                    # Add message to Firebase
                    message_id = result.get('message_id', '')
                    add_message(phone_number, 'human', message_text, message_id)

                    # Auto-pause bot when human sends message
                    if mode == 'bot':
                        update_conversation_mode(phone_number, 'human')

                    # Clear input
                    st.session_state[message_key] = ""

                    st.success("✓ Mensaje enviado exitosamente")
                    st.rerun()

                else:
                    error_msg = result.get('error', 'Error desconocido')
                    st.error(f"❌ Error al enviar mensaje: {error_msg}")

                    # If credentials not configured, still save to Firebase
                    if 'not configured' in error_msg.lower():
                        st.warning("💡 Credenciales no configuradas. Guardando mensaje solo en Firebase...")
                        add_message(phone_number, 'human', message_text)

                        # Auto-pause bot
                        if mode == 'bot':
                            update_conversation_mode(phone_number, 'human')

                        st.session_state[message_key] = ""
                        st.info("✓ Mensaje guardado en Firebase (no enviado por WhatsApp)")
                        st.rerun()

    # Instructions
    with st.expander("ℹ️ Instrucciones"):
        st.markdown("""
        **Cómo usar el chat:**

        1. **Ver mensajes**: El historial muestra todos los mensajes de la conversación
           - 👤 Gris: Mensajes del cliente
           - 🤖 Azul: Respuestas del bot
           - 🧑 Verde: Respuestas humanas

        2. **Enviar mensaje**: Escribe tu respuesta y haz clic en "Enviar"
           - El mensaje se envía por WhatsApp al cliente
           - Se guarda en el historial
           - El bot se pausa automáticamente

        3. **Control del bot**:
           - **Bot Activo**: El bot responde automáticamente
           - **Bot Pausado**: Solo respuestas manuales (modo humano)
           - Usa el botón para alternar entre modos

        4. **Borrar conversación**: Usa el botón "Borrar" para eliminar permanentemente
        """)


def render_empty_state():
    """
    Render empty state when no conversation is selected.
    """
    st.info("👈 Selecciona una conversación del sidebar para comenzar")

    st.markdown("---")

    st.markdown("""
    ### 💬 Dashboard de Conversaciones WhatsApp

    **Funcionalidades:**

    - 📱 Ver todas las conversaciones activas
    - 💬 Responder manualmente a clientes
    - 🤖 Controlar cuándo el bot responde
    - 📊 Filtrar por estado y modo
    - 🔍 Buscar conversaciones

    **Primeros pasos:**

    1. Selecciona una conversación de la lista
    2. Revisa el historial de mensajes
    3. Escribe y envía tu respuesta
    4. El bot se pausa automáticamente
    """)
