"""
Validation utilities for forms and data.
"""
import re
from typing import Tuple, Optional


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    """Validate email address format."""
    if not email or not email.strip():
        return False, "Email is required"
    
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email.strip()):
        return False, "Please enter a valid email address"
    
    return True, None


def validate_password(password: str) -> Tuple[bool, Optional[str]]:
    """Validate password strength."""
    if not password:
        return False, "Password is required"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    return True, None


def validate_name(name: str) -> Tuple[bool, Optional[str]]:
    """Validate name field."""
    if not name or not name.strip():
        return False, "Name is required"
    
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    
    return True, None


def validate_phone(phone: str) -> Tuple[bool, Optional[str]]:
    """Validate phone number format."""
    if not phone or not phone.strip():
        return False, "Phone number is required"
    
    cleaned = re.sub(r'[\s\-\(\)]', '', phone.strip())
    
    if cleaned.startswith('+'):
        cleaned = cleaned[1:]
    
    if not cleaned.isdigit():
        return False, "Phone number must contain only digits"
    
    if len(cleaned) < 10:
        return False, "Phone number must be at least 10 digits"
    
    return True, None


def validate_price(price: float) -> Tuple[bool, Optional[str]]:
    """Validate product price."""
    if price is None:
        return False, "Price is required"
    
    try:
        price_float = float(price)
        if price_float < 0:
            return False, "Price cannot be negative"
        if price_float == 0:
            return False, "Price must be greater than zero"
        return True, None
    except (ValueError, TypeError):
        return False, "Price must be a valid number"


def validate_quantity(quantity: int) -> Tuple[bool, Optional[str]]:
    """Validate product quantity."""
    if quantity is None:
        return False, "Quantity is required"
    
    try:
        quantity_int = int(quantity)
        if quantity_int < 1:
            return False, "Quantity must be at least 1"
        if quantity_int > 999:
            return False, "Quantity cannot exceed 999"
        return True, None
    except (ValueError, TypeError):
        return False, "Quantity must be a valid integer"


def validate_address(address_data: dict) -> Tuple[bool, Optional[str]]:
    """Validate shipping address."""
    required_fields = ['street', 'city', 'state', 'zip_code', 'country']
    
    for field in required_fields:
        if not address_data.get(field) or not str(address_data[field]).strip():
            return False, f"{field.replace('_', ' ').title()} is required"
    
    zip_code = str(address_data['zip_code']).strip()
    if not zip_code.isdigit() and len(zip_code) < 5:
        return False, "Zip code must be at least 5 digits"
    
    return True, None

