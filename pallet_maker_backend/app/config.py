from dotenv import load_dotenv
import os

load_dotenv()

URL = os.getenv("URL", "http://localhost:4840")
NODE_IDS = os.getenv("NODE_IDS", "").split(",")
USERNAME = os.getenv("USERNAME", "admin")
PASSWORD = os.getenv("PASSWORD", "password123")