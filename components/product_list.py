"""
Product list component with modern grid layout.
REDISEÑO UX/UI - Grid responsive y tarjetas profesionales
"""
import streamlit as st
from typing import List, Dict, Any


def render_product_grid(products: List[Dict[str, Any]], columns: int = 4):
    """
    Render products in a modern responsive grid.
    
    Args:
        products: List of product dictionaries
        columns: Number of columns (default: 4)
    """
    if not products:
        st.info("No se encontraron productos.")
        return
    
    # Responsive grid: usa CSS Grid nativo de Streamlit
    for i in range(0, len(products), columns):
        cols = st.columns(columns)
        
        for j, col in enumerate(cols):
            if i + j < len(products):
                with col:
                    render_product_card(products[i + j], key_prefix=f"grid_{i}_{j}")


def render_product_card(product: Dict[str, Any], key_prefix: str = ""):
    """
    Render a single product card with modern design.
    
    Args:
        product: Product dictionary
        key_prefix: Unique key prefix for Streamlit widgets
    """
    product_id = product.get('id', '')
    name = product.get('name', 'Producto')
    price = product.get('price', 0)
    images = product.get('images', [])
    rating = product.get('rating', 0)
    reviews_count = product.get('reviews_count', 0)
    stock = product.get('stock', 0)
    in_stock = stock > 0
    
    image_url = images[0].get('url', '') if images else ''
    
    # Contenedor de tarjeta con clase CSS personalizada
    st.markdown('<div class="product-card">', unsafe_allow_html=True)
    
    # Imagen del producto
    if image_url:
        st.image(image_url, use_container_width=True)
    else:
        st.image(
            "https://placehold.co/400x400/E5E7EB/9CA3AF?text=Sin+Imagen",
            use_container_width=True
        )
    
    # Nombre del producto (truncado)
    product_name = name if len(name) <= 50 else name[:47] + "..."
    st.markdown(f"### {product_name}")
    
    # Rating y reviews
    if rating > 0:
        stars = "⭐" * int(rating) + "☆" * (5 - int(rating))
        st.markdown(
            f'<div class="product-rating">{stars} <span>({reviews_count})</span></div>',
            unsafe_allow_html=True
        )
    
    # Precio
    from utils.formatters import format_currency
    st.markdown(
        f'<div class="product-price">{format_currency(price)}</div>',
        unsafe_allow_html=True
    )
    
    # Estado de stock
    if in_stock:
        st.success("✅ Disponible", icon="✅")
    else:
        st.error("❌ Agotado", icon="❌")
    
    # Botones de acción
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(
            "Ver detalles",
            key=f"{key_prefix}_view_{product_id}",
            use_container_width=True,
            type="secondary"
        ):
            st.session_state.selected_product_id = product_id
            st.rerun()
    
    with col2:
        if st.session_state.get('user'):
            if in_stock:
                if st.button(
                    "Agregar",
                    key=f"{key_prefix}_add_{product_id}",
                    use_container_width=True,
                    type="primary"
                ):
                    from services.firebase_service import FirebaseService
                    firebase = FirebaseService()
                    
                    success = firebase.add_to_cart(
                        st.session_state.user['uid'],
                        product_id,
                        1  # Cantidad por defecto
                    )
                    
                    if success:
                        st.success("✓ Agregado", icon="✅")
                        # Actualizar contador del carrito
                        if 'cart_count' in st.session_state:
                            st.session_state.cart_count += 1
                        st.rerun()
                    else:
                        st.error("Error al agregar")
            else:
                st.button(
                    "Agotado",
                    key=f"{key_prefix}_sold_{product_id}",
                    use_container_width=True,
                    disabled=True
                )
        else:
            # Si no hay usuario, mostrar botón para iniciar sesión
            if st.button(
                "Ingresar",
                key=f"{key_prefix}_login_{product_id}",
                use_container_width=True,
                type="primary"
            ):
                st.session_state.page = 'auth'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)


def render_product_skeleton(count: int = 8):
    """
    Render skeleton loaders for products while loading.
    
    Args:
        count: Number of skeleton cards to show
    """
    st.markdown("""
        <style>
            .skeleton-card {
                background: white;
                border: 1px solid var(--gray-200);
                border-radius: var(--radius-lg);
                padding: var(--space-md);
                margin-bottom: var(--space-md);
            }
            
            .skeleton-img {
                width: 100%;
                height: 250px;
                background: linear-gradient(
                    90deg,
                    #E5E7EB 0%,
                    #F3F4F6 50%,
                    #E5E7EB 100%
                );
                background-size: 200% 100%;
                animation: skeleton-loading 1.5s ease-in-out infinite;
                border-radius: var(--radius-md);
                margin-bottom: var(--space-md);
            }
            
            .skeleton-text {
                height: 20px;
                background: linear-gradient(
                    90deg,
                    #E5E7EB 0%,
                    #F3F4F6 50%,
                    #E5E7EB 100%
                );
                background-size: 200% 100%;
                animation: skeleton-loading 1.5s ease-in-out infinite;
                border-radius: 4px;
                margin-bottom: var(--space-sm);
            }
            
            @keyframes skeleton-loading {
                0% { background-position: 200% 0; }
                100% { background-position: -200% 0; }
            }
        </style>
    """, unsafe_allow_html=True)
    
    cols = st.columns(4)
    
    for i in range(count):
        with cols[i % 4]:
            st.markdown("""
                <div class="skeleton-card">
                    <div class="skeleton-img"></div>
                    <div class="skeleton-text" style="width: 80%;"></div>
                    <div class="skeleton-text" style="width: 60%;"></div>
                    <div class="skeleton-text" style="width: 40%;"></div>
                </div>
            """, unsafe_allow_html=True)
