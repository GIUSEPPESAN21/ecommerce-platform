"""
E-Commerce Platform - Main Application
A professional e-commerce platform built with Streamlit, Firebase, and Python.
Inspired by MercadoLibre, Amazon, and Temu.

MEJORA DE UI (v2):
- Refinamientos en CSS para el header.
- Estilo mejorado para el selector de idioma.
- Animación de entrada suave para el contenido.
- Ajuste en el botón/logo de SAVA para mejor alineación.
"""
import streamlit as st
import sys
from typing import Optional, Dict, Any

# --- Configuración de Página ---
st.set_page_config(
    page_title="SAVA E-Commerce",
    page_icon="https" + "://github.com/GIUSEPPESAN21/LOGO-SAVA/blob/main/LOGO.jpg?raw=true", # Icono de SAVA
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- INYECCIÓN DE CSS MEJORADO ---
# Basado en la Propuesta de Interfaz y refinamientos UX/UI
st.markdown("""
    <style>
        /* --- 1. Globales y Tipografía (Inter) --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
        
        html, body, [class*="st-"], .main {
            font-family: 'Inter', sans-serif;
            background-color: #F5F5F5; /* Fondo gris claro */
        }
        
        /* Ocultar elementos por defecto de Streamlit */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* --- 2. Header Personalizado --- */
        .app-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999;
            background: #FFFFFF; /* HEADER BLANCO LIMPIO */
            padding: 0.75rem 2rem; /* Un poco más delgado */
            box-shadow: 0 2px 4px rgba(0,0,0,0.05); /* Sombra sutil */
            border-bottom: 1px solid #E0E0E0;
        }
        
        .header-main-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        /* MEJORA: Wrapper para el logo y botón de home */
        .header-logo-container {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        /* MEJORA: Estilo para el botón de texto "SAVA E-Commerce" */
        .header-logo-container .stButton>button {
            background: none;
            border: none;
            padding: 0;
            color: #222222; /* Texto oscuro */
            font-size: 1.1rem; /* Ajustado */
            font-weight: 700;
            transition: color 0.2s;
        }
        .header-logo-container .stButton>button:hover {
            color: #0D9488; /* Acento SAVA (Teal) */
            transform: none;
            box-shadow: none;
        }

        .header-search {
            flex-grow: 1;
            margin: 0 2rem;
        }
        
        .header-search .stTextInput input {
            border-radius: 25px;
            border: 1px solid #E0E0E0;
            padding-left: 1.5rem;
            background-color: white;
            transition: all 0.2s ease;
        }
        .header-search .stTextInput input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
        }
        
        .header-nav-links {
            display: flex;
            gap: 0.5rem; /* Espaciado consistente */
            align-items: center;
        }
        
        .header-nav-links .stButton>button {
            background: none;
            border: none;
            color: #333333; /* Texto oscuro */
            font-weight: 400;
            padding: 0.5rem 0.75rem;
            transition: all 0.2s;
            border-radius: 6px;
            width: auto !important; /* !! ARREGLO CLAVE: TAMAÑO DE BOTÓN CONSISTENTE */
        }
        
        .header-nav-links .stButton>button:hover {
            color: #0D9488; /* Acento SAVA (Teal) */
            background-color: rgba(13, 148, 136, 0.05); /* Fondo hover muy sutil */
            transform: none; /* Sin animación de levantamiento en header */
            box-shadow: none;
        }

        /* MEJORA: Estilo para el SelectBox de Idioma */
        .header-nav-links .stSelectbox {
            width: 75px; /* Ancho fijo */
        }
        .header-nav-links .stSelectbox div[data-baseweb="select"] {
            background-color: transparent;
            border: 1px solid #AAAAAA; /* Borde oscuro */
            border-radius: 6px;
            font-size: 0.9rem;
            font-weight: 600;
            color: #333333; /* Texto oscuro */
        }
        .header-nav-links .stSelectbox div[data-baseweb="select"] > div {
            padding: 2px 6px; /* Más pequeño */
        }
        /* MEJORA: Color del icono del selectbox */
        .header-nav-links .stSelectbox svg {
            fill: #333333;
        }
        
        /* MEJORA: Arreglo para Popover y Carrito para que tengan tamaño automático */
        div[data-testid="stPopover"] > button,
        .cart-button-wrapper .stButton>button {
            width: auto !important;
            padding: 0.5rem 0.75rem;
            background: none;
            border: none;
            color: #333333;
            font-weight: 400;
            transition: all 0.2s;
            border-radius: 6px;
        }
        div[data-testid="stPopover"] > button:hover,
        .cart-button-wrapper .stButton>button:hover {
            color: #0D9488;
            background-color: rgba(13, 148, 136, 0.05);
        }

        .cart-button-wrapper {
            position: relative;
        }
        
        .cart-badge {
            position: absolute;
            top: -5px;
            right: -10px;
            background: #ff4444;
            color: white;
            border-radius: 50%;
            width: 20px;
            height: 20px;
            font-size: 0.75rem;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Contenedor principal con padding y animación */
        .main .block-container {
            padding-top: 100px; /* Ajustar según altura del header */
            /* MEJORA: Animación de entrada suave */
            animation: fadeIn 0.5s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* --- 3. Tarjeta de Producto (Product Card) --- */
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"] {
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 1rem;
            background: white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            transition: box-shadow 0.3s ease, transform 0.3s ease;
            height: 100%; /* MEJORA: Asegurar altura consistente */
        }
        
        div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] > div[data-testid="stContainer"]:hover {
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            transform: translateY(-2px);
        }
        
        /* --- 4. Botones --- */
        .stButton>button {
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.3s ease;
            border: none;
            width: 100%;
        }
        
        /* Botón Primario (Comprar, Checkout) */
        .stButton>button[kind="primary"] {
            background-color: #0D9488; /* Acento SAVA (Teal) */
            color: white;
        }
        .stButton>button[kind="primary"]:hover {
            background-color: #0F766E; /* Teal más oscuro */
            transform: translateY(-2px); /* Animación de botón */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Animación de botón */
        }
        
        /* Botón Secundario (Ver Detalles) */
        .stButton>button[kind="secondary"] {
            background-color: #E0E0E0;
            color: #333333;
        }
        .stButton>button[kind="secondary"]:hover {
            background-color: #d5d5d5;
            transform: translateY(-2px); /* Animación de botón */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Animación de botón */
        }
        
        /* --- 5. Footer --- */
        .app-footer {
            background: #FFFFFF; /* Footer blanco */
            color: #333333; /* Texto oscuro */
            padding: 3rem 2rem;
            margin-top: 4rem;
            border-radius: 15px 15px 0 0;
            border-top: 1px solid #E0E0E0;
        }
        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        .footer-col h4 {
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: #0D9488; /* Acento SAVA (Teal) */
        }
        .footer-col ul {
            list-style: none;
            padding: 0;
        }
        .footer-col li {
            margin-bottom: 0.75rem;
        }
        .footer-col a, .footer-col span {
            color: #555555; /* Texto de enlace más oscuro */
            text-decoration: none;
            transition: color 0.2s;
        }
        .footer-col a:hover {
            color: #0D9488; /* Acento SAVA (Teal) */
            text-decoration: underline;
        }
        .footer-copyright {
            text-align: center;
            margin-top: 2rem;
            padding-top: 2rem;
            border-top: 1px solid #555555;
            font-size: 0.9rem;
            color: #AAAAAA;
        }

    </style>
""", unsafe_allow_html=True)


# --- TEXTOS BILINGÜES (ES/EN) ---
# Se centraliza el texto para facilitar la traducción
TEXTS = {
    'ES': {
        'search_placeholder': "Buscar productos, marcas y más...",
        'nav_categories': "🗂️ Categorías",
        'nav_deals': "🔥 Ofertas", # Se mantiene en dicc, pero no se usa en header
        'nav_history': "📜 Historial", # Se mantiene en dicc, pero no se usa en header
        'nav_sell': "💰 Vender", # Se mantiene en dicc, pero no se usa en header
        'user_welcome': "Bienvenido",
        'user_account': "👤 Mi Cuenta",
        'user_orders': "📦 Mis Compras",
        'user_logout': "🚪 Cerrar Sesión",
        'nav_signin': "Ingresa",
        'nav_signup': "Crea tu cuenta",
        'nav_cart': "🛒 Carrito",
        'page_home_title': "Bienvenido a SAVA E-Commerce",
        'page_home_subtitle': "Descubre productos increíbles a precios imbatibles.",
        'page_featured_products': "Productos Destacados",
        'page_products': "Productos",
        'page_cart': "Carrito de Compras",
        'page_checkout': "Finalizar Compra",
        'page_account': "Mi Cuenta",
        'page_orders': "Mis Pedidos",
        'page_about': "ℹ️ Acerca de Nosotros",
        'filter_title': "Filtrar por",
        'filter_categories': "Categorías",
        'filter_all_categories': "Todas las Categorías",
        'filter_selected': "Seleccionado",
        'cart_empty': "Tu carrito está vacío.",
        'cart_browse': "Descubrir productos",
        'cart_summary': "Resumen de compra",
        'cart_subtotal': "Subtotal",
        'cart_shipping': "Envío",
        'cart_tax': "Impuestos",
        'cart_total': "Total",
        'cart_checkout_button': "Continuar Compra",
        'cart_item_list': "Lista de Productos",
        'back_to_products': "← Volver a Productos",
        'add_to_cart': "Agregar al Carrito",
        'in_stock': "En Stock",
        'out_of_stock': "Agotado",
        'footer_col1_title': "Atención al Cliente",
        'footer_col1_l1': "Ayuda y Soporte",
        'footer_col1_l2': "Garantía",
        'footer_col1_l3': "Devoluciones",
        'footer_col2_title': "Acerca de SAVA",
        'footer_col2_l1': "Quiénes somos",
        'footer_col2_l2': "Trabaja con nosotros",
        'footer_col3_title': "Métodos de Pago",
        'footer_col3_l1': "Tarjetas de Crédito",
        'footer_col3_l2': "PayPal",
        'footer_col4_title': "Síguenos",
        'footer_col4_l1': "GitHub",
        'footer_col4_l2': "LinkedIn",
        'footer_copyright': "© 2025 SAVA Software for Engineering. Todos los derechos reservados."
    },
    'EN': {
        'search_placeholder': "Search products, brands, and more...",
        'nav_categories': "🗂️ Categories",
        'nav_deals': "🔥 Deals", # Kept in dict, but not used in header
        'nav_history': "📜 History", # Kept in dict, but not used in header
        'nav_sell': "💰 Sell", # Kept in dict, but not used in header
        'user_welcome': "Welcome",
        'user_account': "👤 My Account",
        'user_orders': "📦 My Purchases",
        'user_logout': "🚪 Sign Out",
        'nav_signin': "Sign In",
        'nav_signup': "Create your account",
        'nav_cart': "🛒 Cart",
        'page_home_title': "Welcome to SAVA E-Commerce",
        'page_home_subtitle': "Discover amazing products at unbeatable prices.",
        'page_featured_products': "Featured Products",
        'page_products': "Products",
        'page_cart': "Shopping Cart",
        'page_checkout': "Checkout",
        'page_account': "My Account",
        'page_orders': "My Orders",
        'page_about': "ℹ️ About Us",
        'filter_title': "Filter by",
        'filter_categories': "Categories",
        'filter_all_categories': "All Categories",
        'filter_selected': "Selected",
        'cart_empty': "Your cart is empty.",
        'cart_browse': "Browse Products",
        'cart_summary': "Order Summary",
        'cart_subtotal': "Subtotal",
        'cart_shipping': "Shipping",
        'cart_tax': "Taxes",
        'cart_total': "Total",
        'cart_checkout_button': "Proceed to Checkout",
        'cart_item_list': "Product List",
        'back_to_products': "← Back to Products",
        'add_to_cart': "Add to Cart",
        'in_stock': "In Stock",
        'out_of_stock': "Out of Stock",
        'footer_col1_title': "Customer Service",
        'footer_col1_l1': "Help & Support",
        'footer_col1_l2': "Warranty",
        'footer_col1_l3': "Returns",
        'footer_col2_title': "About SAVA",
        'footer_col2_l1': "About Us",
        'footer_col2_l2': "Work with us",
        'footer_col3_title': "Payment Methods",
        'footer_col3_l1': "Credit Cards",
        'footer_col3_l2': "PayPal",
        'footer_col4_title': "Follow Us",
        'footer_col4_l1': "GitHub",
        'footer_col4_l2': "LinkedIn",
        'footer_copyright': "© 2025 SAVA Software for Engineering. All rights reserved."
    }
}

# --- Inicialización de Session State ---
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
    if 'lang' not in st.session_state:
        st.session_state.lang = 'ES'

init_session_state()
T = TEXTS[st.session_state.lang] # Objeto de texto global

# ==================== Helper Functions ====================

def update_cart_count():
    """Update cart count in session state."""
    try:
        from services.firebase_service import FirebaseService
        firebase = FirebaseService()
        
        if st.session_state.user:
            cart = firebase.get_user_cart(st.session_state.user['uid'])
            st.session_state.cart_count = sum(item.get('quantity', 0) for item in cart)
        else:
            st.session_state.cart_count = 0
    except Exception as e:
        st.session_state.cart_count = 0

def navigate_to(page: str):
    """Helper function to navigate pages."""
    st.session_state.page = page
    st.rerun()

# --- MEJORA: Header completamente refactorizado ---
def render_header():
    """Render application header with navigation."""
    
    st.markdown('<div class="app-header">', unsafe_allow_html=True)
    
    with st.container():
        # --- 1. Barra Principal (UNA SOLA FILA) ---
        cols = st.columns([2, 3, 4]) # Logo, Búsqueda, Acciones
        
        with cols[0]:
            # MEJORA: Wrapper para alinear logo y texto/botón
            st.markdown('<div class="header-logo-container">', unsafe_allow_html=True)
            st.image(
                "https://github.com/GIUSEPPESAN21/LOGO-SAVA/blob/main/LOGO.jpg?raw=true", 
                width=100, # Logo un poco más pequeño
            )
            if st.session_state.page != 'home':
                # El CSS se aplicará a este botón
                if st.button("SAVA E-Commerce", use_container_width=False):
                     navigate_to('home')
            st.markdown('</div>', unsafe_allow_html=True)
        
        with cols[1]:
            # Barra de búsqueda central
            search_query = st.text_input(
                label="Search",
                placeholder=T['search_placeholder'],
                value=st.session_state.search_query,
                key="header_search",
                label_visibility="collapsed"
            )
            if search_query != st.session_state.search_query:
                st.session_state.search_query = search_query
                st.session_state.page = 'products' # Forzar a página de productos al buscar
                st.rerun()
        
        with cols[2]:
            # Acciones de usuario y carrito
            # !! ARREGLO CLAVE: No usar st.columns aquí
            st.markdown('<div class="header-nav-links">', unsafe_allow_html=True)
            
            # Selector de Idioma
            def on_lang_change():
                st.session_state.lang = st.session_state.lang_selector
            
            st.selectbox(
                label="Language",
                options=['ES', 'EN'],
                index=0 if st.session_state.lang == 'ES' else 1,
                key='lang_selector',
                on_change=on_lang_change,
                label_visibility="collapsed"
            )

            # Botones funcionales
            if st.button(T['nav_categories'], use_container_width=True):
                st.session_state.selected_category = None # Reset
                navigate_to('products')
            
            if st.button(T['page_about'], use_container_width=True):
                navigate_to('about')

            # Usuario (Login o Popover de Cuenta)
            if st.session_state.user:
                with st.popover(f"👤 {T['user_welcome']}, {st.session_state.user.get('display_name', 'User')}"):
                    st.markdown(f"**{st.session_state.user.get('display_name', 'User')}**")
                    st.markdown(f"<small>{st.session_state.user.get('email')}</small>", unsafe_allow_html=True)
                    st.divider()
                    if st.button(T['user_account'], use_container_width=True):
                        navigate_to('account')
                    if st.button(T['user_orders'], use_container_width=True):
                        navigate_to('orders')
                    if st.button(T['user_logout'], use_container_width=True):
                        st.session_state.user = None
                        st.session_state.cart_count = 0
                        if 'id_token' in st.session_state: del st.session_state.id_token
                        if 'refresh_token' in st.session_state: del st.session_state.refresh_token
                        navigate_to('home')
            else:
                if st.button(T['nav_signin'], use_container_width=True):
                    navigate_to('auth')
                if st.button(T['nav_signup'], use_container_width=True):
                    st.session_state.auth_tab = 'register'
                    navigate_to('auth')

            # Carrito
            st.markdown('<div class="cart-button-wrapper">', unsafe_allow_html=True)
            if st.button(f"{T['nav_cart']}", use_container_width=True):
                navigate_to('cart')
            if st.session_state.cart_count > 0:
                st.markdown(f'<div class="cart-badge">{st.session_state.cart_count}</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)
            
        # --- ELIMINADO: Barra de Navegación (Inferior) ---
        # Los botones no funcionales se han quitado para limpiar la UI.

    st.markdown('</div>', unsafe_allow_html=True)


# --- MEJORA: Sidebar refactorizada ---
def render_sidebar():
    """
    Render sidebar with filters.
    MEJORA: Esta función ahora solo debe ser llamada en `products_page`.
    """
    with st.sidebar:
        st.title(T['filter_title'])
        st.divider()
        
        # Categorías
        try:
            from services.firebase_service import FirebaseService
            firebase = FirebaseService()
            categories = firebase.get_categories()
            
            if categories:
                st.subheader(T['filter_categories'])
                
                if st.button(T['filter_all_categories']):
                    st.session_state.selected_category = None
                    st.rerun()
                
                for category in categories:
                    if st.button(category, key=f"cat_{category}"):
                        st.session_state.selected_category = category
                        st.rerun()
                
                if st.session_state.selected_category:
                    st.info(f"{T['filter_selected']}: {st.session_state.selected_category}")
            else:
                if st.session_state.get('firebase_initialized', False):
                    st.info("No categories available yet.")
        except Exception as e:
            if 'firebase_error_shown' not in st.session_state:
                error_msg = str(e)
                if 'service account certificate' not in error_msg.lower():
                    st.warning("Categories temporarily unavailable.")
        
        st.divider()
        # Aquí se pueden añadir más filtros (Precio, Marca, etc.)


# ==================== Page Functions ====================

def render_home_page():
    """Render home page with featured products."""
    st.title(T['page_home_title'])
    st.markdown(T['page_home_subtitle'])
    
    # MEJORA: Añadir banner hero
    st.image(
        "https://placehold.co/1200x300/667eea/FFFFFF?text=ENVÍO+GRATIS+EN+TU+PRIMERA+COMPRA",
        use_container_width=True
    )
    
    try:
        from services.firebase_service import FirebaseService
        from components.product_list import render_product_grid
        
        firebase = FirebaseService()
        products = firebase.get_products(limit=8) # Limitar a 8 para la home
        
        if products:
            st.subheader(T['page_featured_products'])
            render_product_grid(products, columns=4) # 4 columnas
        else:
            if st.session_state.get('firebase_initialized', False):
                st.info("No products available. Check back soon!")
            else:
                st.info("Loading products...")
            
    except Exception as e:
        error_msg = str(e)
        if 'service account certificate' not in error_msg.lower() and 'firebase' not in error_msg.lower():
            if 'products_error_shown' not in st.session_state:
                st.warning("Products temporarily unavailable. Please try again later.")
                st.session_state.products_error_shown = True


def render_products_page():
    """Render products page with search and filters."""
    st.title(T['page_products'])
    
    # MEJORA: La sidebar SÓLO se renderiza aquí
    render_sidebar()
    
    try:
        from services.firebase_service import FirebaseService
        from components.product_list import render_product_grid
        
        firebase = FirebaseService()
        
        products = firebase.get_products(
            limit=24,
            category=st.session_state.selected_category,
            search_query=st.session_state.search_query
        )
        
        filters_active = []
        if st.session_state.search_query:
            filters_active.append(f"Search: {st.session_state.search_query}")
        if st.session_state.selected_category:
            filters_active.append(f"Category: {st.session_state.selected_category}")
        
        if filters_active:
            st.info(" | ".join(filters_active))
        
        if products:
            render_product_grid(products, columns=4)
        else:
            if st.session_state.get('firebase_initialized', False):
                st.info("No products found matching your criteria.")
            else:
                st.info("Loading products...")
            
    except Exception as e:
        error_msg = str(e)
        if 'service account certificate' not in error_msg.lower() and 'firebase' not in error_msg.lower():
            if 'products_error_shown' not in st.session_state:
                st.warning("Products temporarily unavailable. Please try again later.")
                st.session_state.products_error_shown = True


def render_product_detail_page():
    """Render product detail page."""
    product_id = st.session_state.selected_product_id
    
    if not product_id:
        st.warning("No product selected.")
        navigate_to('home')
        return
    
    try:
        from services.firebase_service import FirebaseService
        from utils.formatters import format_currency
        
        firebase = FirebaseService()
        product = firebase.get_product_by_id(product_id)
        
        if not product:
            st.error("Product not found.")
            navigate_to('home')
            return
        
        if st.button(T['back_to_products']):
            st.session_state.selected_product_id = None
            navigate_to('products')
        
        # MEJORA: Layout de 2 columnas con fondo blanco
        with st.container():
            st.markdown('<div style="background: white; padding: 2rem; border-radius: 8px;">', unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            
            with col1:
                images = product.get('images', [])
                if images:
                    st.image(images[0].get('url', ''), use_container_width=True)
                else:
                    st.image("https://placehold.co/500x500/F5F5F5/AAAAAA?text=No+Image", use_container_width=True)
                
                if len(images) > 1:
                    cols_thumb = st.columns(min(len(images) - 1, 4))
                    for i, img in enumerate(images[1:5]):
                        with cols_thumb[i]:
                            st.image(img.get('url', ''), use_container_width=True)
            
            with col2:
                st.title(product.get('name', 'Product'))
                
                rating = product.get('rating', 0)
                reviews_count = product.get('reviews_count', 0)
                if rating > 0:
                    stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
                    st.markdown(f"{stars} ({reviews_count} reviews)")
                
                price = product.get('price', 0)
                st.markdown(f"## {format_currency(price)}")
                
                st.markdown(f"🚚 **{T['cart_shipping']}**: {format_currency(5.99)} - _Llega mañana_")
                
                stock = product.get('stock', 0)
                in_stock = stock > 0
                if in_stock:
                    st.success(f"✅ {T['in_stock']} ({stock} available)")
                else:
                    st.error(f"❌ {T['out_of_stock']}")
                
                if st.session_state.user:
                    if in_stock:
                        col_qty, col_add = st.columns([1, 2])
                        with col_qty:
                            quantity = st.number_input(
                                "Quantity",
                                min_value=1,
                                max_value=min(stock, 99),
                                value=1,
                                key="product_detail_qty",
                                label_visibility="collapsed"
                            )
                        with col_add:
                            if st.button(T['add_to_cart'], type="primary", use_container_width=True):
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
                    st.info(f"🔐 {T['nav_signin']} to add items to your cart")
                
                st.divider()
                description = product.get('description', '')
                if description:
                    st.markdown("### Description")
                    st.write(description)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Error loading product: {str(e)}")


# --- MEJORA: Página de carrito refactorizada (2 columnas) ---
def render_cart_page():
    """Render cart page with 2-column layout."""
    if not st.session_state.user:
        st.warning("Please sign in to view your cart.")
        navigate_to('auth')
        return
    
    st.title(T['page_cart'])
    
    try:
        from services.firebase_service import FirebaseService
        from utils.formatters import format_currency, calculate_total
        
        firebase = FirebaseService()
        cart_items = firebase.get_user_cart(st.session_state.user['uid'])
        update_cart_count()

        if not cart_items:
            st.info(T['cart_empty'])
            if st.button(T['cart_browse']):
                navigate_to('products')
            return

        # Layout de 2 columnas
        col_items, col_summary = st.columns([2, 1])

        with col_items:
            st.subheader(T['cart_item_list'])
            st.markdown('<div style="background: white; padding: 1rem; border-radius: 8px;">', unsafe_allow_html=True)
            
            def handle_quantity_change(user_id: str, product_id: str, new_quantity_key: str):
                new_quantity = st.session_state.get(new_quantity_key)
                if new_quantity is None: return
                firebase.update_cart_item(user_id, product_id, new_quantity)
                st.rerun()

            for item in cart_items:
                with st.container():
                    c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
                    with c1:
                        st.image(item.get('image', 'https://placehold.co/80x80'), width=80)
                    with c2:
                        st.write(f"**{item.get('name', 'Product')}**")
                        st.write(format_currency(item.get('price', 0)))
                    with c3:
                        quantity_key = f"cart_qty_{item['product_id']}"
                        st.number_input(
                            "Qty",
                            min_value=1,
                            max_value=99,
                            value=item.get('quantity', 1),
                            key=quantity_key,
                            on_change=handle_quantity_change,
                            kwargs={
                                'user_id': st.session_state.user['uid'],
                                'product_id': item['product_id'],
                                'new_quantity_key': quantity_key
                            },
                            label_visibility="collapsed"
                        )
                    with c4:
                        if st.button("🗑️", key=f"cart_remove_{item['product_id']}"):
                            firebase.update_cart_item(st.session_state.user['uid'], item['product_id'], 0)
                            st.rerun()
                    st.divider()
            
            st.markdown('</div>', unsafe_allow_html=True)

        with col_summary:
            st.subheader(T['cart_summary'])
            st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #E0E0E0;">', unsafe_allow_html=True)
            
            totals = calculate_total(cart_items, tax_rate=0.08, shipping=5.99)
            
            col_label, col_value = st.columns(2)
            with col_label:
                st.write(f"{T['cart_subtotal']}:")
                st.write(f"{T['cart_tax']} (8%):")
                st.write(f"{T['cart_shipping']}:")
                st.markdown(f"**{T['cart_total']}:**")
            with col_value:
                st.write(format_currency(totals['subtotal']))
                st.write(format_currency(totals['tax']))
                st.write(format_currency(totals['shipping']))
                st.markdown(f"**{format_currency(totals['total'])}**")
            
            st.divider()
            
            if st.button(T['cart_checkout_button'], type="primary", use_container_width=True):
                st.session_state.checkout_step = 'shipping'
                navigate_to('checkout')
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error loading cart: {str(e)}")


def render_checkout_page():
    """Render checkout page."""
    if not st.session_state.user:
        st.warning("Please sign in to checkout.")
        navigate_to('auth')
        return
    
    st.title(T['page_checkout'])
    
    try:
        from services.firebase_service import FirebaseService
        from components.checkout_form import render_checkout_form
        
        firebase = FirebaseService()
        cart_items = firebase.get_user_cart(st.session_state.user['uid'])
        
        if not cart_items:
            st.warning("Your cart is empty. Add items before checkout.")
            navigate_to('cart')
            return
        
        col_form, col_summary = st.columns([1.5, 1])
        
        with col_form:
            st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 8px;">', unsafe_allow_html=True)
            render_checkout_form(cart_items)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_summary:
            st.subheader(T['cart_summary'])
            st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #E0E0E0;">', unsafe_allow_html=True)
            
            from utils.formatters import format_currency, calculate_total
            totals = calculate_total(cart_items, tax_rate=0.08, shipping=5.99)
            
            for item in cart_items:
                st.write(f"• {item.get('name')} x{item.get('quantity')}")
            st.divider()
            
            col_label, col_value = st.columns(2)
            with col_label:
                st.write(f"{T['cart_subtotal']}:")
                st.write(f"{T['cart_tax']}:")
                st.write(f"{T['cart_shipping']}:")
                st.markdown(f"**{T['cart_total']}:**")
            with col_value:
                st.write(format_currency(totals['subtotal']))
                st.write(format_currency(totals['tax']))
                st.write(format_currency(totals['shipping']))
                st.markdown(f"**{format_currency(totals['total'])}**")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
    except Exception as e:
        st.error(f"Error loading checkout: {str(e)}")


def render_auth_page():
    """Render authentication page."""
    st.title(T['page_account'])
    
    from components.auth import render_login_form, render_register_form
    
    tab_titles = [T['nav_signin'], T['nav_signup']]
    
    if st.session_state.auth_tab == 'register':
        default_index = 1
    else:
        default_index = 0

    tab1, tab2 = st.tabs(tab_titles)
    
    with tab1:
        render_login_form()
    
    with tab2:
        render_register_form()


def render_account_page():
    """Render account page."""
    if not st.session_state.user:
        st.warning("Please sign in to view your account.")
        navigate_to('auth')
        return
    
    st.title(T['page_account'])
    
    user = st.session_state.user
    st.write(f"**Name:** {user.get('display_name', 'N/A')}")
    st.write(f"**Email:** {user.get('email', 'N/A')}")
    
    st.divider()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button(T['page_orders'], use_container_width=True):
            navigate_to('orders')
    with col2:
        if st.button(T['page_cart'], use_container_width=True):
            navigate_to('cart')
    with col3:
        if st.button("Edit Profile", use_container_width=True):
            st.info("Profile editing coming soon!")


def render_orders_page():
    """Render orders page."""
    if not st.session_state.user:
        st.warning("Please sign in to view your orders.")
        navigate_to('auth')
        return
    
    st.title(T['page_orders'])
    
    try:
        from services.firebase_service import FirebaseService
        from utils.formatters import format_currency, format_date, format_order_status
        
        firebase = FirebaseService()
        orders = firebase.get_user_orders(st.session_state.user['uid'])
        
        if orders:
            for order in orders:
                with st.container():
                    st.markdown('<div style="background: white; padding: 1.5rem; border-radius: 8px; border: 1px solid #E0E0E0; margin-bottom: 1rem;">', unsafe_allow_html=True)
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
                            st.session_state.page = 'order_detail' # Necesita implementación de esta página
                            st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("You have no orders yet.")
            if st.button(T['cart_browse']):
                navigate_to('products')
    
    except Exception as e:
        st.error(f"Error loading orders: {str(e)}")


def render_about_page():
    """Render about page with company and team information."""
    from components.about import render_about_content
    render_about_content()


# --- MEJORA: Footer completamente refactorizado ---
def render_footer():
    """Render footer with company information and copyright."""
    st.markdown("---")
    
    footer_html = f"""
    <div class="app-footer">
        <div class="footer-grid">
            <div class="footer-col">
                <h4>{T['footer_col1_title']}</h4>
                <ul>
                    <li><a href="#">{T['footer_col1_l1']}</a></li>
                    <li><a href="#">{T['footer_col1_l2']}</a></li>
                    <li><a href="#">{T['footer_col1_l3']}</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>{T['footer_col2_title']}</h4>
                <ul>
                    <li><a href="#">{T['footer_col2_l1']}</a></li>
                    <li><a href="#">{T['footer_col2_l2']}</a></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>{T['footer_col3_title']}</h4>
                <ul>
                    <li><span>{T['footer_col3_l1']}</span></li>
                    <li><span>{T['footer_col3_l2']}</span></li>
                </ul>
            </div>
            <div class="footer-col">
                <h4>{T['footer_col4_title']}</h4>
                <ul>
                    <li><a href="https://github.com/GIUSEPPESAN21" target="_blank">{T['footer_col4_l1']}</a></li>
                    <li><a href="https://www.linkedin.com/in/joseph-javier-sánchez-acuña-150410275" target="_blank">{T['footer_col4_l2']}</a></li>
                </ul>
            </div>
        </div>
        <div class="footer-copyright">
            <p>{T['footer_copyright']}</p>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


# ==================== Main Application ====================

def main():
    """Main application function."""
    
    # Render header (siempre visible)
    render_header()
    
    # Actualizar contador de carrito
    update_cart_count()
    
    # Contenedor principal para el contenido de la página
    with st.container():
        
        # MEJORA: Lógica de layout
        # Solo mostrar sidebar en 'products'
        if st.session_state.page == 'products':
            # render_sidebar() es llamado dentro de render_products_page()
            pass
        
        # Handle product detail page (check if product selected)
        if st.session_state.selected_product_id:
            render_product_detail_page()
        else:
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
            elif page == 'about':
                render_about_page()
            else:
                render_home_page()
    
    # Render footer (siempre visible)
    render_footer()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.exception(e)
