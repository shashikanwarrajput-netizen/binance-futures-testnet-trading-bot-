# Binance Futures Testnet Trading Bot

A polished Python trading bot project for Binance Futures Testnet, with both CLI and Flask web UI support.

## Project Overview

This project demonstrates a structured trading bot that:
- places Binance Futures Testnet orders
- supports both `MARKET` and `LIMIT` orders
- supports `BUY` and `SELL` sides
- validates user inputs before submission
- logs API requests, responses, and validation errors
- handles errors gracefully
- offers a simple web dashboard and command-line interface

## Features

- Binance Futures Testnet integration
- CLI order placement
- Flask-based trading dashboard
- validation for symbols, sides, order types, quantity, and limit price
- environment-based configuration
- secure session handling in Flask
- file-based logging in `logs/trading.log`

## Folder Structure

```text
trading_bot/
│
├── bot/
│   ├── client.py
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── orders.py
│   └── validators.py
│
├── logs/
├── tests/
│   └── test_validators.py
├── cli.py
├── project.py
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore
```

## Installation

1. Create a virtual environment:

```bash
python -m venv venv
```

2. Activate the environment:

- Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

- macOS/Linux:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Copy `.env.example` to `.env` and provide your Binance Futures Testnet credentials plus a Flask secret key:

```ini
BINANCE_API_KEY=your_testnet_api_key_here
BINANCE_API_SECRET=your_testnet_api_secret_here
FLASK_SECRET_KEY=replace_with_secure_random_string
```

## Running the CLI

From the project root:

```bash
python trading_bot/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Or use the root entry point:

```bash
python project.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Example MARKET order

```bash
python trading_bot/cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

### Example LIMIT order

```bash
python trading_bot/cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 35000
```

## Running the Flask Web App

From the project root:

```bash
python web_app.py
```

Open `http://localhost:5000` in your browser.

## Sample Output

Market order success:

```text
Order Summary:
  Symbol: BTCUSDT
  Side: BUY
  Type: MARKET
  Order ID: 123456789
  Status: NEW
  Executed Quantity: 0.001
  Average Price: 0
```

Limit order success:

```text
Order Summary:
  Symbol: BTCUSDT
  Side: SELL
  Type: LIMIT
  Order ID: 987654321
  Status: NEW
  Executed Quantity: 0
  Average Price: 0
```

## Logging

- Logs are written to `logs/trading.log`
- Errors are also captured in `logs/error.log`
- Validation issues and API failures use structured log messages

## Error Handling

The project handles:
- invalid order inputs
- missing or invalid Binance credentials
- Binance API exceptions
- network failures
- unexpected exceptions

The web UI displays user-friendly messages while the logs keep the detailed diagnostic information.

## Assumptions

- The project uses Binance Futures Testnet only.
- Credentials are stored securely in `.env`.
- The web interface is for demo and development purposes.
- A production deployment would use a proper WSGI server instead of Flask’s built-in server.
