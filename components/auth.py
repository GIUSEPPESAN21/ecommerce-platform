"""
Authentication components for login and registration.
"""
import streamlit as st
from utils.validators import validate_email, validate_password, validate_name


def render_login_form():
    """Render login form."""
    st.subheader("Sign In")
    
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        
        submitted = st.form_submit_button("Sign In", type="primary")
        
        if submitted:
            if not email or not password:
                st.error("Please enter both email and password")
                return
            
            email_valid, email_error = validate_email(email)
            if not email_valid:
                st.error(email_error)
                return
            
            # Authenticate using Firebase Auth REST API
            from services.auth_service import AuthService
            
            with st.spinner("Signing in..."):
                user_data = AuthService.sign_in(email, password)
            
            if user_data:
                # Store user in session state
                st.session_state.user = {
                    'uid': user_data['uid'],
                    'email': user_data['email'],
                    'display_name': user_data['display_name']
                }
                st.session_state.id_token = user_data.get('idToken')
                st.session_state.refresh_token = user_data.get('refreshToken')
                
                st.success(f"Welcome back, {user_data['display_name']}!")
                st.balloons()
                st.rerun()


def render_register_form():
    """Render registration form."""
    st.subheader("Create Account")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name *", key="register_first_name")
            email = st.text_input("Email *", key="register_email")
        
        with col2:
            last_name = st.text_input("Last Name *", key="register_last_name")
            phone = st.text_input("Phone (optional)", key="register_phone")
        
        password = st.text_input("Password *", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password *", type="password", key="register_confirm_password")
        
        agree_terms = st.checkbox("I agree to the terms and conditions *", key="register_agree_terms")
        
        submitted = st.form_submit_button("Create Account", type="primary")
        
        if submitted:
            errors = []
            
            if not first_name:
                errors.append("First name is required")
            elif not validate_name(first_name)[0]:
                errors.append(validate_name(first_name)[1])
            
            if not last_name:
                errors.append("Last name is required")
            elif not validate_name(last_name)[0]:
                errors.append(validate_name(last_name)[1])
            
            if not email:
                errors.append("Email is required")
            else:
                email_valid, email_error = validate_email(email)
                if not email_valid:
                    errors.append(email_error)
            
            if not password:
                errors.append("Password is required")
            else:
                password_valid, password_error = validate_password(password)
                if not password_valid:
                    errors.append(password_error)
            
            if password != confirm_password:
                errors.append("Passwords do not match")
            
            if not agree_terms:
                errors.append("You must agree to the terms and conditions")
            
            if errors:
                for error in errors:
                    st.error(error)
                return
            
            display_name = f"{first_name} {last_name}"
            
            # Register using Firebase Auth REST API
            from services.auth_service import AuthService
            
            with st.spinner("Creating account..."):
                user_data = AuthService.sign_up(email, password, display_name)
            
            if user_data:
                # Store user in session state and auto-login
                st.session_state.user = {
                    'uid': user_data['uid'],
                    'email': user_data['email'],
                    'display_name': user_data['display_name']
                }
                st.session_state.id_token = user_data.get('idToken')
                st.session_state.refresh_token = user_data.get('refreshToken')
                
                st.success(f"Account created successfully! Welcome, {display_name}!")
                st.balloons()
                st.rerun()

