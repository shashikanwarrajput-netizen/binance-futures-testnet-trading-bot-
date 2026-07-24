"""Simple Flask web interface for the Binance Futures testnet trading bot."""
from os import getenv
from pathlib import Path
from datetime import timedelta, datetime
import time
import random
import json
from typing import Any

from dotenv import load_dotenv
from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for,
    Response,
)

from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.exceptions import TradingBotError
from trading_bot.bot.logging_config import configure_logger
from trading_bot.bot.orders import OrderService

load_dotenv(Path(__file__).resolve().parent / "trading_bot" / ".env")
logger = configure_logger()

app = Flask(__name__)
app.config.update(
    SECRET_KEY=getenv("FLASK_SECRET_KEY", ""),
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    ENV=getenv("FLASK_ENV", "production"),
)

if not app.config["SECRET_KEY"]:
    raise RuntimeError("FLASK_SECRET_KEY is required in trading_bot/.env.")


def create_order_response(form: dict[str, Any]) -> dict[str, Any]:
    """Create an order using form values."""
    symbol = form.get("symbol", "").strip()
    side = form.get("side", "").strip()
    order_type = form.get("type", "").strip()
    quantity_text = form.get("quantity", "").strip()
    price_text = form.get("price", "").strip()

    logger.info(
        "Dashboard order submission: symbol=%s, side=%s, type=%s, quantity=%s, price=%s",
        symbol,
        side,
        order_type,
        quantity_text,
        "[REDACTED]" if price_text else "",
    )


def generate_price_stream():
    """Yield a simple server-sent events stream with simulated price ticks."""
    price = 63240.0
    while True:
        # small random walk to simulate price changes
        delta = (random.random() - 0.47) * 120
        price = max(1000.0, price + delta)
        payload = {"time": datetime.utcnow().isoformat() + "Z", "price": round(price, 2)}
        yield f"data: {json.dumps(payload)}\n\n"
        time.sleep(1)


@app.route("/stream")
def stream():
    """Server-Sent Events endpoint streaming price ticks."""
    return Response(generate_price_stream(), mimetype="text/event-stream")

    quantity = float(quantity_text)
    price = float(price_text) if price_text else None

    client = BinanceFuturesClient()
    service = OrderService(client)
    return service.place_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
    )


@app.route("/", methods=["GET", "POST"])
def login() -> Any:
    """Render a login page and establish a session."""
    if session.get("authenticated"):
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or "@" not in email:
            flash("Enter a valid email address.", "error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
        else:
            session["authenticated"] = True
            session["email"] = email
            session.permanent = True
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard() -> Any:
    """Render the trading dashboard and place orders."""
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    order_response: dict[str, Any] | None = None
    messages: list[str] = []

    if request.method == "POST":
        try:
            order_response = create_order_response(request.form)
            flash("Order sent successfully.", "success")
        except TradingBotError as error:
            logger.warning("Trading bot error: %s", error)
            messages.append(str(error))
        except ValueError as error:
            logger.warning("Invalid order input: %s", error)
            messages.append(str(error))
        except Exception as error:
            logger.exception("Unexpected dashboard error.")
            messages.append("An unexpected error occurred. Please try again later.")

    return render_template(
        "dashboard.html",
        order_response=order_response,
        messages=messages,
    )


@app.route("/logout")
def logout() -> Any:
    """Clear session and return to login."""
    session.clear()
    return redirect(url_for("login"))


@app.errorhandler(500)
def handle_internal_server_error(error: Exception) -> Any:
    logger.exception("Internal server error.")
    flash("An unexpected server error occurred. Please try again later.", "error")
    return redirect(url_for("dashboard"))


if __name__ == "__main__":
    # enable threaded so SSE streams and requests can be handled concurrently in dev
    app.run(host="0.0.0.0", port=5000, threaded=True)
