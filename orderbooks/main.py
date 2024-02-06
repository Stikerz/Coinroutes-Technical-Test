import sys
from decimal import Decimal

import click

from orderbooks.integrations.constants import COINROUTES_GET_PRICE_CHOICES
from orderbooks.utils import get_buy_and_sell_price


@click.command()
@click.option("--add-kraken-exchange", is_flag=True)
@click.option("--quantity", required=False, type=float, default=16)
@click.option("--product", required=False, type=str, default="BTCUSD")
def get_prices(add_kraken_exchange, quantity, product):
    """Program that fetches the order books from CoinBase Pro, Gemini and Kraken(optional)
    and prints out the price to buy and sell a specified quantity of a product.

    :param add_kraken_exchange: Fetch order books from the Kraken Exchange as well.
    :param quantity: The amount of the product for which to get the buy and sell prices.
    :param product: The product that you want to buy/sell on the stock exchanges e.g. BTCUSD.
    """

    if product not in COINROUTES_GET_PRICE_CHOICES:
        click.echo(
            f"Unsupported product {product} submitted, please select a supported product."
        )
        sys.exit()

    (
        buy_price,
        remaining_buy_amount,
        sell_price,
        remaining_sell_amount,
    ) = get_buy_and_sell_price(
        quantity=quantity, product=product, kraken_exchange=add_kraken_exchange
    )

    if remaining_buy_amount:
        click.echo(
            f"Buy order of {quantity} {product} partially filled. Remaining: {remaining_buy_amount} {product}."
            f" Price of {Decimal(quantity) - remaining_buy_amount} {product} is {buy_price}."
        )
    else:
        click.echo(f"Buy price for {quantity} {product} is {buy_price}.")

    if remaining_sell_amount:
        click.echo(
            f"Sell order of {quantity} {product} partially filled. Remaining: {remaining_sell_amount} {product}."
            f" Price of {Decimal(quantity) - remaining_sell_amount} {product} is {sell_price}."
        )
    else:
        click.echo(f"Sell price for {quantity} {product} is {sell_price}.")


if __name__ == "__main__":
    get_prices()
