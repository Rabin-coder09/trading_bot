# Binance Futures Testnet Trading Bot

A Python CLI trading bot for placing orders on Binance Futures Testnet (USDT-M) using the Binance Demo API.

## Features
- Place MARKET and LIMIT orders
- Support for BUY and SELL sides
- TWAP bonus order (splits large orders into timed slices)
- Input validation with helpful error messages
- Structured logging to file and console
- Clean CLI interface with rich output tables
- Account balance checker

## Project Structure

```
trading_bot/
  bot/
    __init__.py          # Package init
    client.py            # Binance API client wrapper
    orders.py            # Order placement logic
    validators.py        # Input validation
    logging_config.py    # Logging setup
  logs/
    trading_bot.log      # Auto-generated log file
  cli.py                 # CLI entry point
  .env                   # API credentials (not committed)
  .gitignore
  requirements.txt
  README.md
```

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Rabin-coder09/trading_bot.git
cd trading_bot
```

### 2. Create and activate environment
```bash
# Using conda (recommended)
conda create -n trading_bot python=3.11 -y
conda activate trading_bot

# OR using venv
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API credentials
Create a `.env` file in the root directory:
```
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
BASE_URL=https://testnet.binancefuture.com
```

> Get free API credentials from Binance Demo Trading (demo.binance.com) — no real money needed.

---

## How to Run

### Check account balance
```bash
python cli.py balance
```

### Place a MARKET order
```bash
# BUY
python cli.py order --symbol BTCUSDT --side BUY --type MARKET --qty 0.001

# SELL
python cli.py order --symbol BTCUSDT --side SELL --type MARKET --qty 0.001
```

### Place a LIMIT order
```bash
# BUY
python cli.py order --symbol BTCUSDT --side BUY --type LIMIT --qty 0.001 --price 75000

# SELL
python cli.py order --symbol BTCUSDT --side SELL --type LIMIT --qty 0.001 --price 80000
```

### TWAP order (Bonus)
Splits a large order into equal slices placed at timed intervals:
```bash
python cli.py twap --symbol BTCUSDT --side BUY --qty 0.003 --slices 3 --interval 5
```

### Get help
```bash
python cli.py --help
python cli.py order --help
python cli.py twap --help
```

---

## Example Output

```
╭─────────────────────────────────────╮
│ Binance Futures Testnet Trading Bot │
╰─────────────────────────────────────╯

     Order Request Summary
┌─────────────┬─────────────────────────┐
│ Field       │ Value                   │
├─────────────┼─────────────────────────┤
│ Symbol      │ BTCUSDT                 │
│ Side        │ BUY                     │
│ Order Type  │ MARKET                  │
│ Quantity    │ 0.001                   │
└─────────────┴─────────────────────────┘

Confirm order placement? [y/N]: y

          Order Response
┌──────────────┬──────────────────────┐
│ Field        │ Value                │
├──────────────┼──────────────────────┤
│ Order ID     │ 13058398167          │
│ Symbol       │ BTCUSDT              │
│ Status       │ NEW                  │
│ Side         │ BUY                  │
│ Type         │ MARKET               │
│ Quantity     │ 0.0010               │
│ Executed Qty │ 0.0000               │
│ Avg Price    │ 0.00                 │
└──────────────┴──────────────────────┘

╭───────────────────────────────╮
│ ✅ Order placed successfully! │
╰───────────────────────────────╯
```

---

## Logging
All activity is logged to `logs/trading_bot.log`:
- API requests and responses
- Order success/failure details
- Validation errors
- Network errors

---

## Assumptions
- Uses Binance Demo Trading API (demo.binance.com)
- STOP_MARKET is not supported on the Demo account — TWAP is implemented as the bonus order type
- Minimum order quantity for BTCUSDT is 0.001
- LIMIT orders use GTC (Good Till Cancelled) time in force
- API credentials stored in `.env` file (never committed to GitHub)
- Python 3.11+ required

---

## Dependencies
- `requests` — HTTP client for API calls
- `typer` — CLI framework
- `rich` — Beautiful terminal output
- `python-dotenv` — Environment variable management