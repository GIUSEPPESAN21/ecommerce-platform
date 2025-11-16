"""
Authentication service using Firebase Auth REST API.
Handles user login and registration.
"""
import streamlit as st
from typing import Optional, Dict, Any
import requests
from config.settings import get_firebase_api_key, get_firebase_project_id


class AuthService:
    """Service for handling user authentication via Firebase Auth REST API."""
    
    FIREBASE_AUTH_BASE_URL = "https://identitytoolkit.googleapis.com/v1/accounts"
    
    @staticmethod
    def _get_api_key() -> Optional[str]:
        """Get Firebase Web API Key."""
        api_key = get_firebase_api_key()
        
        # If no API key in secrets, try to get from project ID
        # Note: This requires the Web API Key to be configured in Streamlit secrets
        if not api_key:
            st.warning("⚠️ Firebase Web API Key not found. Please add 'firebase_api_key' to your Streamlit secrets.")
            st.info("💡 You can find your Web API Key in Firebase Console → Project Settings → General → Web API Key")
        
        return api_key
    
    @staticmethod
    def sign_up(email: str, password: str, display_name: str = None) -> Optional[Dict[str, Any]]:
        """
        Register a new user using Firebase Auth REST API.
        
        Args:
            email: User email
            password: User password
            display_name: Optional display name
            
        Returns:
            Dictionary with user info and idToken, or None on error
        """
        api_key = AuthService._get_api_key()
        if not api_key:
            return None
        
        try:
            url = f"{AuthService.FIREBASE_AUTH_BASE_URL}:signUp?key={api_key}"
            
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            
            if display_name:
                payload["displayName"] = display_name
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Create user document in Firestore
                from services.firebase_service import FirebaseService
                firebase = FirebaseService()
                
                user_data = {
                    'uid': data.get('localId'),
                    'email': email,
                    'display_name': display_name or email.split('@')[0],
                    'created_at': None,  # Will be set by Firestore
                    'cart': [],
                    'orders': [],
                    'addresses': []
                }
                
                # Try to save user data to Firestore (non-blocking)
                try:
                    db = firebase.get_db()
                    if db:
                        from datetime import datetime
                        user_data['created_at'] = datetime.now()
                        db.collection('users').document(data.get('localId')).set(user_data)
                except Exception:
                    pass  # Continue even if Firestore save fails
                
                return {
                    'uid': data.get('localId'),
                    'email': data.get('email'),
                    'display_name': display_name or data.get('displayName', email.split('@')[0]),
                    'idToken': data.get('idToken'),
                    'refreshToken': data.get('refreshToken')
                }
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                
                if 'EMAIL_EXISTS' in error_msg:
                    st.error("This email is already registered. Please sign in instead.")
                elif 'WEAK_PASSWORD' in error_msg:
                    st.error("Password is too weak. Please use a stronger password.")
                else:
                    st.error(f"Registration failed: {error_msg}")
                
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Network error during registration: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Error during registration: {str(e)}")
            return None
    
    @staticmethod
    def sign_in(email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Sign in user using Firebase Auth REST API.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            Dictionary with user info and idToken, or None on error
        """
        api_key = AuthService._get_api_key()
        if not api_key:
            return None
        
        try:
            url = f"{AuthService.FIREBASE_AUTH_BASE_URL}:signInWithPassword?key={api_key}"
            
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Get user display name from Firestore if available
                display_name = data.get('displayName', email.split('@')[0])
                
                try:
                    from services.firebase_service import FirebaseService
                    firebase = FirebaseService()
                    db = firebase.get_db()
                    if db:
                        user_doc = db.collection('users').document(data.get('localId')).get()
                        if user_doc.exists:
                            user_data = user_doc.to_dict()
                            display_name = user_data.get('display_name', display_name)
                except Exception:
                    pass
                
                return {
                    'uid': data.get('localId'),
                    'email': data.get('email'),
                    'display_name': display_name,
                    'idToken': data.get('idToken'),
                    'refreshToken': data.get('refreshToken')
                }
            else:
                error_data = response.json()
                error_msg = error_data.get('error', {}).get('message', 'Unknown error')
                
                if 'INVALID_PASSWORD' in error_msg or 'EMAIL_NOT_FOUND' in error_msg:
                    st.error("Invalid email or password. Please try again.")
                elif 'USER_DISABLED' in error_msg:
                    st.error("This account has been disabled.")
                else:
                    st.error(f"Sign in failed: {error_msg}")
                
                return None
                
        except requests.exceptions.RequestException as e:
            st.error(f"Network error during sign in: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Error during sign in: {str(e)}")
            return None
    
    @staticmethod
    def verify_token(id_token: str) -> Optional[Dict[str, Any]]:
        """
        Verify Firebase ID token.
        
        Args:
            id_token: Firebase ID token
            
        Returns:
            Decoded token data, or None if invalid
        """
        api_key = AuthService._get_api_key()
        if not api_key:
            return None
        
        try:
            url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={api_key}"
            
            payload = {
                "idToken": id_token
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                users = data.get('users', [])
                if users:
                    user = users[0]
                    return {
                        'uid': user.get('localId'),
                        'email': user.get('email'),
                        'display_name': user.get('displayName', user.get('email', '').split('@')[0])
                    }
            return None
        except Exception:
            return None

