"""
E-Commerce Platform - Main Application
A professional e-commerce platform built with Streamlit, Firebase, and Python.
Inspired by MercadoLibre, Amazon, and Temu.
"""
import streamlit as st
import sys
from typing import Optional, Dict, Any

# Configure page
st.set_page_config(
    page_title="E-Commerce Platform",
    page_icon="ðŸ›’",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for professional look
st.markdown("""
    <style>
        .main {
            padding-top: 2rem;
        }
        .stButton>button {
            width: 100%;
        }
        .product-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 1rem;
            margin: 0.5rem 0;
        }
        .header {
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 1rem;
            border-radius: 10px;
            color: white;
            margin-bottom: 2rem;
        }
        .cart-badge {
            background: #ff4444;
            color: white;
            border-radius: 50%;
            padding: 0.2rem 0.5rem;
            font-size: 0.8rem;
            margin-left: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    """Initialize session state variables."""
    if 'page' not in st.session_state:
        st.session_state.page = 'home'
    
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    if 'cart_count' not in st.session_state:
        st.session_state.cart_count = 0
    
    if 'search_query' not in st.session_state:
        st.session_state.search_query = ''
    
    if 'selected_category' not in st.session_state:
        st.session_state.selected_category = None
    
    if 'selected_product_id' not in st.session_state:
        st.session_state.selected_product_id = None
    
    if 'auth_tab' not in st.session_state:
        st.session_state.auth_tab = 'login'


# Initialize session state
init_session_state()


# ==================== Helper Functions ====================

def update_cart_count():
    """Update cart count in session state."""
    try:
        from services.firebase_service import FirebaseService
        firebase = FirebaseService()
        
        if st.session_state.user:
            cart = firebase.get_user_cart(st.session_state.user['uid'])
            st.session_state.cart_count = len(cart) if cart else 0
        else:
            st.session_state.cart_count = 0
    except Exception as e:
        st.session_state.cart_count = 0


def render_header():
    """Render application header with navigation."""
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
    
    with col1:
        st.markdown("### ðŸ›’ E-Commerce Platform")
    
    with col2:
        if st.button("ðŸ  Home"):
            st.session_state.page = 'home'
            st.rerun()
    
    with col3:
        if st.button("ðŸ“¦ Products"):
            st.session_state.page = 'products'
            st.rerun()
    
    with col4:
        cart_text = f"ðŸ›ï¸ Cart"
        if st.session_state.cart_count > 0:
            cart_text += f" ({st.session_state.cart_count})"
        
        if st.button(cart_text):
            st.session_state.page = 'cart'
            st.rerun()
    
    with col5:
        if st.session_state.user:
            if st.button("ðŸ‘¤ Account"):
                st.session_state.page = 'account'
                st.rerun()
        else:
            if st.button("ðŸ” Sign In"):
                st.session_state.page = 'auth'
                st.rerun()
    
    st.divider()


def render_sidebar():
    """Render sidebar with filters and navigation."""
    with st.sidebar:
        st.title("Filters")
        
        # Search
        search_query = st.text_input(
            "Search products",
            value=st.session_state.search_query,
            placeholder="Enter product name..."
        )
        
        if search_query != st.session_state.search_query:
            st.session_state.search_query = search_query
            st.rerun()
        
        st.divider()
        
        # Categories
        try:
            from services.firebase_service import FirebaseService
            firebase = FirebaseService()
            categories = firebase.get_categories()
            
            if categories:
                st.subheader("Categories")
                
                if st.button("All Categories"):
                    st.session_state.selected_category = None
                    st.rerun()
                
                for category in categories:
                    if st.button(category, key=f"cat_{category}"):
                        st.session_state.selected_category = category
                        st.rerun()
                
                if st.session_state.selected_category:
                    st.info(f"Selected: {st.session_state.selected_category}")
        except Exception as e:
            st.error(f"Error loading categories: {str(e)}")
        
        st.divider()
        
        # User info
        if st.session_state.user:
            st.write(f"**Welcome, {st.session_state.user.get('display_name', 'User')}!**")
            
            if st.button("My Orders"):
                st.session_state.page = 'orders'
                st.rerun()
            
            if st.button("Sign Out"):
                st.session_state.user = None
                st.session_state.cart_count = 0
                st.session_state.page = 'home'
                st.rerun()
        else:
            st.info("Sign in to access your account and cart")


# ==================== Page Functions ====================

def render_home_page():
    """Render home page with featured products."""
    st.title("Welcome to Our E-Commerce Platform")
    st.markdown("Discover amazing products at unbeatable prices!")
    
    try:
        from services.firebase_service import FirebaseService
        from components.product_list import render_product_grid
        
        firebase = FirebaseService()
        
        # Get featured products
        products = firebase.get_products(limit=12)
        
        if products:
            st.subheader("Featured Products")
            render_product_grid(products, columns=4)
        else:
            st.info("No products available. Check back soon!")
            
    except Exception as e:
        st.error(f"Error loading products: {str(e)}")


def render_products_page():
    """Render products page with search and filters."""
    st.title("Products")
    
    try:
        from services.firebase_service import FirebaseService
        from components.product_list import render_product_grid
        
        firebase = FirebaseService()
        
        # Get products with filters
        products = firebase.get_products(
            limit=24,
            category=st.session_state.selected_category,
            search_query=st.session_state.search_query
        )
        
        # Display filters active
        filters_active = []
        if st.session_state.search_query:
            filters_active.append(f"Search: {st.session_state.search_query}")
        if st.session_state.selected_category:
            filters_active.append(f"Category: {st.session_state.selected_category}")
        
        if filters_active:
            st.info(" | ".join(filters_active))
        
        # Display products
        if products:
            render_product_grid(products, columns=4)
        else:
            st.info("No products found matching your criteria.")
            
    except Exception as e:
        st.error(f"Error loading products: {str(e)}")


def render_product_detail_page():
    """Render product detail page."""
    product_id = st.session_state.selected_product_id
    
    if not product_id:
        st.warning("No product selected.")
        st.session_state.page = 'home'
        st.rerun()
        return
    
    try:
        from services.firebase_service import FirebaseService
        from utils.formatters import format_currency
        
        firebase = FirebaseService()
        product = firebase.get_product_by_id(product_id)
        
        if not product:
            st.error("Product not found.")
            st.session_state.page = 'home'
            st.rerun()
            return
        
        # Back button
        if st.button("â† Back to Products"):
            st.session_state.selected_product_id = None
            st.session_state.page = 'products'
            st.rerun()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            images = product.get('images', [])
            if images:
                main_image = images[0].get('url', '')
                st.image(main_image, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/500x500?text=No+Image", use_container_width=True)
            
            # Additional images
            if len(images) > 1:
                cols = st.columns(min(len(images) - 1, 4))
                for i, img in enumerate(images[1:5]):
                    with cols[i]:
                        st.image(img.get('url', ''), use_container_width=True)
        
        with col2:
            st.title(product.get('name', 'Product'))
            
            # Price
            price = product.get('price', 0)
            st.markdown(f"## {format_currency(price)}")
            
            # Rating
            rating = product.get('rating', 0)
            reviews_count = product.get('reviews_count', 0)
            if rating > 0:
                stars = "â­" * int(rating) + "â˜†" * (5 - int(rating))
                st.markdown(f"{stars} ({reviews_count} reviews)")
            
            # Stock
            stock = product.get('stock', 0)
            in_stock = stock > 0
            if in_stock:
                st.success(f"âœ“ In Stock ({stock} available)")
            else:
                st.error("âœ— Out of Stock")
            
            # Description
            description = product.get('description', '')
            if description:
                st.markdown("### Description")
                st.write(description)
            
            # Add to cart (if logged in)
            if st.session_state.user:
                if in_stock:
                    col_qty, col_add = st.columns([1, 2])
                    
                    with col_qty:
                        quantity = st.number_input(
                            "Quantity",
                            min_value=1,
                            max_value=min(stock, 99),
                            value=1,
                            key="product_detail_qty"
                        )
                    
                    with col_add:
                        if st.button("Add to Cart", type="primary", use_container_width=True):
                            success = firebase.add_to_cart(
                                st.session_state.user['uid'],
                                product_id,
                                quantity
                            )
                            
                            if success:
                                st.success("Added to cart!")
                                update_cart_count()
                                st.rerun()
                            else:
                                st.error("Failed to add to cart")
                else:
                    st.warning("This product is currently out of stock.")
            else:
                st.info("ðŸ” Sign in to add items to your cart")
        
        # Additional details
        st.divider()
        st.subheader("Product Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if product.get('category'):
                st.write(f"**Category:** {product.get('category')}")
            if product.get('brand'):
                st.write(f"**Brand:** {product.get('brand')}")
            if product.get('sku'):
                st.write(f"**SKU:** {product.get('sku')}")
        
        with col2:
            if product.get('weight'):
                st.write(f"**Weight:** {product.get('weight')} lbs")
            if product.get('dimensions'):
                st.write(f"**Dimensions:** {product.get('dimensions')}")
        
    except Exception as e:
        st.error(f"Error loading product: {str(e)}")


def render_cart_page():
    """Render cart page."""
    if not st.session_state.user:
        st.warning("Please sign in to view your cart.")
        st.session_state.page = 'auth'
        st.rerun()
        return
    
    st.title("Shopping Cart")
    
    try:
        from services.firebase_service import FirebaseService
        from components.cart_summary import render_cart_summary
        
        firebase = FirebaseService()
        cart_items = firebase.get_user_cart(st.session_state.user['uid'])
        
        update_cart_count()
        
        if cart_items:
            render_cart_summary(cart_items)
        else:
            st.info("Your cart is empty.")
            if st.button("Browse Products"):
                st.session_state.page = 'products'
                st.rerun()
    
    except Exception as e:
        st.error(f"Error loading cart: {str(e)}")


def render_checkout_page():
    """Render checkout page."""
    if not st.session_state.user:
        st.warning("Please sign in to checkout.")
        st.session_state.page = 'auth'
        st.rerun()
        return
    
    st.title("Checkout")
    
    try:
        from services.firebase_service import FirebaseService
        from components.checkout_form import render_checkout_form
        
        firebase = FirebaseService()
        cart_items = firebase.get_user_cart(st.session_state.user['uid'])
        
        if not cart_items:
            st.warning("Your cart is empty. Add items before checkout.")
            st.session_state.page = 'cart'
            st.rerun()
            return
        
        render_checkout_form(cart_items)
    
    except Exception as e:
        st.error(f"Error loading checkout: {str(e)}")


def render_auth_page():
    """Render authentication page."""
    st.title("Account")
    
    from components.auth import render_login_form, render_register_form
    
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])
    
    with tab1:
        render_login_form()
    
    with tab2:
        render_register_form()


def render_account_page():
    """Render account page."""
    if not st.session_state.user:
        st.warning("Please sign in to view your account.")
        st.session_state.page = 'auth'
        st.rerun()
        return
    
    st.title("My Account")
    
    user = st.session_state.user
    st.write(f"**Name:** {user.get('display_name', 'N/A')}")
    st.write(f"**Email:** {user.get('email', 'N/A')}")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("My Orders", use_container_width=True):
            st.session_state.page = 'orders'
            st.rerun()
    
    with col2:
        if st.button("My Cart", use_container_width=True):
            st.session_state.page = 'cart'
            st.rerun()
    
    with col3:
        if st.button("Edit Profile", use_container_width=True):
            st.info("Profile editing coming soon!")


def render_orders_page():
    """Render orders page."""
    if not st.session_state.user:
        st.warning("Please sign in to view your orders.")
        st.session_state.page = 'auth'
        st.rerun()
        return
    
    st.title("My Orders")
    
    try:
        from services.firebase_service import FirebaseService
        from utils.formatters import format_currency, format_date, format_order_status
        
        firebase = FirebaseService()
        orders = firebase.get_user_orders(st.session_state.user['uid'])
        
        if orders:
            for order in orders:
                with st.container():
                    col1, col2, col3 = st.columns([2, 1, 1])
                    
                    with col1:
                        st.write(f"**Order ID:** {order.get('id', 'N/A')}")
                        st.write(f"**Date:** {format_date(order.get('created_at', ''))}")
                        st.write(f"**Status:** {format_order_status(order.get('status', 'pending'))}")
                    
                    with col2:
                        items = order.get('items', [])
                        st.write(f"**Items:** {len(items)}")
                        totals = order.get('totals', {})
                        st.write(f"**Total:** {format_currency(totals.get('total', 0))}")
                    
                    with col3:
                        if st.button("View Details", key=f"order_{order.get('id')}"):
                            st.session_state.selected_order_id = order.get('id')
                            st.session_state.page = 'order_detail'
                            st.rerun()
                    
                    st.divider()
        else:
            st.info("You have no orders yet.")
            if st.button("Start Shopping"):
                st.session_state.page = 'products'
                st.rerun()
    
    except Exception as e:
        st.error(f"Error loading orders: {str(e)}")


# ==================== Main Application ====================

def main():
    """Main application function."""
    # Render header
    render_header()
    
    # Render sidebar
    render_sidebar()
    
    # Update cart count
    update_cart_count()
    
    # Handle product detail page (check if product selected)
    if st.session_state.selected_product_id:
        render_product_detail_page()
        return
    
    # Route to appropriate page
    page = st.session_state.page
    
    if page == 'home':
        render_home_page()
    elif page == 'products':
        render_products_page()
    elif page == 'cart':
        render_cart_page()
    elif page == 'checkout':
        render_checkout_page()
    elif page == 'auth':
        render_auth_page()
    elif page == 'account':
        render_account_page()
    elif page == 'orders':
        render_orders_page()
    else:
        render_home_page()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)