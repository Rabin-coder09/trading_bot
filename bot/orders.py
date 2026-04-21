from bot.client import BinanceClient
from bot.logging_config import setup_logger

logger = setup_logger("orders")

# Order types not supported on Binance Demo account
DEMO_UNSUPPORTED_TYPES = ["STOP_MARKET"]


def place_order(
    client: BinanceClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float = None,
    stop_price: float = None
) -> dict:
    """Place an order on Binance Futures Testnet."""

    # Warn user if order type has known demo limitations
    if order_type in DEMO_UNSUPPORTED_TYPES:
        logger.warning(
            f"{order_type} is not supported on Binance Demo account. "
            f"Use TAKE_PROFIT_MARKET as an alternative."
        )
        return {
            "success": False,
            "error": {
                "code": -4120,
                "msg": (
                    f"{order_type} is not supported on Binance Demo account (demo.binance.com). "
                    f"If using real Futures Testnet (testnet.binancefuture.com), it will work. "
                    f"Try TAKE_PROFIT_MARKET instead."
                )
            }
        }

    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    if order_type == "TAKE_PROFIT_MARKET":
        params["stopPrice"] = stop_price
        params["closePosition"] = "false"

    logger.info(
        f"Placing {order_type} {side} order | Symbol: {symbol} | Qty: {quantity}" +
        (f" | Price: {price}" if price else "") +
        (f" | StopPrice: {stop_price}" if stop_price else "")
    )

    response = client.post("/fapi/v1/order", params)

    if response["status_code"] == 200:
        data = response["data"]
        logger.info(
            f"Order SUCCESS | OrderId: {data.get('orderId')} | "
            f"Status: {data.get('status')} | "
            f"ExecutedQty: {data.get('executedQty')} | "
            f"AvgPrice: {data.get('avgPrice', 'N/A')}"
        )
        return {"success": True, "data": data}
    else:
        error = response["data"]
        logger.error(f"Order FAILED | Code: {error.get('code')} | Msg: {error.get('msg')}")
        return {"success": False, "error": error}


def get_account_info(client: BinanceClient) -> dict:
    """Get account balance info."""
    response = client.get("/fapi/v2/account")
    if response["status_code"] == 200:
        return {"success": True, "data": response["data"]}
    else:
        return {"success": False, "error": response["data"]}