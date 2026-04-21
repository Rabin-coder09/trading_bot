import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from bot.logging_config import setup_logger

logger = setup_logger("client")

class BinanceClient:
    def __init__(self, api_key: str, secret_key: str, base_url: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        })

    def _sign(self, params: dict) -> dict:
        """Add timestamp and signature to params."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = urlencode(params)
        signature = hmac.new(
            self.secret_key.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def post(self, endpoint: str, params: dict) -> dict:
        """Send signed POST request."""
        url = f"{self.base_url}{endpoint}"
        signed_params = self._sign(params)

        logger.debug(f"POST {url} | params: { {k: v for k, v in signed_params.items() if k != 'signature'} }")

        try:
            response = self.session.post(url, params=signed_params)
            data = response.json()

            if response.status_code == 200:
                logger.debug(f"Response: {data}")
            else:
                logger.error(f"API Error {response.status_code}: {data}")

            return {"status_code": response.status_code, "data": data}

        except requests.exceptions.ConnectionError:
            logger.error("Network error: Could not connect to Binance API")
            raise ConnectionError("Network error: Could not connect to Binance API")

        except requests.exceptions.Timeout:
            logger.error("Request timed out")
            raise TimeoutError("Request timed out")

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise

    def get(self, endpoint: str, params: dict = {}) -> dict:
        """Send signed GET request."""
        url = f"{self.base_url}{endpoint}"
        signed_params = self._sign(params)

        logger.debug(f"GET {url} | params: {signed_params}")

        try:
            response = self.session.get(url, params=signed_params)
            data = response.json()
            return {"status_code": response.status_code, "data": data}

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise