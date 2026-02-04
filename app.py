#!/usr/bin/env python3
"""
Dashboard Bot WhatsApp - Main Application
Streamlit dashboard to manage WhatsApp bot conversations with manual intervention.

Author: Alejo
Project: Jugando y Educando WhatsApp Bot Management
"""

import streamlit as st
from config.firebase import initialize_firebase
from components.sidebar import render_sidebar
from components.chat_view import render_chat_view, render_empty_state
import utils.styles
import importlib
importlib.reload(utils.styles)
from utils.styles import get_custom_css


# Page configuration
st.set_page_config(
    page_title="Dashboard Bot WhatsApp",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize theme in session state
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Load custom CSS
st.markdown(get_custom_css(st.session_state.theme), unsafe_allow_html=True)


def initialize_app():
    """
    Initialize the application.
    Sets up Firebase connection and session state.
    """
    try:
        # Initialize Firebase
        initialize_firebase()

        # Initialize session state variables if not exist
        if 'selected_phone' not in st.session_state:
            st.session_state.selected_phone = None

        if 'app_initialized' not in st.session_state:
            st.session_state.app_initialized = True

    except Exception as e:
        st.error(f"Error inicializando la aplicación: {str(e)}")
        st.stop()


def render_header():
    """
    Render the main header of the application.
    """
    st.title("💬 Dashboard Bot WhatsApp")
    st.caption("Gestiona conversaciones y responde manualmente cuando sea necesario")
    st.markdown("---")


def render_footer():
    """
    Render the footer with app information.
    """
    st.markdown("---")
    st.caption("🤖 Dashboard Bot WhatsApp - Jugando y Educando | Desarrollado por Alejo")


def main():
    """
    Main application function.
    Orchestrates the entire dashboard interface.
    """
    # Initialize the app
    initialize_app()

    # Render sidebar (returns selected phone number)
    selected_phone = render_sidebar()

    # Main content area
    render_header()

    # Render chat view or empty state based on selection
    if selected_phone:
        render_chat_view(selected_phone)
    else:
        render_empty_state()

    # Footer
    render_footer()


if __name__ == "__main__":
    main()
