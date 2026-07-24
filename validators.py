"""Validate CLI inputs and order parameters."""
from typing import Optional

from .logging_config import configure_logger

SUPPORTED_ORDER_TYPES = {"MARKET", "LIMIT"}
SUPPORTED_SIDES = {"BUY", "SELL"}
logger = configure_logger()


def validate_api_keys(api_key: str, api_secret: str) -> None:
    """Validate that Binance API credentials are present."""
    if not api_key or not api_secret:
        message = "API credentials are required in the .env file."
        logger.warning(message)
        raise ValueError(message)


def validate_symbol(symbol: str) -> None:
    """Validate the trading symbol."""
    if not symbol or not symbol.strip():
        message = "Symbol must be a non-empty string."
        logger.warning(message)
        raise ValueError(message)
    if not symbol.strip().isalnum():
        message = "Symbol must contain only letters and numbers."
        logger.warning(message)
        raise ValueError(message)


def validate_side(side: str) -> None:
    """Validate BUY/SELL side values."""
    if side.upper() not in SUPPORTED_SIDES:
        message = "Side must be BUY or SELL."
        logger.warning(message)
        raise ValueError(message)


def validate_order_type(order_type: str) -> None:
    """Validate order type values."""
    if order_type.upper() not in SUPPORTED_ORDER_TYPES:
        message = "Order type must be MARKET or LIMIT."
        logger.warning(message)
        raise ValueError(message)


def validate_quantity(quantity: float) -> None:
    """Validate order quantity values."""
    if quantity <= 0:
        message = "Quantity must be a positive number."
        logger.warning(message)
        raise ValueError(message)


def validate_price(order_type: str, price: Optional[float]) -> None:
    """Validate that price is present when required."""
    if order_type.upper() == "LIMIT":
        if price is None:
            message = "Price is mandatory for LIMIT orders."
            logger.warning(message)
            raise ValueError(message)
        if price <= 0:
            message = "Price must be a positive number."
            logger.warning(message)
            raise ValueError(message)
