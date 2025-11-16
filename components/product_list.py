"""
Product list component for displaying products in grid.
"""
import streamlit as st
from typing import List, Dict, Any
from components.product_card import render_product_card


def render_product_grid(products: List[Dict[str, Any]], columns: int = 4):
    """
    Render products in a grid layout.
    
    Args:
        products: List of product dictionaries
        columns: Number of columns in grid
    """
    if not products:
        st.info("No products found.")
        return
    
    for i in range(0, len(products), columns):
        cols = st.columns(columns)
        
        for j, col in enumerate(cols):
            if i + j < len(products):
                with col:
                    render_product_card(products[i + j], key_prefix=f"grid_{i}_{j}")

