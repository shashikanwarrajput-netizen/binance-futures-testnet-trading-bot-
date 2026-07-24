"""Binance Futures client wrapper for order placement."""
from os import getenv
from pathlib import Path
from typing import Any, Dict

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from dotenv import load_dotenv

from .exceptions import AuthenticationError, BinanceAPIError, NetworkError
from .logging_config import configure_logger


class BinanceFuturesClient:
    """Client for Binance Futures Testnet requests."""

    BASE_URL = "https://testnet.binancefuture.com"

    def __init__(self) -> None:
        project_root = Path(__file__).resolve().parents[1]
        load_dotenv(project_root / ".env")

        api_key = getenv("BINANCE_API_KEY", "")
        api_secret = getenv("BINANCE_API_SECRET", "")
        if not api_key or not api_secret:
            raise AuthenticationError(
                "Missing BINANCE_API_KEY or BINANCE_API_SECRET in .env file."
            )

        self.logger = configure_logger()
        self.client = Client(api_key, api_secret, testnet=True)
        self.client.API_URL = self.BASE_URL
        self.client.FUTURES_URL = self.BASE_URL

    def create_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None,
    ) -> Dict[str, Any]:
        """Place an order on Binance Futures Testnet."""
        payload: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if price is not None:
            payload["price"] = price
            payload["timeInForce"] = "GTC"

        self.logger.info("Sending Binance order request: %s", payload)

        try:
            response = self.client.futures_create_order(**payload)
        except BinanceAPIException as error:
            self.logger.exception("Binance API error while placing order.")
            raise BinanceAPIError(str(error)) from error
        except BinanceRequestException as error:
            self.logger.exception("Network error while placing order.")
            raise NetworkError(str(error)) from error
        except Exception as error:
            self.logger.exception("Unexpected error in Binance client.")
            raise BinanceAPIError("Unexpected Binance client error.") from error

        self.logger.info("Binance order response: %s", response)
        return response
