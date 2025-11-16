"""
Formatting utilities for displaying data.
"""
from typing import Optional
from datetime import datetime


def format_currency(amount: float, currency_symbol: str = '$') -> str:
    """Format amount as currency."""
    try:
        return f"{currency_symbol}{amount:,.2f}"
    except (ValueError, TypeError):
        return f"{currency_symbol}0.00"


def format_date(date: datetime, format_str: str = "%B %d, %Y") -> str:
    """Format datetime object as string."""
    try:
        if isinstance(date, datetime):
            return date.strftime(format_str)
        return str(date)
    except (ValueError, TypeError):
        return "Invalid date"


def format_phone(phone: str) -> str:
    """Format phone number for display."""
    if not phone:
        return ""
    
    digits = ''.join(filter(str.isdigit, phone))
    
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    
    return phone


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length with ellipsis."""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length - 3] + "..."


def format_order_status(status: str) -> str:
    """Format order status for display."""
    status_map = {
        'pending': 'Pending',
        'processing': 'Processing',
        'shipped': 'Shipped',
        'delivered': 'Delivered',
        'cancelled': 'Cancelled'
    }
    return status_map.get(status.lower(), status.title())


def calculate_total(items: list, tax_rate: float = 0.0, shipping: float = 0.0) -> dict:
    """Calculate cart/order totals."""
    subtotal = sum(item.get('price', 0) * item.get('quantity', 0) for item in items)
    tax = subtotal * tax_rate
    total = subtotal + tax + shipping
    
    return {
        'subtotal': subtotal,
        'tax': tax,
        'shipping': shipping,
        'total': total
    }

