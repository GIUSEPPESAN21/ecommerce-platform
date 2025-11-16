"""
Firebase service for authentication, Firestore, and Storage.
Handles all Firebase operations for the e-commerce platform.
"""
import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, firestore, auth, storage
import json


class FirebaseService:
    """Service class for Firebase operations."""
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Singleton pattern to ensure Firebase is initialized only once."""
        if cls._instance is None:
            cls._instance = super(FirebaseService, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize Firebase Admin SDK if not already initialized."""
        if not FirebaseService._initialized:
            self._initialize_firebase()
            FirebaseService._initialized = True
    
    def _initialize_firebase(self):
        """Initialize Firebase Admin SDK with credentials from Streamlit secrets."""
        try:
            from config.settings import get_firebase_credentials
            
            # Check if Firebase is already initialized
            try:
                firebase_admin.get_app()
                if 'firebase_initialized' not in st.session_state:
                    st.session_state.firebase_initialized = True
                return
            except ValueError:
                pass  # Firebase not initialized yet, continue
            
            # Get credentials
            cred_dict = get_firebase_credentials()
            
            if not cred_dict:
                error_msg = "Firebase credentials not found in Streamlit secrets. Please configure them in Streamlit Cloud settings."
                if 'firebase_error_shown' not in st.session_state:
                    st.error(error_msg)
                    st.session_state.firebase_error_shown = True
                raise ValueError(error_msg)
            
            # Validate that credentials have required fields
            required_fields = ['type', 'project_id', 'private_key', 'client_email']
            missing_fields = [field for field in required_fields if field not in cred_dict]
            
            if missing_fields:
                error_msg = f"Firebase credentials missing required fields: {', '.join(missing_fields)}"
                if 'firebase_error_shown' not in st.session_state:
                    st.error(error_msg)
                    st.session_state.firebase_error_shown = True
                raise ValueError(error_msg)
            
            # Ensure type field is set correctly
            if cred_dict.get('type') != 'service_account':
                cred_dict['type'] = 'service_account'
            
            # Initialize Firebase
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            
            st.session_state.firebase_initialized = True
            if 'firebase_error_shown' in st.session_state:
                del st.session_state.firebase_error_shown
            
        except ValueError as e:
            # Don't show error multiple times
            if 'firebase_error_shown' not in st.session_state:
                st.error(f"Error initializing Firebase: {str(e)}")
                st.session_state.firebase_error_shown = True
            # Don't raise, allow app to continue (but Firebase features won't work)
            return
        except Exception as e:
            error_msg = f"Error initializing Firebase: {str(e)}"
            if 'firebase_error_shown' not in st.session_state:
                st.error(error_msg)
                st.session_state.firebase_error_shown = True
            # Don't raise, allow app to continue
            return
    
    def create_user(self, email: str, password: str, display_name: str = None) -> Optional[Dict[str, Any]]:
        """Create a new user account."""
        try:
            user = auth.create_user(
                email=email,
                password=password,
                display_name=display_name
            )
            
            user_data = {
                'uid': user.uid,
                'email': email,
                'display_name': display_name or email.split('@')[0],
                'created_at': datetime.now(),
                'cart': [],
                'orders': [],
                'addresses': []
            }
            
            db = firestore.client()
            db.collection('users').document(user.uid).set(user_data)
            
            return {
                'uid': user.uid,
                'email': user.email,
                'display_name': user.display_name
            }
        except Exception as e:
            st.error(f"Error creating user: {str(e)}")
            return None
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify Firebase ID token."""
        try:
            decoded_token = auth.verify_id_token(token)
            return decoded_token
        except Exception as e:
            return None
    
    def get_db(self):
        """Get Firestore database client."""
        try:
            # Verify Firebase is initialized
            firebase_admin.get_app()
            return firestore.client()
        except ValueError:
            st.error("Firebase is not initialized. Please check your credentials.")
            return None
    
    def create_product(self, product_data: Dict[str, Any]) -> Optional[str]:
        """Create a new product in Firestore."""
        try:
            db = self.get_db()
            if db is None:
                return None
            
            product_data['created_at'] = datetime.now()
            product_data['updated_at'] = datetime.now()
            doc_ref = db.collection('products').add(product_data)
            return doc_ref[1].id
        except Exception as e:
            st.error(f"Error creating product: {str(e)}")
            return None
    
    def _fetch_products_from_db(self, category: Optional[str] = None, max_fetch: int = 100) -> List[Dict[str, Any]]:
        """
        Internal method to fetch products from Firestore.
        This is the actual database query that gets cached.
        """
        try:
            db = self.get_db()
            if db is None:
                return []
            
            # Build base query
            query = db.collection('products').where('active', '==', True)
            
            # Apply category filter if provided
            if category:
                query = query.where('category', '==', category)
            
            docs = query.limit(max_fetch).stream()
            
            products = []
            for doc in docs:
                product = doc.to_dict()
                product['id'] = doc.id
                products.append(product)
            
            return products
        except Exception as e:
            st.error(f"Error fetching products: {str(e)}")
            return []
    
    def get_products(self, limit: int = 12, category: Optional[str] = None, 
                     search_query: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get products from Firestore with optional filtering.
        Results are cached for 10 minutes to reduce Firebase costs.
        
        Args:
            limit: Maximum number of products to return (applied AFTER search filter)
            category: Optional category filter
            search_query: Optional search query for product name/description
            
        Returns:
            List of product dictionaries
        """
        try:
            # IMPORTANT: Get more products than limit to allow for search filtering
            # We'll fetch up to 100 products, filter by search, then apply limit
            max_fetch = 100 if search_query else limit
            
            # Use cached function to fetch products
            products = _get_cached_products(category, max_fetch)
            
            # Apply search filter BEFORE limiting results
            # This fixes the bug where search wouldn't work if first N products didn't match
            if search_query:
                search_lower = search_query.lower()
                products = [
                    p for p in products
                    if search_lower in p.get('name', '').lower() or
                       search_lower in p.get('description', '').lower()
                ]
            
            # Apply limit AFTER search filtering
            return products[:limit]
            
        except Exception as e:
            st.error(f"Error fetching products: {str(e)}")
            return []
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get a single product by ID."""
        try:
            db = self.get_db()
            if db is None:
                return None
            
            doc = db.collection('products').document(product_id).get()
            
            if doc.exists:
                product = doc.to_dict()
                product['id'] = doc.id
                return product
            return None
        except Exception as e:
            st.error(f"Error fetching product: {str(e)}")
            return None
    
    def _fetch_categories_from_db(self) -> List[str]:
        """
        Internal method to fetch categories from Firestore.
        This is the actual database query that gets cached.
        """
        try:
            db = self.get_db()
            if db is None:
                return []
            
            # Only fetch active products to reduce reads
            docs = db.collection('products').where('active', '==', True).stream()
            
            categories = set()
            for doc in docs:
                product = doc.to_dict()
                if product.get('category'):
                    categories.add(product['category'])
            
            return sorted(list(categories))
        except Exception as e:
            st.error(f"Error fetching categories: {str(e)}")
            return []
    
    
    def get_categories(self) -> List[str]:
        """
        Get all available product categories.
        Results are cached for 1 hour to dramatically reduce Firebase read costs.
        Categories are cached longer than products since they change less frequently.
        
        Returns:
            Sorted list of category names
        """
        return _get_cached_categories()
    
    def get_user_cart(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's shopping cart."""
        try:
            db = self.get_db()
            if db is None:
                return []
            
            user_doc = db.collection('users').document(user_id).get()
            
            if user_doc.exists:
                user_data = user_doc.to_dict()
                return user_data.get('cart', [])
            return []
        except Exception as e:
            st.error(f"Error fetching cart: {str(e)}")
            return []
    
    def add_to_cart(self, user_id: str, product_id: str, quantity: int = 1) -> bool:
        """Add item to user's cart."""
        try:
            db = self.get_db()
            if db is None:
                return False
            
            user_ref = db.collection('users').document(user_id)
            
            user_doc = user_ref.get()
            cart = user_doc.to_dict().get('cart', []) if user_doc.exists else []
            
            product_in_cart = False
            for item in cart:
                if item['product_id'] == product_id:
                    item['quantity'] += quantity
                    product_in_cart = True
                    break
            
            if not product_in_cart:
                product = self.get_product_by_id(product_id)
                if product:
                    cart.append({
                        'product_id': product_id,
                        'name': product.get('name', ''),
                        'price': product.get('price', 0),
                        'image': product.get('images', [{}])[0].get('url', '') if product.get('images') else '',
                        'quantity': quantity
                    })
            
            user_ref.update({
                'cart': cart,
                'updated_at': datetime.now()
            })
            
            return True
        except Exception as e:
            st.error(f"Error adding to cart: {str(e)}")
            return False
    
    def update_cart_item(self, user_id: str, product_id: str, quantity: int) -> bool:
        """Update cart item quantity."""
        try:
            db = self.get_db()
            if db is None:
                return False
            
            user_ref = db.collection('users').document(user_id)
            
            user_doc = user_ref.get()
            if not user_doc.exists:
                return False
            
            cart = user_doc.to_dict().get('cart', [])
            
            if quantity <= 0:
                cart = [item for item in cart if item['product_id'] != product_id]
            else:
                for item in cart:
                    if item['product_id'] == product_id:
                        item['quantity'] = quantity
                        break
            
            user_ref.update({
                'cart': cart,
                'updated_at': datetime.now()
            })
            
            return True
        except Exception as e:
            st.error(f"Error updating cart: {str(e)}")
            return False
    
    def clear_cart(self, user_id: str) -> bool:
        """Clear user's cart."""
        try:
            db = self.get_db()
            if db is None:
                return False
            
            db.collection('users').document(user_id).update({
                'cart': [],
                'updated_at': datetime.now()
            })
            return True
        except Exception as e:
            st.error(f"Error clearing cart: {str(e)}")
            return False
    
    def create_order(self, user_id: str, order_data: Dict[str, Any]) -> Optional[str]:
        """Create a new order."""
        try:
            db = self.get_db()
            if db is None:
                return None
            
            order_data['user_id'] = user_id
            order_data['status'] = 'pending'
            order_data['created_at'] = datetime.now()
            order_data['updated_at'] = datetime.now()
            
            doc_ref = db.collection('orders').add(order_data)
            order_id = doc_ref[1].id
            
            user_ref = db.collection('users').document(user_id)
            user_doc = user_ref.get()
            orders = user_doc.to_dict().get('orders', []) if user_doc.exists else []
            orders.append(order_id)
            
            user_ref.update({
                'orders': orders,
                'updated_at': datetime.now()
            })
            
            return order_id
        except Exception as e:
            st.error(f"Error creating order: {str(e)}")
            return None
    
    def get_user_orders(self, user_id: str) -> List[Dict[str, Any]]:
        """Get user's orders."""
        try:
            db = self.get_db()
            if db is None:
                return []
            
            user_doc = db.collection('users').document(user_id).get()
            
            if not user_doc.exists:
                return []
            
            orders = user_doc.to_dict().get('orders', [])
            order_details = []
            
            for order_id in orders:
                order_doc = db.collection('orders').document(order_id).get()
                if order_doc.exists:
                    order = order_doc.to_dict()
                    order['id'] = order_id
                    order_details.append(order)
            
            order_details.sort(key=lambda x: x.get('created_at', datetime.min), reverse=True)
            
            return order_details
        except Exception as e:
            st.error(f"Error fetching orders: {str(e)}")
            return []
    
    def upload_image(self, file_bytes: bytes, file_name: str, folder: str = 'products') -> Optional[str]:
        """Upload image to Firebase Storage."""
        try:
            bucket = storage.bucket()
            blob = bucket.blob(f"{folder}/{file_name}")
            blob.upload_from_string(file_bytes, content_type='image/jpeg')
            blob.make_public()
            return blob.public_url
        except Exception as e:
            st.error(f"Error uploading image: {str(e)}")
            return None


# ==================== Cached Helper Functions ====================
# These functions are at module level to enable proper caching with @st.cache_data

@st.cache_data(ttl=600)  # Cache for 10 minutes
def _get_cached_products(category: Optional[str] = None, max_fetch: int = 100) -> List[Dict[str, Any]]:
    """
    Cached helper function to fetch products from Firestore.
    This function is cached to dramatically reduce Firebase read costs.
    
    Args:
        category: Optional category filter
        max_fetch: Maximum number of products to fetch from database
        
    Returns:
        List of product dictionaries
    """
    try:
        firebase = FirebaseService()
        return firebase._fetch_products_from_db(category, max_fetch)
    except Exception as e:
        st.error(f"Error in cached products fetch: {str(e)}")
        return []


@st.cache_data(ttl=3600)  # Cache for 1 hour (categories change infrequently)
def _get_cached_categories() -> List[str]:
    """
    Cached helper function to fetch categories from Firestore.
    This function is cached for 1 hour to dramatically reduce Firebase read costs.
    Categories are cached longer than products since they change less frequently.
    
    Returns:
        Sorted list of category names
    """
    try:
        firebase = FirebaseService()
        return firebase._fetch_categories_from_db()
    except Exception as e:
        st.error(f"Error in cached categories fetch: {str(e)}")
        return []

