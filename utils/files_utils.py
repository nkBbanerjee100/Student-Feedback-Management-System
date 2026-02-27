"""Filesystem helpers for application runtime files."""

class FUtils:
    """Utility helpers grouped as static methods."""

    @staticmethod
    def get_log_file_path():
        """Return absolute log file path and ensure log directory exists."""
        from flask import current_app
        import os
        logs_dir = os.path.join(current_app.root_path, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        return os.path.join(logs_dir, "app.log")
