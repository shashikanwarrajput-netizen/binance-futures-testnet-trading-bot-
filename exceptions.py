"""Custom exceptions for trading bot operations."""

class TradingBotError(Exception):
    """Base exception for trading bot errors."""


class InvalidOrderError(TradingBotError):
    """Raised when user input is invalid."""


class BinanceAPIError(TradingBotError):
    """Raised when Binance returns an API error."""


class NetworkError(TradingBotError):
    """Raised when a network error occurs."""


class AuthenticationError(TradingBotError):
    """Raised when API credentials are missing or invalid."""
