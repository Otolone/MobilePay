import os
from dotenv import load_dotenv

load_dotenv()


class PawaPayConfig:

    ENVIRONMENT: str = os.getenv("PAWAPAY_ENVIRONMENT", "sandbox")
    API_TOKEN: str | None = os.getenv("PAWAPAY_API_TOKEN")

    SANDBOX_BASE_URL = "https://api.sandbox.pawapay.io"
    PRODUCTION_BASE_URL = "https://api.pawapay.io"

    COUNTRY = "CMR"
    CURRENCY = "XAF"

    CORRESPONDENTS = {
        "MTN": "MTN_MOMO_CMR",
        "ORANGE": "ORANGE_CMR",
    }

    REQUEST_TIMEOUT_SECONDS = 30
    POLL_MAX_ATTEMPTS = 10
    POLL_INTERVAL_SECONDS = 5

    @classmethod
    def base_url(cls) -> str:
        if cls.ENVIRONMENT == "production":
            return cls.PRODUCTION_BASE_URL
        return cls.SANDBOX_BASE_URL

    @classmethod
    def reload(cls) -> None:
        """Re-read env vars without restarting the process. Call after os.environ changes."""
        cls.ENVIRONMENT = os.getenv("PAWAPAY_ENVIRONMENT", "sandbox")
        cls.API_TOKEN = os.getenv("PAWAPAY_API_TOKEN")
