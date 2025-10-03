import os
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

from openai import OpenAI
OPENAI_CLIENT = OpenAI()

DIVORCE_VS = os.getenv("DIVORCE_VS")

VECTOR_STORES = [DIVORCE_VS]

MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY", "API_KEY")
MAILGUN_SANDBOX_DOMAIN = os.getenv("MAILGUN_SANDBOX_DOMAIN", "SANDBOX")
MAILGUN_SANDBOX_USER = os.getenv("MAILGUN_SANDBOX_USER", "MAILGUN_SANDBOX_USER")

PASSWORD = os.getenv("PASSWORD", "PASSWORD")
