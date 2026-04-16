import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
MIN_SCORE = 60.0  # Default minimum score threshold for job matching