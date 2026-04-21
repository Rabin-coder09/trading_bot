import os
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv

from bot.client import BinanceClient
from bot.orders import place_order, get_account_info
from bot.validators import validate_all
from bot.logging_config import setup_logger

load_dotenv()
logger = setup_logger("cli")
app = typer.Typer(help="Binance Futures Testnet Trading Bot")
console = Console()


def get_client() -> BinanceClient:
    """Initialize Binance client from environment variables."""
    api_key = os.getenv("API_KEY")
    secret_key = os.getenv("SECRET_KEY")
    base_url = os.getenv("BASE_URL", "https://testnet.binancefuture.com")

    if not api_key or not secret_key:
        console.print("[red]ERROR: API_KEY or SECRET_KEY not found in .env file![/red]")
        raise typer.Exit(1)

    return BinanceClient(api_key, secret_key, base_url)


def print_order_summary(symbol, side, order_type, quantity, price=None, stop_price=None):
    """Print order request summary."""
    table = Table(title="Order Request Summary", style="cyan")
    table.add_column("Field", style="bold white")
    table.add_column("Value", style="yellow")

    table.add_row("Symbol", symbol)
    table.add_row("Side", f"[green]{side}[/green]" if side == "BUY" else f"[red]{side}[/red]")
    table.add_row("Order Type", order_type)
    table.add_row("Quantity", str(quantity))
    if price:
        table.add_row("Price", str(price))
    if stop_price:
        table.add_row("Stop Price", str(stop_price))

    console.print(table)


def print_order_response(data: dict):
    """Print order response details."""
    table = Table(title="Order Response", style="green")
    table.add_column("Field", style="bold white")
    table.add_column("Value", style="yellow")

    table.add_row("Order ID", str(data.get("orderId", "N/A")))
    table.add_row("Symbol", str(data.get("symbol", "N/A")))
    table.add_row("Status", str(data.get("status", "N/A")))
    table.add_row("Side", str(data.get("side", "N/A")))
    table.add_row("Type", str(data.get("type", "N/A")))
    table.add_row("Quantity", str(data.get("origQty", "N/A")))
    table.add_row("Executed Qty", str(data.get("executedQty", "N/A")))
    table.add_row("Avg Price", str(data.get("avgPrice", "N/A")))
    table.add_row("Time in Force", str(data.get("timeInForce", "N/A")))

    console.print(table)


@app.command()
def order(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading pair e.g. BTCUSDT"),
    side: str = typer.Option(..., "--side", help="BUY or SELL"),
    order_type: str = typer.Option(..., "--type", "-t", help="MARKET, LIMIT, or STOP_MARKET"),
    quantity: float = typer.Option(..., "--qty", "-q", help="Order quantity"),
    price: float = typer.Option(None, "--price", "-p", help="Price for LIMIT orders"),
    stop_price: float = typer.Option(None, "--stop-price", help="Stop price for STOP_MARKET orders"),
):
    """Place a futures order on Binance Testnet."""

    console.print(Panel("[bold cyan]Binance Futures Testnet Trading Bot[/bold cyan]", expand=False))

    # Validate inputs
    try:
        validated = validate_all(symbol, side, order_type, quantity, price)
    except ValueError as e:
        console.print(f"[red]Validation Error: {e}[/red]")
        logger.error(f"Validation Error: {e}")
        raise typer.Exit(1)

    # Print request summary
    print_order_summary(
        validated["symbol"],
        validated["side"],
        validated["order_type"],
        validated["quantity"],
        validated["price"],
        stop_price
    )

    # Confirm before placing
    confirm = typer.confirm("Confirm order placement?")
    if not confirm:
        console.print("[yellow]Order cancelled by user.[/yellow]")
        raise typer.Exit(0)

    # Place order
    client = get_client()
    result = place_order(
        client=client,
        symbol=validated["symbol"],
        side=validated["side"],
        order_type=validated["order_type"],
        quantity=validated["quantity"],
        price=validated["price"],
        stop_price=stop_price
    )

    if result["success"]:
        print_order_response(result["data"])
        console.print(Panel("[bold green]✅ Order placed successfully![/bold green]", expand=False))
        logger.info("Order completed successfully")
    else:
        error = result["error"]
        console.print(f"[red]❌ Order Failed: {error.get('msg', 'Unknown error')}[/red]")
        logger.error(f"Order failed: {error}")
        raise typer.Exit(1)


@app.command()
def balance():
    """Check your futures account balance."""
    client = get_client()
    console.print(Panel("[bold cyan]Account Balance[/bold cyan]", expand=False))

    result = get_account_info(client)
    if result["success"]:
        assets = result["data"].get("assets", [])
        table = Table(title="Account Assets", style="cyan")
        table.add_column("Asset", style="bold white")
        table.add_column("Wallet Balance", style="yellow")
        table.add_column("Available Balance", style="green")

        for asset in assets:
            if float(asset.get("walletBalance", 0)) > 0:
                table.add_row(
                    asset.get("asset"),
                    asset.get("walletBalance"),
                    asset.get("availableBalance")
                )
        console.print(table)
    else:
        console.print(f"[red]Failed to fetch balance: {result['error']}[/red]")


if __name__ == "__main__":
    app()