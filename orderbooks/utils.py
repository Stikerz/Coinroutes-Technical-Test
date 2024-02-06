from decimal import Decimal

from orderbooks.integrations.constants import (
    COINROUTES_SYMBOL_TO_COINBASE_SYMBOL, COINROUTES_SYMBOL_TO_GEMINI_SYMBOL,
    COINROUTES_SYMBOL_TO_KRAKEN_SYMBOL,
    KRAKEN_REQUEST_SYMBOL_TO_RESULTS_SYMBOL, KRAKEN, COINBASE, GEMINI)
from orderbooks.integrations.exchanges import (CoinBaseClient, GeminiClient,
                                               KrakenClient)

TWOPLACES = Decimal(10) ** -2


def transform_exchange_data(data, exchange, dict_datatype=False):

    if dict_datatype:
        bids = [(exchange, Decimal(record.get("price")), Decimal(record.get("amount"))) for record in data["bids"]]
        offers = [(exchange, Decimal(record.get("price")), Decimal(record.get("amount"))) for record in data["asks"]]

        return bids, offers

    bids = [(exchange, Decimal(record[0]), Decimal(record[1])) for record in data["bids"]]
    offers = [(exchange, Decimal(record[0]), Decimal(record[1])) for record in data["asks"]]
    return bids, offers


def get_exchange_data(product: str, kraken=False):
    bid_order_book = []
    offer_order_book = []
    gemini_c = GeminiClient()
    coinbase_c = CoinBaseClient()
    gemini_product_symbol = COINROUTES_SYMBOL_TO_GEMINI_SYMBOL.get(product)
    coinbase_product_symbol = COINROUTES_SYMBOL_TO_COINBASE_SYMBOL.get(product)

    gemini_order_book_request = gemini_c.get_order_book(gemini_product_symbol)
    gemini_bids, gemini_offers = transform_exchange_data(gemini_order_book_request, GEMINI, dict_datatype=True)
    bid_order_book.extend(gemini_bids)
    offer_order_book.extend(gemini_offers)

    coinbase_order_book_request = coinbase_c.get_order_book(
        coinbase_product_symbol, params={"level": "3"}
    )
    coinbase_bids, coinbase_offers = transform_exchange_data(
        coinbase_order_book_request, COINBASE
    )
    bid_order_book.extend(coinbase_bids)
    offer_order_book.extend(coinbase_offers)

    if kraken:
        kraken_c = KrakenClient()
        kraken_product_symbol = COINROUTES_SYMBOL_TO_KRAKEN_SYMBOL.get(product)
        kraken_order_book_request = kraken_c.get_order_book(kraken_product_symbol)
        results_symbol = KRAKEN_REQUEST_SYMBOL_TO_RESULTS_SYMBOL.get(
            kraken_product_symbol
        )
        kraken_bids, kraken_offers = transform_exchange_data(
            kraken_order_book_request.get("result").get(results_symbol), KRAKEN
        )
        bid_order_book.extend(kraken_bids)
        offer_order_book.extend(kraken_offers)

    return bid_order_book, offer_order_book


def execute_market_order(product_amount_target, order_book, bid=False):
    product_amount_decimal = Decimal(product_amount_target)
    order_book.sort(key=lambda x: x[1], reverse=bid)

    cumulative_amount = 0
    total_cost = 0
    transactions = {KRAKEN: [0, 0], GEMINI: [0, 0], COINBASE: [0, 0]}

    for exchange, price, amount in order_book:
        previous_cumulative_amount = cumulative_amount
        cumulative_amount += amount

        if cumulative_amount > product_amount_decimal:
            partial_product_amount = product_amount_decimal - previous_cumulative_amount
            partial_filled_cost = partial_product_amount * price
            total_cost += partial_filled_cost
            transactions[exchange][0] += partial_product_amount
            transactions[exchange][1] = price
            print(transactions)
            return total_cost.quantize(TWOPLACES), 0
        elif cumulative_amount == product_amount_decimal:
            total_cost += price * amount
            transactions[exchange][0] += amount
            transactions[exchange][1] = price
            print(transactions)
            return total_cost.quantize(TWOPLACES), 0

        total_cost += price * amount
        transactions[exchange][0] += amount
        transactions[exchange][1] = price

    print(transactions)
    return total_cost.quantize(TWOPLACES), product_amount_decimal - cumulative_amount


def get_buy_and_sell_price(quantity, product, kraken_exchange):
    bid_order_book, offer_order_book = get_exchange_data(
        product=product, kraken=kraken_exchange
    )
    buy_cost, remaining_buy_amount = execute_market_order(
        quantity, offer_order_book, bid=False
    )
    sell_cost, remaining_sell_amount = execute_market_order(
        quantity, bid_order_book, bid=True
    )
    return (
        buy_cost,
        remaining_buy_amount,
        sell_cost,
        remaining_sell_amount,
    )
