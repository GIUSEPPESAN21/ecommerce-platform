"""
Product card component for displaying products in grid layout.
"""
import streamlit as st
from typing import Dict, Any


def render_product_card(product: Dict[str, Any], key_prefix: str = ""):
    """
    Render a product card component.
    
    Args:
        product: Product dictionary
        key_prefix: Optional prefix for Streamlit keys
    """
    product_id = product.get('id', '')
    name = product.get('name', 'No name')
    price = product.get('price', 0)
    images = product.get('images', [])
    rating = product.get('rating', 0)
    reviews_count = product.get('reviews_count', 0)
    in_stock = product.get('stock', 0) > 0
    
    image_url = images[0].get('url', '') if images else ''
    
    with st.container():
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if image_url:
                st.image(image_url, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300x300?text=No+Image", use_container_width=True)
        
        with col2:
            st.subheader(name)
            
            from utils.formatters import format_currency
            st.markdown(f"### {format_currency(price)}")
            
            if rating > 0:
                stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
                st.markdown(f"{stars} ({reviews_count} reviews)")
            
            if in_stock:
                st.success("✓ In Stock")
            else:
                st.error("✗ Out of Stock")
            
            if st.button("View Details", key=f"{key_prefix}_view_{product_id}"):
                st.session_state.selected_product_id = product_id
                st.rerun()
            
            if st.session_state.get('user'):
                if in_stock:
                    quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        max_value=10,
                        value=1,
                        key=f"{key_prefix}_qty_{product_id}"
                    )
                    if st.button("Add to Cart", key=f"{key_prefix}_add_{product_id}"):
                        from services.firebase_service import FirebaseService
                        firebase = FirebaseService()
                        
                        success = firebase.add_to_cart(
                            st.session_state.user['uid'],
                            product_id,
                            quantity
                        )
                        
                        if success:
                            st.success("Added to cart!")
                            st.rerun()
                        else:
                            st.error("Failed to add to cart")

