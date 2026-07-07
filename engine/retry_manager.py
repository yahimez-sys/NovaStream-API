"""Simple retry manager for transient failures."""

import time

class RetryManager:
    """Provides a retry loop for callables."""

    def __init__(self, retries: int = 3, delay: float = 1.0):
        self.retries = retries
        self.delay = delay

    def run(self, func, *args, **kwargs):
        last_exc = None
        for attempt in range(1, self.retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exc = e
                time.sleep(self.delay)
        raise last_exc
