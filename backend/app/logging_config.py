import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    handler = RotatingFileHandler("logs/app.log", maxBytes=5*1024*1024, backupCount=3)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(handler)
