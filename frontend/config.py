import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
MIN_SCORE = int(os.getenv("MIN_SCORE", 90))