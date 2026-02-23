import datetime

class Logger:

    @staticmethod
    def log(message):
        timestamp = datetime.datetime.now().isoformat()
        print(f"[{timestamp}] {message}")
