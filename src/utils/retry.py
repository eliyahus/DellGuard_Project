"""Retry logic for transient failures

Example usage:
    @retry(max_attempts=3, delay=1.0, backoff=2.0)
    def call_external_api():
        response = requests.get("https://api.example.com")
        return response.json()
    
    # Will retry up to 3 times with delays: 1s, 2s, 4s
"""

import time
import logging
from functools import wraps
from typing import Callable, TypeVar, Any

logger = logging.getLogger(__name__)

T = TypeVar('T')


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Retry decorator for handling transient failures with exponential backoff.
    
    Useful for network calls, external APIs, or any operation that may
    temporarily fail but succeed on retry.
    
    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        delay: Initial delay between retries in seconds (default: 1.0)
        backoff: Multiplier for delay after each attempt (default: 2.0)
                 Example: delay=1.0, backoff=2.0 → delays of 1s, 2s, 4s
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            current_delay = delay
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt == max_attempts:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts")
                        raise
                    
                    logger.warning(f"{func.__name__} failed (attempt {attempt}/{max_attempts}): {e}")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            raise last_exception  # type: ignore
        
        return wrapper
    return decorator
