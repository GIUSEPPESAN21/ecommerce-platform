"""
Cart summary component for displaying cart items and totals.
"""
import streamlit as st
from typing import List, Dict, Any
from utils.formatters import format_currency, calculate_total


def render_cart_summary(cart_items: List[Dict[str, Any]]):
    """
    Render cart summary with items and totals.
    
    Args:
        cart_items: List of cart item dictionaries
    """
    if not cart_items:
        st.info("Your cart is empty.")
        return
    
    st.subheader("Shopping Cart")
    
    for i, item in enumerate(cart_items):
        with st.container():
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            
            with col1:
                if item.get('image'):
                    st.image(item['image'], width=80)
                st.write(f"**{item.get('name', 'Product')}**")
            
            with col2:
                st.write(format_currency(item.get('price', 0)))
            
            with col3:
                # Create callback with closure to capture item and user info
                # The callback receives the new value as first argument automatically
                product_id = item['product_id']  # Capture for closure
                user_id = st.session_state.user['uid']  # Capture for closure
                
                def update_quantity(new_quantity: int):
                    """Callback to update cart item quantity."""
                    from services.firebase_service import FirebaseService
                    firebase = FirebaseService()
                    firebase.update_cart_item(user_id, product_id, int(new_quantity))
                    st.rerun()
                
                quantity = st.number_input(
                    "Qty",
                    min_value=1,
                    max_value=99,
                    value=item.get('quantity', 1),
                    key=f"cart_qty_{i}",
                    on_change=update_quantity
                )
            
            with col4:
                item_total = item.get('price', 0) * item.get('quantity', 1)
                st.write(f"**{format_currency(item_total)}**")
                
                if st.button("Remove", key=f"cart_remove_{i}"):
                    from services.firebase_service import FirebaseService
                    firebase = FirebaseService()
                    firebase.update_cart_item(
                        st.session_state.user['uid'],
                        item['product_id'],
                        0
                    )
                    st.rerun()
            
            st.divider()
    
    totals = calculate_total(cart_items, tax_rate=0.08, shipping=5.99)
    
    st.subheader("Order Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Subtotal:")
        st.write("Tax (8%):")
        st.write("Shipping:")
        st.write("**Total:**")
    
    with col2:
        st.write(format_currency(totals['subtotal']))
        st.write(format_currency(totals['tax']))
        st.write(format_currency(totals['shipping']))
        st.write(f"**{format_currency(totals['total'])}**")
    
    if st.button("Proceed to Checkout", type="primary", use_container_width=True):
        st.session_state.checkout_step = 'shipping'
        st.rerun()

