"""Application settings and configuration management."""
import streamlit as st
from typing import Dict, Any, Optional
import base64
import json


def get_firebase_credentials() -> Optional[Dict[str, Any]]:
    """
    Retrieve Firebase credentials from Streamlit secrets.
    Handles both base64 encoded and direct JSON formats.
    """
    try:
        if 'firebase_credentials' in st.secrets:
            creds = st.secrets['firebase_credentials']
            
            # Check if credentials are in base64 format
            if 'service_account_base64' in creds:
                # Decode base64 string
                base64_string = creds['service_account_base64']
                decoded_bytes = base64.b64decode(base64_string)
                decoded_str = decoded_bytes.decode('utf-8')
                
                # Parse JSON
                cred_dict = json.loads(decoded_str)
                
                # Ensure 'type' field is present
                if 'type' not in cred_dict:
                    cred_dict['type'] = 'service_account'
                
                # Handle private key formatting (replace \n with actual newlines)
                if 'private_key' in cred_dict and isinstance(cred_dict['private_key'], str):
                    cred_dict['private_key'] = cred_dict['private_key'].replace('\\n', '\n')
                
                return cred_dict
            
            # Fallback: try direct dictionary format
            elif isinstance(creds, dict):
                cred_dict = dict(creds)
                
                # Ensure 'type' field is present
                if 'type' not in cred_dict:
                    cred_dict['type'] = 'service_account'
                
                # Handle private key formatting
                if 'private_key' in cred_dict and isinstance(cred_dict['private_key'], str):
                    cred_dict['private_key'] = cred_dict['private_key'].replace('\\n', '\n')
                
                return cred_dict
        
        return None
    except json.JSONDecodeError as e:
        st.error(f"Error parsing Firebase credentials JSON: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error loading Firebase credentials: {str(e)}")
        return None


def get_gemini_api_key() -> Optional[str]:
    """
    Retrieve Gemini API key from Streamlit secrets.
    Handles multiple possible key formats.
    """
    try:
        # Try new format: GEMINI_API_KEY at root level
        if 'GEMINI_API_KEY' in st.secrets:
            return st.secrets['GEMINI_API_KEY']
        
        # Try nested format: gemini.api_key
        if 'gemini' in st.secrets and 'api_key' in st.secrets['gemini']:
            return st.secrets['gemini']['api_key']
        
        # Try direct format: gemini_api_key
        if 'gemini_api_key' in st.secrets:
            return st.secrets['gemini_api_key']
        
        return None
    except Exception as e:
        st.error(f"Error loading Gemini API key: {str(e)}")
        return None

def get_firebase_api_key() -> Optional[str]:
    """
    Get Firebase Web API Key from Streamlit secrets.
    This is needed for Firebase Auth REST API.
    """
    try:
        # Try direct format
        if 'firebase_api_key' in st.secrets:
            return st.secrets['firebase_api_key']
        
        # Try nested format
        if 'firebase' in st.secrets and 'api_key' in st.secrets['firebase']:
            return st.secrets['firebase']['api_key']
        
        # Try in firebase_credentials
        if 'firebase_credentials' in st.secrets:
            creds = st.secrets['firebase_credentials']
            if 'api_key' in creds:
                return creds['api_key']
            if 'web_api_key' in creds:
                return creds['web_api_key']
        
        return None
    except Exception as e:
        return None


def get_firebase_project_id() -> Optional[str]:
    """Get Firebase project ID from credentials."""
    try:
        cred_dict = get_firebase_credentials()
        if cred_dict and 'project_id' in cred_dict:
            return cred_dict['project_id']
        return None
    except Exception:
        return None


def get_app_config() -> Dict[str, Any]:
    return {
        'app_name': 'E-Commerce Platform',
        'currency': 'USD',
        'currency_symbol': '$',
        'max_cart_items': 50,
        'max_product_images': 5,
        'products_per_page': 12,
        'storage_bucket': None,
    }
