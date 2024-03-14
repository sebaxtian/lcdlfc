import os

from dotenv import load_dotenv

# Load .env variables
_ = load_dotenv(dotenv_path=".env")


def get(env_name: str) -> str | None:
    return os.getenv(env_name, None)
