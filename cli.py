"""CLI for the Binance Futures Testnet trading bot."""
import argparse
import sys
from typing import Any

from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.orders import OrderService
from trading_bot.bot.exceptions import TradingBotError
from trading_bot.bot.logging_config import configure_logger

logger = configure_logger()


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Place Binance Futures testnet orders.")
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL"], help="Order side")
    parser.add_argument(
        "--type", required=True, choices=["MARKET", "LIMIT"], help="Order type"
    )
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument("--price", type=float, help="Price for LIMIT orders")
    return parser.parse_args()


def format_order_summary(response: dict[str, Any]) -> str:
    """Format the order response for printing."""
    return (
        f"Order Summary:\n"
        f"  Symbol: {response.get('symbol')}\n"
        f"  Side: {response.get('side')}\n"
        f"  Type: {response.get('type')}\n"
        f"  Order ID: {response.get('orderId')}\n"
        f"  Status: {response.get('status')}\n"
        f"  Executed Quantity: {response.get('executedQty')}\n"
        f"  Average Price: {response.get('avgPrice')}\n"
    )


def main() -> None:
    """Execute the CLI command."""
    args = parse_args()
    client = BinanceFuturesClient()
    service = OrderService(client)

    try:
        response = service.place_order(
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
        )
        logger.info(
            "CLI order executed: symbol=%s, side=%s, type=%s, quantity=%s, price=%s",
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price,
        )
        print(format_order_summary(response))
    except TradingBotError as error:
        logger.warning("CLI order failed: %s", error)
        print(f"Error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
