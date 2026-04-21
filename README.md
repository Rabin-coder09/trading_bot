# Binance Futures Testnet Trading Bot

A Python CLI trading bot for placing orders on Binance Futures Testnet (USDT-M).

---

## Features

- Place MARKET, LIMIT, and STOP_MARKET orders
- Support for BUY and SELL sides
- Input validation with helpful error messages
- Structured logging to file and console
- Clean CLI interface with rich output tables
- Account balance checker

---

## Project Structure

    trading_bot/
      bot/
        __init__.py          # Package init
        client.py            # Binance API client wrapper
        orders.py            # Order placement logic
        validators.py        # Input validation
        logging_config.py    # Logging setup
      cli.py                 # CLI entry point
      .env                   # API credentials (not committed)
      requirements.txt       # Dependencies
      README.md              # This file

---

## Setup

### 1. Clone the repository

    git clone https://github.com/Rabin-coder09/trading_bot.git
    cd trading_bot

### 2. Create and activate virtual environment

    conda create -n trading_bot python=3.11 -y
    conda activate trading_bot

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Configure API credentials

Create a .env file in the root directory with the following content:

    API_KEY=your_api_key_here
    SECRET_KEY=your_secret_key_here
    BASE_URL=https://testnet.binancefuture.com

Get your API credentials from Binance Futures Testnet:
https://testnet.binancefuture.com

---

## How to Run

### Check account balance

    python cli.py balance

### Place a MARKET order

    # BUY
    python cli.py order --symbol BTCUSDT --side BUY --type MARKET --qty 0.001

    # SELL
    python cli.py order --symbol BTCUSDT --side SELL --type MARKET --qty 0.001

### Place a LIMIT order

    # BUY
    python cli.py order --symbol BTCUSDT --side BUY --type LIMIT --qty 0.001 --price 75000

    # SELL
    python cli.py order --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 80000

### Place a STOP_MARKET order (Bonus)

    # SELL with stop price
    python cli.py order --symbol BTCUSDT --side SELL --type STOP_MARKET --qty 0.001 --stop-price 74000

### Get help

    python cli.py --help
    python cli.py order --help

---

## Example Output

    Binance Futures Testnet Trading Bot

    Order Request Summary
    ---------------------
    Symbol      : BTCUSDT
    Side        : BUY
    Order Type  : MARKET
    Quantity    : 0.001

    Confirm order placement? [y/N]: y

    Order Response
    --------------
    Order ID     : 123456789
    Symbol       : BTCUSDT
    Status       : FILLED
    Side         : BUY
    Type         : MARKET
    Quantity     : 0.001
    Executed Qty : 0.001
    Avg Price    : 76190.5

    Order placed successfully!

---

## Logging

All activity is logged to logs/trading_bot.log including:
- API requests and responses
- Order success and failure details
- Validation errors
- Network errors

---

## Assumptions

- Uses Binance Futures Testnet (USDT-M) only
- Minimum order quantity for BTCUSDT is 0.001
- LIMIT orders use GTC (Good Till Cancelled) time in force
- API credentials are stored in .env file
- Python 3.11 or higher is required

---

## Dependencies

- requests       HTTP client for API calls
- typer          CLI framework
- rich           Beautiful terminal output
- python-dotenv  Environment variable management