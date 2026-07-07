"""High-level controller for managing downloads via the engine."""

from typing import Optional

class DownloadController:
    """Coordinate download jobs and handle lifecycle events."""

    def __init__(self, engine=None):
        self.engine = engine

    def start_download(self, *cmd_parts, cwd: Optional[str]=None):
        """Start a download and return a generator of progress dicts."""
        if self.engine is None:
            raise RuntimeError("No engine configured")
        return self.engine.run(*cmd_parts, cwd=cwd)
