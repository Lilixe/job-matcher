import os

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")
min_score = 50.0  # Default minimum score threshold for job matching