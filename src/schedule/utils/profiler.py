import time
import logging

logger = logging.getLogger(__name__)

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        result = func(*args, **kwargs)

        duration = time.perf_counter() - start
        logger.info(f"{func.__name__} took {duration:.4f}s")

        return result
    return wrapper