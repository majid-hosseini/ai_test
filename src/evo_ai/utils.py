"""
Utility functions for the Evo AI Agent.
"""

import functools
import logging
from typing import Any, Callable, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")


def with_logging(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator that adds logging functionality to functions.
    Logs function calls and exceptions.
    
    Args:
        func: The function to be decorated.
        
    Returns:
        The decorated function with logging.
    """
    @functools.wraps(func)
    async def async_wrapper(*args: Any, **kwargs: Any) -> T:
        function_name = func.__name__
        logger.info(f"Calling function: {function_name}")
        try:
            result = await func(*args, **kwargs)
            logger.info(f"Function {function_name} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Function {function_name} failed with error: {e}", exc_info=True)
            raise
    
    @functools.wraps(func)
    def sync_wrapper(*args: Any, **kwargs: Any) -> T:
        function_name = func.__name__
        logger.info(f"Calling function: {function_name}")
        try:
            result = func(*args, **kwargs)
            logger.info(f"Function {function_name} completed successfully")
            return result
        except Exception as e:
            logger.error(f"Function {function_name} failed with error: {e}", exc_info=True)
            raise
    
    # Return the appropriate wrapper based on whether the function is async or not
    if hasattr(func, '__code__') and func.__code__.co_flags & 0x80:  # Check if coroutine
        return async_wrapper
    else:
        return sync_wrapper 