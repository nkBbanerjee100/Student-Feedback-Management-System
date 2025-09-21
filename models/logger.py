import datetime
import os

class Logger:
    def __init__(self, logfile="logs/app.log"):
        self.logfile = logfile
        os.makedirs(os.path.dirname(self.logfile), exist_ok=True)

    def write_log(self, action, message):
        """Write log entry to file"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{action}] {message}\n"
        try:
            with open(self.logfile, "a") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Failed to write log: {e}")
