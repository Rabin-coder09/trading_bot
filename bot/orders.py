from bot.client import BinanceClient
from bot.logging_config import setup_logger

logger = setup_logger("orders")


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

    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    if order_type == "STOP_MARKET":
        params["stopPrice"] = stop_price
        params["closePosition"] = "false"

    logger.info(f"Placing {order_type} {side} order | Symbol: {symbol} | Qty: {quantity}" +
                (f" | Price: {price}" if price else "") +
                (f" | StopPrice: {stop_price}" if stop_price else ""))

    # STOP_MARKET uses different endpoint
    if order_type == "STOP_MARKET":
        endpoint = "/fapi/v1/order"
        params["type"] = "STOP_MARKET"
    else:
        endpoint = "/fapi/v1/order"

    response = client.post(endpoint, params)

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