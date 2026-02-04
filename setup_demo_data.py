#!/usr/bin/env python3
"""
Setup Demo Data Script
Creates sample conversations to test the dashboard.
"""

from services.firebase_service import add_message, update_conversation_mode, mark_resolved
from datetime import datetime
import time


def create_demo_conversations():
    """Create demo conversations for testing."""

    print("="*60)
    print("  CREATING DEMO CONVERSATIONS")
    print("="*60)

    # Conversation 1: Active, Bot mode
    print("\n[1/4] Creating conversation: +573001234567")
    phone1 = "+573001234567"

    messages1 = [
        ('user', 'Hola, busco rompecabezas de 1000 piezas'),
        ('bot', 'Claro! Tenemos varios modelos. ¿Qué temática prefieres?'),
        ('user', 'Paisajes naturales'),
        ('bot', 'Te recomiendo:\n1. Montañas nevadas - $45.000\n2. Playa tropical - $42.000'),
    ]

    for from_type, text in messages1:
        add_message(phone1, from_type, text)
        time.sleep(0.1)

    print(f"   ✓ Added {len(messages1)} messages")

    # Conversation 2: Active, Human mode (escalated)
    print("\n[2/4] Creating conversation: +573119876543")
    phone2 = "+573119876543"

    messages2 = [
        ('user', 'Necesito factura de mi compra #12345'),
        ('bot', 'Por favor espera un momento, te contacto con un asesor'),
        ('user', 'Ok, gracias'),
    ]

    for from_type, text in messages2:
        add_message(phone2, from_type, text)
        time.sleep(0.1)

    # Escalate to human
    update_conversation_mode(phone2, 'human')
    print(f"   ✓ Added {len(messages2)} messages")
    print(f"   ✓ Escalated to human mode")

    # Conversation 3: Active, Human mode with human response
    print("\n[3/4] Creating conversation: +573155551234")
    phone3 = "+573155551234"

    messages3 = [
        ('user', '¿Tienen envío a Medellín?'),
        ('bot', 'Sí, hacemos envíos a toda Colombia'),
        ('user', '¿Cuánto demora?'),
        ('bot', 'Un momento, te contacto con un asesor para darte información precisa'),
        ('user', 'Perfecto'),
        ('human', 'Hola! El envío a Medellín demora 2-3 días hábiles y tiene un costo de $8.000'),
    ]

    for from_type, text in messages3:
        add_message(phone3, from_type, text)
        time.sleep(0.1)

    update_conversation_mode(phone3, 'human')
    print(f"   ✓ Added {len(messages3)} messages")
    print(f"   ✓ Set to human mode")

    # Conversation 4: Resolved
    print("\n[4/4] Creating conversation: +573007654321")
    phone4 = "+573007654321"

    messages4 = [
        ('user', '¿Tienen juegos de mesa?'),
        ('bot', 'Sí, tenemos una gran variedad. ¿Buscas algo específico?'),
        ('user', 'No, solo preguntaba. Gracias'),
        ('bot', 'De nada! Cualquier cosa estamos para ayudarte'),
    ]

    for from_type, text in messages4:
        add_message(phone4, from_type, text)
        time.sleep(0.1)

    mark_resolved(phone4)
    print(f"   ✓ Added {len(messages4)} messages")
    print(f"   ✓ Marked as resolved")

    # Summary
    print("\n" + "="*60)
    print("  DEMO DATA CREATED SUCCESSFULLY")
    print("="*60)
    print("\nConversations created:")
    print(f"  1. {phone1} - Bot mode, Active")
    print(f"  2. {phone2} - Human mode, Active (escalated)")
    print(f"  3. {phone3} - Human mode, Active (with human response)")
    print(f"  4. {phone4} - Bot mode, Resolved")
    print("\nYou can now run the dashboard:")
    print("  streamlit run app.py")
    print("="*60)


if __name__ == "__main__":
    try:
        create_demo_conversations()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
