import random
import string
import re
from typing import Set


def generate_short_code(length: int = 6, existing_codes: Set[str] = None) -> str:
    """Generate a unique 6-character alphanumeric code."""
    chars = string.ascii_letters + string.digits
    
    # Generate codes until we find one that doesn't exist
    max_attempts = 100
    for _ in range(max_attempts):
        code = ''.join(random.choice(chars) for _ in range(length))
        if existing_codes is None or code not in existing_codes:
            return code
    
    # If we can't find a unique code after max_attempts, raise an error
    raise Exception("Unable to generate unique short code")


def is_valid_url(url: str) -> bool:
    """Basic URL validation using regex."""
    if not url or not isinstance(url, str):
        return False
    
    # Basic URL pattern - must start with http/https/ftp
    url_pattern = re.compile(
        r'^(https?|ftp)://[^\s/$.?#].[^\s]*$', 
        re.IGNORECASE
    )
    return bool(url_pattern.match(url.strip()))


def validate_short_code(short_code: str) -> bool:
    """Validate short code format (6 alphanumeric characters)."""
    if not short_code or len(short_code) != 6:
        return False
    return short_code.isalnum()