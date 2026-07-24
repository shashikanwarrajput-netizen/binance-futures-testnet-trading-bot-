"""Order placement logic for the trading bot."""
from typing import Any, Dict

from .client import BinanceFuturesClient
from .exceptions import InvalidOrderError
from .logging_config import configure_logger
from .validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)

logger = configure_logger()


class OrderService:
    """Business logic for Binance Futures orders."""

    def __init__(self, client: BinanceFuturesClient) -> None:
        self.client = client

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None,
    ) -> Dict[str, Any]:
        """Validate inputs and place an order."""
        normalized_symbol = symbol.upper().strip()
        normalized_order_type = order_type.upper().strip()
        normalized_side = side.upper().strip()

        try:
            validate_symbol(normalized_symbol)
            validate_side(normalized_side)
            validate_order_type(normalized_order_type)
            validate_quantity(quantity)
            validate_price(normalized_order_type, price)
        except ValueError as error:
            logger.warning("Order validation failed: %s", error)
            raise InvalidOrderError(str(error)) from error

        if normalized_order_type == "MARKET" and price is not None:
            message = "Price must not be provided for MARKET orders."
            logger.warning(message)
            raise InvalidOrderError(message)

        return self.client.create_order(
            normalized_symbol,
            normalized_side,
            normalized_order_type,
            quantity,
            price,
        )
