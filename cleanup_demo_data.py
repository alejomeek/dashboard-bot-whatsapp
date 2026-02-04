#!/usr/bin/env python3
"""
Cleanup Demo Data Script
Removes sample conversations created for testing.
"""

from services.firebase_service import delete_conversation


def cleanup_demo_conversations():
    """Delete demo conversations."""

    print("="*60)
    print("  CLEANING UP DEMO CONVERSATIONS")
    print("="*60)

    demo_phones = [
        "+573001234567",
        "+573119876543",
        "+573155551234",
        "+573007654321"
    ]

    print("\nDeleting conversations...")

    for phone in demo_phones:
        result = delete_conversation(phone)
        if result:
            print(f"   ✓ Deleted: {phone}")
        else:
            print(f"   ⚠ Not found: {phone}")

    print("\n" + "="*60)
    print("  CLEANUP COMPLETED")
    print("="*60)


if __name__ == "__main__":
    try:
        cleanup_demo_conversations()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
