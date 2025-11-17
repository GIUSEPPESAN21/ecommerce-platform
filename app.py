"""
E-Commerce Platform - Main Application
SAVA SOFTWARE FOR ENGINEERING

🎨 REDISEÑO UX/UI PROFESIONAL v3.0
- Interfaz moderna bilingüe (ES/EN)
- Sistema de diseño coherente y profesional
- Microinteracciones y feedback visual
- Responsive design optimizado
- Accesibilidad mejorada
"""
import streamlit as st
from typing import Optional, Dict, Any

# --- Configuración de Página ---
st.set_page_config(
    page_title="SAVA E-Commerce",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SISTEMA DE DISEÑO PROFESIONAL ---
st.markdown("""
    <style>
        /* ========================================
           1. SISTEMA DE TIPOGRAFÍA Y COLORES
        ======================================== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        :root {
            /* Colores principales SAVA */
            --sava-primary: #0D9488;
            --sava-primary-dark: #0F766E;
            --sava-primary-light: #14B8A6;
            
            /* Escala de grises */
            --gray-50: #F9FAFB;
            --gray-100: #F3F4F6;
            --gray-200: #E5E7EB;
            --gray-300: #D1D5DB;
            --gray-400: #9CA3AF;
            --gray-500: #6B7280;
            --gray-600: #4B5563;
            --gray-700: #374151;
            --gray-800: #1F2937;
            --gray-900: #111827;
            
            /* Semánticos */
            --success: #10B981;
            --warning: #F59E0B;
            --error: #EF4444;
            --info: #3B82F6;
            
            /* Espaciado (sistema 8px) */
            --space-xs: 0.5rem;
            --space-sm: 0.75rem;
            --space-md: 1rem;
            --space-lg: 1.5rem;
            --space-xl: 2rem;
            --space-2xl: 3rem;
            
            /* Bordes */
            --radius-sm: 6px;
            --radius-md: 8px;
            --radius-lg: 12px;
            --radius-xl: 16px;
            
            /* Sombras */
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }
        
        /* Reset y base */
        html, body, [class*="st-"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--gray-900);
            background-color: var(--gray-50);
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }
        
        /* Ocultar elementos Streamlit */
        #MainMenu, footer, header {visibility: hidden;}
        .stDeployButton {display: none;}
        
        /* ========================================
           2. HEADER PROFESIONAL
        ======================================== */
        .sava-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            background: white;
            border-bottom: 1px solid var(--gray-200);
            transition: box-shadow 0.3s ease;
        }
        
        .sava-header.scrolled {
            box-shadow: var(--shadow-md);
        }
        
        .header-content {
            max-width: 1400px;
            margin: 0 auto;
            padding: var(--space-md) var(--space-xl);
            display: flex;
            align-items: center;
            gap: var(--space-lg);
        }
        
        /* Logo y marca */
        .header-brand {
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            flex-shrink: 0;
        }
        
        .header-brand img {
            width: 48px;
            height: 48px;
            border-radius: var(--radius-md);
        }
        
        .header-brand .brand-name {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--gray-900);
            letter-spacing: -0.02em;
        }
        
        /* Búsqueda */
        .header-search {
            flex: 1;
            max-width: 600px;
        }
        
        .header-search .stTextInput > div > div > input {
            border: 2px solid var(--gray-200);
            border-radius: var(--radius-lg);
            padding: 0.625rem 1rem;
            font-size: 0.9375rem;
            transition: all 0.2s ease;
            background: var(--gray-50);
        }
        
        .header-search .stTextInput > div > div > input:focus {
            border-color: var(--sava-primary);
            background: white;
            box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
        }
        
        /* Navegación */
        .header-nav {
            display: flex;
            align-items: center;
            gap: var(--space-sm);
            flex-shrink: 0;
        }
        
        /* Botones de navegación */
        .header-nav .stButton > button {
            background: transparent;
            border: none;
            color: var(--gray-700);
            font-size: 0.9375rem;
            font-weight: 500;
            padding: 0.5rem 0.875rem;
            border-radius: var(--radius-md);
            transition: all 0.15s ease;
            white-space: nowrap;
        }
        
        .header-nav .stButton > button:hover {
            background: var(--gray-100);
            color: var(--sava-primary);
            transform: translateY(-1px);
        }
        
        /* Selector de idioma mejorado */
        .lang-selector {
            position: relative;
        }
        
        .lang-selector .stSelectbox {
            width: 70px;
        }
        
        .lang-selector [data-baseweb="select"] {
            background: var(--gray-100);
            border: 1px solid var(--gray-300);
            border-radius: var(--radius-md);
            min-height: 36px;
        }
        
        .lang-selector [data-baseweb="select"]:hover {
            border-color: var(--sava-primary);
            background: white;
        }
        
        /* Icono de carrito con badge */
        .cart-wrapper {
            position: relative;
        }
        
        .cart-badge {
            position: absolute;
            top: -6px;
            right: -6px;
            background: var(--error);
            color: white;
            font-size: 0.75rem;
            font-weight: 700;
            min-width: 20px;
            height: 20px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 6px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
            animation: badge-pop 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
        }
        
        @keyframes badge-pop {
            0% { transform: scale(0); }
            50% { transform: scale(1.2); }
            100% { transform: scale(1); }
        }
        
        /* Popover de usuario */
        [data-testid="stPopover"] {
            z-index: 1001;
        }
        
        [data-testid="stPopover"] > button {
            background: var(--gray-100);
            border: 1px solid var(--gray-300);
            border-radius: var(--radius-md);
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        
        [data-testid="stPopover"] > button:hover {
            background: white;
            border-color: var(--sava-primary);
            transform: translateY(-1px);
            box-shadow: var(--shadow-sm);
        }
        
        /* ========================================
           3. CONTENIDO PRINCIPAL
        ======================================== */
        .main .block-container {
            max-width: 1400px;
            padding-top: 110px;
            padding-bottom: var(--space-2xl);
            animation: fade-in 0.4s ease-out;
        }
        
        @keyframes fade-in {
            from {
                opacity: 0;
                transform: translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Títulos */
        h1, h2, h3 {
            color: var(--gray-900);
            font-weight: 700;
            letter-spacing: -0.02em;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: var(--space-lg);
        }
        
        h2 {
            font-size: 1.875rem;
            margin-bottom: var(--space-md);
        }
        
        h3 {
            font-size: 1.5rem;
        }
        
        /* ========================================
           4. TARJETAS DE PRODUCTO
        ======================================== */
        .product-card {
            background: white;
            border: 1px solid var(--gray-200);
            border-radius: var(--radius-lg);
            padding: var(--space-md);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        .product-card:hover {
            border-color: var(--sava-primary);
            box-shadow: var(--shadow-lg);
            transform: translateY(-4px);
        }
        
        .product-card img {
            border-radius: var(--radius-md);
            margin-bottom: var(--space-md);
            aspect-ratio: 1;
            object-fit: cover;
            background: var(--gray-100);
        }
        
        .product-price {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--sava-primary);
            margin: var(--space-sm) 0;
        }
        
        .product-rating {
            display: flex;
            align-items: center;
            gap: var(--space-xs);
            font-size: 0.875rem;
            color: var(--gray-600);
            margin-bottom: var(--space-md);
        }
        
        /* ========================================
           5. BOTONES
        ======================================== */
        .stButton > button {
            font-weight: 600;
            border-radius: var(--radius-md);
            transition: all 0.2s ease;
            border: none;
            font-size: 0.9375rem;
        }
        
        /* Botón primario */
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, var(--sava-primary) 0%, var(--sava-primary-dark) 100%);
            color: white;
            box-shadow: 0 2px 4px rgba(13, 148, 136, 0.2);
        }
        
        .stButton > button[kind="primary"]:hover {
            background: linear-gradient(135deg, var(--sava-primary-dark) 0%, var(--sava-primary) 100%);
            box-shadow: 0 4px 12px rgba(13, 148, 136, 0.3);
            transform: translateY(-2px);
        }
        
        .stButton > button[kind="primary"]:active {
            transform: translateY(0);
        }
        
        /* Botón secundario */
        .stButton > button[kind="secondary"] {
            background: white;
            color: var(--gray-700);
            border: 2px solid var(--gray-300);
        }
        
        .stButton > button[kind="secondary"]:hover {
            background: var(--gray-50);
            border-color: var(--sava-primary);
            color: var(--sava-primary);
            transform: translateY(-2px);
        }
        
        /* ========================================
           6. FORMULARIOS
        ======================================== */
        .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stNumberInput > div > div > input {
            border: 2px solid var(--gray-200);
            border-radius: var(--radius-md);
            padding: 0.625rem;
            transition: all 0.2s ease;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: var(--sava-primary);
            box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.1);
        }
        
        /* ========================================
           7. CARRITO Y CHECKOUT
        ======================================== */
        .cart-summary {
            background: white;
            border: 2px solid var(--gray-200);
            border-radius: var(--radius-lg);
            padding: var(--space-lg);
            position: sticky;
            top: 120px;
        }
        
        .cart-item {
            padding: var(--space-md);
            background: var(--gray-50);
            border-radius: var(--radius-md);
            margin-bottom: var(--space-sm);
            transition: background 0.2s ease;
        }
        
        .cart-item:hover {
            background: white;
            box-shadow: var(--shadow-sm);
        }
        
        /* ========================================
           8. SIDEBAR (solo en productos)
        ======================================== */
        section[data-testid="stSidebar"] {
            background: white;
            border-right: 1px solid var(--gray-200);
            padding-top: 110px;
        }
        
        section[data-testid="stSidebar"] .stButton > button {
            width: 100%;
            text-align: left;
            justify-content: flex-start;
            background: transparent;
            color: var(--gray-700);
            border: 1px solid transparent;
            margin-bottom: var(--space-xs);
        }
        
        section[data-testid="stSidebar"] .stButton > button:hover {
            background: var(--gray-50);
            border-color: var(--sava-primary);
            color: var(--sava-primary);
        }
        
        /* ========================================
           9. FOOTER
        ======================================== */
        .sava-footer {
            background: white;
            border-top: 1px solid var(--gray-200);
            padding: var(--space-2xl) var(--space-xl);
            margin-top: var(--space-2xl);
        }
        
        .footer-content {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .footer-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: var(--space-xl);
            margin-bottom: var(--space-xl);
        }
        
        .footer-col h4 {
            font-size: 1rem;
            font-weight: 600;
            color: var(--gray-900);
            margin-bottom: var(--space-md);
        }
        
        .footer-col ul {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        
        .footer-col li {
            margin-bottom: var(--space-sm);
        }
        
        .footer-col a {
            color: var(--gray-600);
            text-decoration: none;
            transition: color 0.2s ease;
            font-size: 0.9375rem;
        }
        
        .footer-col a:hover {
            color: var(--sava-primary);
        }
        
        .footer-bottom {
            padding-top: var(--space-lg);
            border-top: 1px solid var(--gray-200);
            text-align: center;
            color: var(--gray-500);
            font-size: 0.875rem;
        }
        
        /* ========================================
           10. UTILIDADES Y ESTADOS
        ======================================== */
        
        /* Loading skeleton */
        .skeleton {
            background: linear-gradient(
                90deg,
                var(--gray-200) 0%,
                var(--gray-100) 50%,
                var(--gray-200) 100%
            );
            background-size: 200% 100%;
            animation: skeleton-loading 1.5s ease-in-out infinite;
            border-radius: var(--radius-md);
        }
        
        @keyframes skeleton-loading {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
        }
        
        /* Toast notifications */
        .stSuccess, .stError, .stWarning, .stInfo {
            border-radius: var(--radius-md);
            padding: var(--space-md);
            animation: slide-in 0.3s ease-out;
        }
        
        @keyframes slide-in {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        /* ========================================
           11. RESPONSIVE
        ======================================== */
        @media (max-width: 768px) {
            .header-content {
                flex-wrap: wrap;
                padding: var(--space-sm) var(--space-md);
            }
            
            .header-search {
                order: 3;
                width: 100%;
                max-width: none;
                margin-top: var(--space-sm);
            }
            
            .header-nav {
                gap: var(--space-xs);
            }
            
            .header-nav .stButton > button {
                padding: 0.5rem;
                font-size: 0.875rem;
            }
            
            h1 {
                font-size: 1.875rem;
            }
            
            .main .block-container {
                padding-top: 140px;
            }
        }
        
        /* ========================================
           12. ACCESIBILIDAD
        ======================================== */
        *:focus-visible {
            outline: 2px solid var(--sava-primary);
            outline-offset: 2px;
        }
        
        button:focus-visible {
            outline: 2px solid var(--sava-primary);
            outline-offset: 2px;
        }
        
        /* Reducir animaciones para usuarios con preferencias */
        @media (prefers-reduced-motion: reduce) {
            *, *::before, *::after {
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# --- TEXTOS BILINGÜES MEJORADOS (ES/EN) ---
TEXTS = {
    'ES': {
        'search_placeholder': "Buscar productos, marcas y más...",
        'nav_categories': "Categorías",
        'nav_about': "Acerca de",
        'user_welcome': "Hola",
        'user_account': "Mi Cuenta",
        'user_orders': "Mis Compras",
        'user_logout': "Cerrar Sesión",
        'nav_signin': "Ingresar",
        'nav_signup': "Crear cuenta",
        'nav_cart': "Carrito",
        'page_home_title': "Descubre productos increíbles",
        'page_home_subtitle': "La mejor selección de productos a precios inmejorables",
        'page_featured_products': "Productos Destacados",
        'page_products': "Catálogo de Productos",
        'page_cart': "Mi Carrito",
        'page_checkout': "Finalizar Compra",
        'page_account': "Mi Cuenta",
        'page_orders': "Mis Pedidos",
        'page_about': "Acerca de SAVA",
        'filter_title': "Filtros",
        'filter_categories': "Categorías",
        'filter_all_categories': "Todas",
        'cart_empty': "Tu carrito está vacío",
        'cart_browse': "Explorar productos",
        'cart_summary': "Resumen",
        'cart_subtotal': "Subtotal",
        'cart_shipping': "Envío",
        'cart_tax': "IVA",
        'cart_total': "Total",
        'cart_checkout_button': "Proceder al pago",
        'back_to_products': "← Volver",
        'add_to_cart': "Agregar al carrito",
        'in_stock': "Disponible",
        'out_of_stock': "Agotado",
        'view_details': "Ver detalles",
        'quantity': "Cantidad",
        'reviews': "opiniones",
        'footer_customer': "Atención al Cliente",
        'footer_help': "Ayuda",
        'footer_returns': "Devoluciones",
        'footer_warranty': "Garantía",
        'footer_about': "Sobre SAVA",
        'footer_about_us': "Quiénes somos",
        'footer_careers': "Trabaja con nosotros",
        'footer_payment': "Métodos de Pago",
        'footer_cards': "Tarjetas",
        'footer_paypal': "PayPal",
        'footer_social': "Síguenos",
        'footer_copyright': "© 2025 SAVA Software for Engineering. Todos los derechos reservados.",
        'loading': "Cargando...",
        'no_products': "No se encontraron productos",
        'signin_required': "Inicia sesión para agregar al carrito"
    },
    'EN': {
        'search_placeholder': "Search products, brands, and more...",
        'nav_categories': "Categories",
        'nav_about': "About",
        'user_welcome': "Hello",
        'user_account': "My Account",
        'user_orders': "My Orders",
        'user_logout': "Sign Out",
        'nav_signin': "Sign In",
        'nav_signup': "Sign Up",
        'nav_cart': "Cart",
        'page_home_title': "Discover amazing products",
        'page_home_subtitle': "The best selection of products at unbeatable prices",
        'page_featured_products': "Featured Products",
        'page_products': "Product Catalog",
        'page_cart': "My Cart",
        'page_checkout': "Checkout",
        'page_account': "My Account",
        'page_orders': "My Orders",
        'page_about': "About SAVA",
        'filter_title': "Filters",
        'filter_categories': "Categories",
        'filter_all_categories': "All",
        'cart_empty': "Your cart is empty",
        'cart_browse': "Browse products",
        'cart_summary': "Summary",
        'cart_subtotal': "Subtotal",
        'cart_shipping': "Shipping",
        'cart_tax': "Tax",
        'cart_total': "Total",
        'cart_checkout_button': "Proceed to checkout",
        'back_to_products': "← Back",
        'add_to_cart': "Add to cart",
        'in_stock': "In stock",
        'out_of_stock': "Out of stock",
        'view_details': "View details",
        'quantity': "Quantity",
        'reviews': "reviews",
        'footer_customer': "Customer Service",
        'footer_help': "Help",
        'footer_returns': "Returns",
        'footer_warranty': "Warranty",
        'footer_about': "About SAVA",
        'footer_about_us': "About Us",
        'footer_careers': "Careers",
        'footer_payment': "Payment Methods",
        'footer_cards': "Cards",
        'footer_paypal': "PayPal",
        'footer_social': "Follow Us",
        'footer_copyright': "© 2025 SAVA Software for Engineering. All rights reserved.",
        'loading': "Loading...",
        'no_products': "No products found",
        'signin_required': "Sign in to add to cart"
    }
}

# --- Inicialización Session State ---
def init_session_state():
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
    if 'lang' not in st.session_state:
        st.session_state.lang = 'ES'
    if 'auth_tab' not in st.session_state:
        st.session_state.auth_tab = 'login'

init_session_state()
T = TEXTS[st.session_state.lang]

# --- Helpers ---
def update_cart_count():
    try:
        from services.firebase_service import FirebaseService
        firebase = FirebaseService()
        if st.session_state.user:
            cart = firebase.get_user_cart(st.session_state.user['uid'])
            st.session_state.cart_count = sum(item.get('quantity', 0) for item in cart)
        else:
            st.session_state.cart_count = 0
    except:
        st.session_state.cart_count = 0

def navigate_to(page: str):
    st.session_state.page = page
    st.rerun()

# --- HEADER REDISEÑADO ---
def render_header():
    st.markdown('<div class="sava-header">', unsafe_allow_html=True)
    st.markdown('<div class="header-content">', unsafe_allow_html=True)
    
    cols = st.columns([1.5, 4, 3])
    
    # Logo y marca
    with cols[0]:
        st.markdown('<div class="header-brand">', unsafe_allow_html=True)
        col_img, col_text = st.columns([1, 2])
        with col_img:
            st.image("https://github.com/GIUSEPPESAN21/LOGO-SAVA/blob/main/LOGO.jpg?raw=true", width=48)
        with col_text:
            if st.button("SAVA", key="home_btn", help="Ir al inicio"):
                navigate_to('home')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Búsqueda
    with cols[1]:
        st.markdown('<div class="header-search">', unsafe_allow_html=True)
        search = st.text_input(
            "search",
            placeholder=T['search_placeholder'],
            value=st.session_state.search_query,
            key="header_search",
            label_visibility="collapsed"
        )
        if search != st.session_state.search_query:
            st.session_state.search_query = search
            navigate_to('products')
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Navegación
    with cols[2]:
        st.markdown('<div class="header-nav">', unsafe_allow_html=True)
        
        # Idioma
        st.markdown('<div class="lang-selector">', unsafe_allow_html=True)
        lang = st.selectbox(
            "lang",
            options=['ES', 'EN'],
            index=0 if st.session_state.lang == 'ES' else 1,
            key='lang_select',
            label_visibility="collapsed"
        )
        if lang != st.session_state.lang:
            st.session_state.lang = lang
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Categorías
        if st.button(f"🗂️ {T['nav_categories']}", key="cat_btn"):
            navigate_to('products')
        
        # About
        if st.button(f"ℹ️ {T['nav_about']}", key="about_btn"):
            navigate_to('about')
        
        # Usuario
        if st.session_state.user:
            with st.popover(f"👤 {T['user_welcome']}, {st.session_state.user.get('display_name', 'User').split()[0]}"):
                st.markdown(f"**{st.session_state.user.get('display_name')}**")
                st.caption(st.session_state.user.get('email'))
                st.divider()
                if st.button(f"👤 {T['user_account']}", use_container_width=True):
                    navigate_to('account')
                if st.button(f"📦 {T['user_orders']}", use_container_width=True):
                    navigate_to('orders')
                if st.button(f"🚪 {T['user_logout']}", use_container_width=True):
                    st.session_state.user = None
                    st.session_state.cart_count = 0
                    navigate_to('home')
        else:
            if st.button(T['nav_signin'], key="signin_btn"):
                navigate_to('auth')
            if st.button(T['nav_signup'], key="signup_btn"):
                st.session_state.auth_tab = 'register'
                navigate_to('auth')
        
        # Carrito
        st.markdown('<div class="cart-wrapper">', unsafe_allow_html=True)
        if st.button(f"🛒 {T['nav_cart']}", key="cart_btn"):
            navigate_to('cart')
        if st.session_state.cart_count > 0:
            st.markdown(
                f'<div class="cart-badge">{st.session_state.cart_count}</div>',
                unsafe_allow_html=True
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

# --- SIDEBAR (solo productos) ---
def render_sidebar():
    with st.sidebar:
        st.title(f"🔍 {T['filter_title']}")
        st.divider()
        
        try:
            from services.firebase_service import FirebaseService
            firebase = FirebaseService()
            categories = firebase.get_categories()
            
            if categories:
                st.subheader(T['filter_categories'])
                
                if st.button(T['filter_all_categories'], use_container_width=True):
                    st.session_state.selected_category = None
                    st.rerun()
                
                for cat in categories:
                    if st.button(cat, key=f"cat_{cat}", use_container_width=True):
                        st.session_state.selected_category = cat
                        st.rerun()
                
                if st.session_state.selected_category:
                    st.success(f"✓ {st.session_state.selected_category}")
        except:
            pass

# --- PÁGINAS ---
def render_home_page():
    st.markdown(f"# {T['page_home_title']}")
    st.markdown(f"### {T['page_home_subtitle']}")
    
    # Banner promocional
    st.markdown("""
        <div style="background: linear-gradient(135deg, #0D9488 0%, #14B8A6 100%); 
                    padding: 3rem; border-radius: 16px; text-align: center; 
                    color: white; margin: 2rem 0;">
            <h2 style="margin: 0; font-size: 2rem;">🚚 Envío Gratis</h2>
            <p style="margin: 0.5rem 0 0; font-size: 1.1rem;">En tu primera compra</p>
        </div>
    """, unsafe_allow_html=True)
    
    try:
        from services.firebase_service import FirebaseService
        from components.product_list import render_product_grid
        
        firebase = FirebaseService()
        products = firebase.get_products(limit=8)
        
        if products:
            st.markdown(f"## {T['page_featured_products']}")
            render_product_grid(products, columns=4)
        else:
            st.info(T['no_products'])
    except Exception as e:
        st.warning(T['loading'])

def render_products_page():
    st.markdown(f"# {T['page_products']}")
    
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
        
        # Mostrar filtros activos
        filters = []
        if st.session_state.search_query:
            filters.append(f"🔍 {st.session_state.search_query}")
        if st.session_state.selected_category:
            filters.append(f"📁 {st.session_state.selected_category}")
        
        if filters:
            st.info(" • ".join(filters))
        
        if products:
            render_product_grid(products, columns=4)
        else:
            st.warning(T['no_products'])
    except:
        st.warning(T['loading'])

def render_product_detail_page():
    product_id = st.session_state.selected_product_id
    
    if not product_id:
        navigate_to('home')
        return
    
    try:
        from services.firebase_service import FirebaseService
        from utils.formatters import format_currency
        
        firebase = FirebaseService()
        product = firebase.get_product_by_id(product_id)
        
        if not product:
            st.error("Producto no encontrado")
            navigate_to('home')
            return
        
        if st.button(T['back_to_products']):
            st.session_state.selected_product_id = None
            navigate_to('products')
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            images = product.get('images', [])
            if images:
                st.image(images[0].get('url'), use_container_width=True)
            else:
                st.image("https://placehold.co/600x600/E5E7EB/9CA3AF?text=Sin+Imagen", use_container_width=True)
        
        with col2:
            st.markdown(f"# {product.get('name', 'Producto')}")
            
            rating = product.get('rating', 0)
            reviews = product.get('reviews_count', 0)
            if rating > 0:
                stars = "⭐" * int(rating)
                st.markdown(f"{stars} ({reviews} {T['reviews']})")
            
            st.markdown(f"<div class='product-price'>{format_currency(product.get('price', 0))}</div>", unsafe_allow_html=True)
            
            stock = product.get('stock', 0)
            if stock > 0:
                st.success(f"✅ {T['in_stock']}")
            else:
                st.error(f"❌ {T['out_of_stock']}")
            
            if st.session_state.user:
                if stock > 0:
                    qty = st.number_input(T['quantity'], min_value=1, max_value=min(stock, 10), value=1)
                    if st.button(T['add_to_cart'], type="primary", use_container_width=True):
                        if firebase.add_to_cart(st.session_state.user['uid'], product_id, qty):
                            st.success("✓ Agregado al carrito")
                            update_cart_count()
                            st.rerun()
            else:
                st.info(f"🔐 {T['signin_required']}")
            
            st.divider()
            st.markdown("### Descripción")
            st.write(product.get('description', ''))
    except Exception as e:
        st.error(str(e))

def render_cart_page():
    if not st.session_state.user:
        st.warning("Inicia sesión para ver tu carrito")
        navigate_to('auth')
        return
    
    st.markdown(f"# {T['page_cart']}")
    
    try:
        from services.firebase_service import FirebaseService
        from utils.formatters import format_currency, calculate_total
        
        firebase = FirebaseService()
        cart_items = firebase.get_user_cart(st.session_state.user['uid'])
        update_cart_count()
        
        if not cart_items:
            st.info(T['cart_empty'])
            if st.button(T['cart_browse'], type="primary"):
                navigate_to('products')
            return
        
        col_items, col_summary = st.columns([2, 1])
        
        with col_items:
            for item in cart_items:
                st.markdown('<div class="cart-item">', unsafe_allow_html=True)
                c1, c2, c3, c4 = st.columns([1, 3, 1, 1])
                
                with c1:
                    st.image(item.get('image', 'https://placehold.co/100x100'), width=80)
                with c2:
                    st.markdown(f"**{item.get('name')}**")
                    st.caption(format_currency(item.get('price', 0)))
                with c3:
                    qty_key = f"qty_{item['product_id']}"
                    new_qty = st.number_input(
                        "Q",
                        min_value=1,
                        max_value=99,
                        value=item.get('quantity', 1),
                        key=qty_key,
                        label_visibility="collapsed"
                    )
                    if new_qty != item.get('quantity', 1):
                        firebase.update_cart_item(st.session_state.user['uid'], item['product_id'], new_qty)
                        st.rerun()
                with c4:
                    if st.button("🗑️", key=f"del_{item['product_id']}"):
                        firebase.update_cart_item(st.session_state.user['uid'], item['product_id'], 0)
                        st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col_summary:
            st.markdown('<div class="cart-summary">', unsafe_allow_html=True)
            st.markdown(f"### {T['cart_summary']}")
            
            totals = calculate_total(cart_items, tax_rate=0.08, shipping=5.99)
            
            st.markdown(f"{T['cart_subtotal']}: **{format_currency(totals['subtotal'])}**")
            st.markdown(f"{T['cart_tax']}: **{format_currency(totals['tax'])}**")
            st.markdown(f"{T['cart_shipping']}: **{format_currency(totals['shipping'])}**")
            st.divider()
            st.markdown(f"### {T['cart_total']}: {format_currency(totals['total'])}")
            
            if st.button(T['cart_checkout_button'], type="primary", use_container_width=True):
                st.session_state.checkout_step = 'shipping'
                navigate_to('checkout')
            
            st.markdown('</div>', unsafe_allow_html=True)
    except Exception as e:
        st.error(str(e))

def render_checkout_page():
    if not st.session_state.user:
        navigate_to('auth')
        return
    
    st.markdown(f"# {T['page_checkout']}")
    
    try:
        from services.firebase_service import FirebaseService
        from components.checkout_form import render_checkout_form
        
        firebase = FirebaseService()
        cart_items = firebase.get_user_cart(st.session_state.user['uid'])
        
        if not cart_items:
            navigate_to('cart')
            return
        
        col1, col2 = st.columns([1.5, 1])
        
        with col1:
            render_checkout_form(cart_items)
        
        with col2:
            from utils.formatters import format_currency, calculate_total
            totals = calculate_total(cart_items, tax_rate=0.08, shipping=5.99)
            
            st.markdown('<div class="cart-summary">', unsafe_allow_html=True)
            st.markdown(f"### {T['cart_summary']}")
            
            for item in cart_items:
                st.caption(f"{item.get('name')} x{item.get('quantity')}")
            
            st.divider()
            st.markdown(f"**{T['cart_total']}: {format_currency(totals['total'])}**")
            st.markdown('</div>', unsafe_allow_html=True)
    except:
        pass

def render_auth_page():
    st.markdown(f"# {T['page_account']}")
    
    from components.auth import render_login_form, render_register_form
    
    tab1, tab2 = st.tabs([T['nav_signin'], T['nav_signup']])
    
    with tab1:
        render_login_form()
    with tab2:
        render_register_form()

def render_account_page():
    if not st.session_state.user:
        navigate_to('auth')
        return
    
    st.markdown(f"# {T['page_account']}")
    
    user = st.session_state.user
    st.markdown(f"**Nombre:** {user.get('display_name')}")
    st.markdown(f"**Email:** {user.get('email')}")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button(f"📦 {T['user_orders']}", use_container_width=True):
            navigate_to('orders')
    with col2:
        if st.button(f"🛒 {T['nav_cart']}", use_container_width=True):
            navigate_to('cart')

def render_orders_page():
    if not st.session_state.user:
        navigate_to('auth')
        return
    
    st.markdown(f"# {T['page_orders']}")
    
    try:
        from services.firebase_service import FirebaseService
        from utils.formatters import format_currency, format_date
        
        firebase = FirebaseService()
        orders = firebase.get_user_orders(st.session_state.user['uid'])
        
        if orders:
            for order in orders:
                with st.expander(f"Pedido #{order.get('id')[:8]} - {format_date(order.get('created_at'))}"):
                    st.markdown(f"**Estado:** {order.get('status', 'pending').upper()}")
                    totals = order.get('totals', {})
                    st.markdown(f"**Total:** {format_currency(totals.get('total', 0))}")
                    
                    items = order.get('items', [])
                    st.markdown("**Productos:**")
                    for item in items:
                        st.caption(f"• {item.get('name')} x{item.get('quantity')}")
        else:
            st.info("No tienes pedidos aún")
            if st.button(T['cart_browse'], type="primary"):
                navigate_to('products')
    except:
        pass

def render_about_page():
    from components.about import render_about_content
    render_about_content()

# --- FOOTER ---
def render_footer():
    footer_html = f"""
    <div class="sava-footer">
        <div class="footer-content">
            <div class="footer-grid">
                <div class="footer-col">
                    <h4>{T['footer_customer']}</h4>
                    <ul>
                        <li><a href="#">{T['footer_help']}</a></li>
                        <li><a href="#">{T['footer_returns']}</a></li>
                        <li><a href="#">{T['footer_warranty']}</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>{T['footer_about']}</h4>
                    <ul>
                        <li><a href="#">{T['footer_about_us']}</a></li>
                        <li><a href="#">{T['footer_careers']}</a></li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>{T['footer_payment']}</h4>
                    <ul>
                        <li>{T['footer_cards']}</li>
                        <li>{T['footer_paypal']}</li>
                    </ul>
                </div>
                <div class="footer-col">
                    <h4>{T['footer_social']}</h4>
                    <ul>
                        <li><a href="https://github.com/GIUSEPPESAN21" target="_blank">GitHub</a></li>
                        <li><a href="https://www.linkedin.com/in/joseph-javier-sánchez-acuña-150410275" target="_blank">LinkedIn</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>{T['footer_copyright']}</p>
            </div>
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

# --- MAIN ---
def main():
    render_header()
    update_cart_count()
    
    with st.container():
        if st.session_state.page == 'products':
            pass  # Sidebar se renderiza dentro de render_products_page()
        
        if st.session_state.selected_product_id:
            render_product_detail_page()
        else:
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
    
    render_footer()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.exception(e)
