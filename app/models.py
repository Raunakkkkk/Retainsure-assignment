import threading
from datetime import datetime
from typing import Dict, Optional


class URLStore:
    """In-memory storage for URL mappings with thread safety."""
    
    def __init__(self):
        self.urls: Dict[str, Dict] = {}  # {short_code: {url, clicks, created_at}}
        self.lock = threading.Lock()
    
    def save_url(self, short_code: str, original_url: str) -> None:
        """Save a URL mapping with initial metadata."""
        with self.lock:
            self.urls[short_code] = {
                'url': original_url,
                'clicks': 0,
                'created_at': datetime.utcnow().isoformat()
            }
    
    def get_url(self, short_code: str) -> Optional[Dict]:
        """Get URL data for a short code."""
        return self.urls.get(short_code)
    
    def increment_clicks(self, short_code: str) -> bool:
        """Increment click count for a short code. Returns True if successful."""
        with self.lock:
            if short_code in self.urls:
                self.urls[short_code]['clicks'] += 1
                return True
            return False
    
    def code_exists(self, short_code: str) -> bool:
        """Check if a short code already exists."""
        return short_code in self.urls