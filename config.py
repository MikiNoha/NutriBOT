import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_fallback_key")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")S

