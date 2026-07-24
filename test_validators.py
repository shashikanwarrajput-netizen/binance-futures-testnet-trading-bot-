"""Unit tests for trading bot validators."""
import pytest

from trading_bot.bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)


def test_validate_symbol_raises_for_empty() -> None:
    with pytest.raises(ValueError):
        validate_symbol("")


def test_validate_side_rejects_invalid() -> None:
    with pytest.raises(ValueError):
        validate_side("HOLD")


def test_validate_order_type_rejects_invalid() -> None:
    with pytest.raises(ValueError):
        validate_order_type("STOP")


def test_validate_quantity_rejects_non_positive() -> None:
    with pytest.raises(ValueError):
        validate_quantity(0)


def test_validate_price_requires_for_limit() -> None:
    with pytest.raises(ValueError):
        validate_price("LIMIT", None)


def test_validate_price_rejects_non_positive() -> None:
    with pytest.raises(ValueError):
        validate_price("LIMIT", 0)
