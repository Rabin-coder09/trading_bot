from bot.logging_config import setup_logger

logger = setup_logger("validators")

VALID_SIDES = ["BUY", "SELL"]
VALID_ORDER_TYPES = ["MARKET", "LIMIT"]


def validate_symbol(symbol: str) -> str:
    if not symbol:
        raise ValueError("Symbol cannot be empty")
    symbol = symbol.upper().strip()
    if len(symbol) < 5:
        raise ValueError(f"Invalid symbol: {symbol}. Example: BTCUSDT")
    logger.debug(f"Symbol validated: {symbol}")
    return symbol


def validate_side(side: str) -> str:
    side = side.upper().strip()
    if side not in VALID_SIDES:
        raise ValueError(f"Invalid side: '{side}'. Must be one of: {VALID_SIDES}")
    logger.debug(f"Side validated: {side}")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper().strip()
    if order_type not in VALID_ORDER_TYPES:
        raise ValueError(f"Invalid order type: '{order_type}'. Must be one of: {VALID_ORDER_TYPES}")
    logger.debug(f"Order type validated: {order_type}")
    return order_type


def validate_quantity(quantity: float) -> float:
    if quantity <= 0:
        raise ValueError(f"Quantity must be greater than 0. Got: {quantity}")
    logger.debug(f"Quantity validated: {quantity}")
    return quantity


def validate_price(price: float, order_type: str) -> float:
    if order_type == "LIMIT":
        if price is None or price <= 0:
            raise ValueError(f"Price must be greater than 0 for LIMIT orders. Got: {price}")
        logger.debug(f"Price validated: {price}")
    return price


def validate_all(symbol, side, order_type, quantity, price=None):
    return {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "order_type": validate_order_type(order_type),
        "quantity": validate_quantity(quantity),
        "price": validate_price(price, order_type.upper()) if price else None
    }