"""
Firebase Configuration Module
This module is preserved for compatibility with existing code.
The actual Firebase initialization is handled in services/firebase_service.py
"""
import streamlit as st
from config.settings import get_firebase_credentials


def initialize_firebase():
    """
    Initialize Firebase Admin SDK.
    This function is preserved for backward compatibility.
    The actual initialization is done in FirebaseService class.
    """
    try:
        from services.firebase_service import FirebaseService
        firebase = FirebaseService()
        return firebase
    except Exception as e:
        st.error(f"Error initializing Firebase: {str(e)}")
        return None


def get_firestore_client():
    """
    Get Firestore client.
    This function is preserved for backward compatibility.
    """
    try:
        from services.firebase_service import FirebaseService
        firebase = FirebaseService()
        return firebase.get_db()
    except Exception as e:
        st.error(f"Error getting Firestore client: {str(e)}")
        return None
