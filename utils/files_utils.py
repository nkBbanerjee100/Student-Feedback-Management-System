class FUtils:
    @staticmethod
    def get_log_file_path():
        from flask import current_app
        import os
        logs_dir = os.path.join(current_app.root_path, "logs")
        os.makedirs(logs_dir, exist_ok=True)
        return os.path.join(logs_dir, "app.log")
