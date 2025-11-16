"""
Checkout form component for collecting shipping and payment information.
"""
import streamlit as st
from typing import Dict, Any
from utils.validators import validate_address, validate_name, validate_email, validate_phone


def render_checkout_form(cart_items: list):
    """
    Render checkout form with shipping and payment information.
    
    Args:
        cart_items: List of cart items
    """
    if not cart_items:
        st.warning("Your cart is empty. Add items before checkout.")
        return
    
    checkout_step = st.session_state.get('checkout_step', 'shipping')
    
    if checkout_step == 'shipping':
        render_shipping_form()
    elif checkout_step == 'payment':
        render_payment_form()
    elif checkout_step == 'review':
        render_review_order()


def render_shipping_form():
    """Render shipping address form."""
    st.subheader("Shipping Information")
    
    with st.form("shipping_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input("First Name *", key="shipping_first_name")
            email = st.text_input("Email *", key="shipping_email")
            phone = st.text_input("Phone *", key="shipping_phone")
            street = st.text_input("Street Address *", key="shipping_street")
            city = st.text_input("City *", key="shipping_city")
        
        with col2:
            last_name = st.text_input("Last Name *", key="shipping_last_name")
            company = st.text_input("Company (optional)", key="shipping_company")
            apartment = st.text_input("Apartment, suite, etc. (optional)", key="shipping_apartment")
            state = st.text_input("State *", key="shipping_state")
            zip_code = st.text_input("Zip Code *", key="shipping_zip")
        
        country = st.selectbox("Country *", ["United States", "Canada", "Mexico"], key="shipping_country")
        
        submitted = st.form_submit_button("Continue to Payment", type="primary")
        
        if submitted:
            is_valid = True
            error_msg = None
            
            if not first_name or not last_name or not email or not phone or not street or not city or not state or not zip_code:
                is_valid = False
                error_msg = "Please fill in all required fields"
            
            if is_valid:
                email_valid, email_error = validate_email(email)
                if not email_valid:
                    st.error(email_error)
                    return
                
                st.session_state.shipping_info = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': email,
                    'phone': phone,
                    'company': company,
                    'street': street,
                    'apartment': apartment,
                    'city': city,
                    'state': state,
                    'zip_code': zip_code,
                    'country': country
                }
                
                st.session_state.checkout_step = 'payment'
                st.rerun()
            else:
                st.error(error_msg)


def render_payment_form():
    """Render payment information form."""
    st.subheader("Payment Information")
    
    if 'shipping_info' in st.session_state:
        with st.expander("Shipping Address", expanded=False):
            shipping = st.session_state.shipping_info
            st.write(f"{shipping.get('first_name')} {shipping.get('last_name')}")
            st.write(shipping.get('street'))
            if shipping.get('apartment'):
                st.write(shipping.get('apartment'))
            st.write(f"{shipping.get('city')}, {shipping.get('state')} {shipping.get('zip_code')}")
            st.write(shipping.get('country'))
    
    with st.form("payment_form"):
        payment_method = st.radio(
            "Payment Method",
            ["Credit/Debit Card", "PayPal", "Cash on Delivery"],
            key="payment_method"
        )
        
        if payment_method == "Credit/Debit Card":
            card_number = st.text_input("Card Number *", placeholder="1234 5678 9012 3456", key="card_number")
            
            col1, col2 = st.columns(2)
            with col1:
                expiry_date = st.text_input("Expiry Date (MM/YY) *", placeholder="12/25", key="expiry_date")
            with col2:
                cvv = st.text_input("CVV *", placeholder="123", type="password", key="cvv")
            
            cardholder_name = st.text_input("Cardholder Name *", key="cardholder_name")
        elif payment_method == "PayPal":
            st.info("You will be redirected to PayPal for payment after order confirmation.")
        else:
            st.info("Payment will be collected upon delivery.")
        
        agree_terms = st.checkbox("I agree to the terms and conditions *", key="agree_terms")
        
        submitted = st.form_submit_button("Review Order", type="primary")
        
        if submitted:
            if not agree_terms:
                st.error("You must agree to the terms and conditions")
                return
            
            if payment_method == "Credit/Debit Card":
                if not card_number or not expiry_date or not cvv or not cardholder_name:
                    st.error("Please fill in all payment fields")
                    return
            
            st.session_state.payment_info = {
                'method': payment_method,
                'card_number': card_number if payment_method == "Credit/Debit Card" else None,
                'expiry_date': expiry_date if payment_method == "Credit/Debit Card" else None,
                'cvv': cvv if payment_method == "Credit/Debit Card" else None,
                'cardholder_name': cardholder_name if payment_method == "Credit/Debit Card" else None
            }
            
            st.session_state.checkout_step = 'review'
            st.rerun()


def render_review_order():
    """Render order review and confirmation."""
    st.subheader("Review Your Order")
    
    from services.firebase_service import FirebaseService
    firebase = FirebaseService()
    cart_items = firebase.get_user_cart(st.session_state.user['uid'])
    
    st.write("**Items:**")
    for item in cart_items:
        st.write(f"- {item.get('name')} x{item.get('quantity')} - ${item.get('price', 0) * item.get('quantity', 1):.2f}")
    
    from utils.formatters import calculate_total
    totals = calculate_total(cart_items, tax_rate=0.08, shipping=5.99)
    
    st.write("**Order Summary:**")
    st.write(f"Subtotal: ${totals['subtotal']:.2f}")
    st.write(f"Tax: ${totals['tax']:.2f}")
    st.write(f"Shipping: ${totals['shipping']:.2f}")
    st.write(f"**Total: ${totals['total']:.2f}**")
    
    if 'shipping_info' in st.session_state:
        st.write("**Shipping Address:**")
        shipping = st.session_state.shipping_info
        st.write(f"{shipping.get('first_name')} {shipping.get('last_name')}")
        st.write(shipping.get('street'))
        if shipping.get('apartment'):
            st.write(shipping.get('apartment'))
        st.write(f"{shipping.get('city')}, {shipping.get('state')} {shipping.get('zip_code')}")
        st.write(shipping.get('country'))
        st.write(f"Phone: {shipping.get('phone')}")
    
    if 'payment_info' in st.session_state:
        st.write("**Payment Method:**")
        payment = st.session_state.payment_info
        st.write(payment.get('method'))
    
    if st.button("Place Order", type="primary", use_container_width=True):
        order_data = {
            'items': cart_items,
            'totals': totals,
            'shipping_info': st.session_state.shipping_info,
            'payment_info': st.session_state.payment_info
        }
        
        order_id = firebase.create_order(st.session_state.user['uid'], order_data)
        
        if order_id:
            firebase.clear_cart(st.session_state.user['uid'])
            
            if 'checkout_step' in st.session_state:
                del st.session_state.checkout_step
            if 'shipping_info' in st.session_state:
                del st.session_state.shipping_info
            if 'payment_info' in st.session_state:
                del st.session_state.payment_info
            
            st.success(f"Order placed successfully! Order ID: {order_id}")
            st.balloons()
            
            st.session_state.page = 'orders'
            st.rerun()
        else:
            st.error("Failed to place order. Please try again.")

