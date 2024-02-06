import pytest

from orderbooks.tests.helpers import (successful_coinbase_response,
                                      successful_gemini_response,
                                      successful_kraken_response)
from orderbooks.utils import (execute_market_order, get_exchange_data,
                              transform_exchange_data)

from decimal import Decimal


class TestUtils:
    @pytest.mark.parametrize(
        [
            "bid",
            "product_amount",
            "expected_total_cost",
            "order_book",
            "expected_remaining_amount",
        ],
        [
            (
                False,
                4,
                "65090.54",
                [
                    (Decimal("39163.70000"), Decimal("1.539")),
                    (Decimal("39166.60000"), Decimal("0.020")),
                    (Decimal("39167.70000"), Decimal("0.103"))
                ],
                "2.338",
            ),
            (
                False,
                1.5,
                "58745.55",
                [
                    (Decimal("39163.70000"), Decimal("1.539")),
                    (Decimal("39166.60000"), Decimal("0.020")),
                    (Decimal("39167.70000"), Decimal("0.103"))
                ],
                "0",
            ),
            (
                False,
                1.6,
                "62662.14",
                [
                    (Decimal("39163.70000"), Decimal("1.539")),
                    (Decimal("39166.60000"), Decimal("0.020")),
                    (Decimal("39167.70000"), Decimal("0.103"))
                ],
                "0",
            ),
            (
                False,
                1.539,
                "60272.93",
                [
                    (Decimal("39163.70000"), Decimal("1.539")),
                    (Decimal("39166.60000"), Decimal("0.020")),
                    (Decimal("39167.70000"), Decimal("0.103"))
                ],
                "0",
            ),
            (
                True,
                15,
                "403970.29",
                [
                    (Decimal("39163.60000"), Decimal("8.187")),
                    (Decimal("39162.80000"), Decimal("0.768")),
                    (Decimal("39162.40000"), Decimal("1.360"))
                ],
                "4.685",
            ),
            (
                True,
                6,
                "234981.60",
                [
                    (Decimal("39163.60000"), Decimal("8.187")),
                    (Decimal("39162.80000"), Decimal("0.768")),
                    (Decimal("39162.40000"), Decimal("1.360"))
                ],
                "0",
            ),
            (
                True,
                9.2,
                "360304.21",
                [
                    (Decimal("39163.60000"), Decimal("8.187")),
                    (Decimal("39162.80000"), Decimal("0.768")),
                    (Decimal("39162.40000"), Decimal("1.360"))
                ],
                "0",
            ),
            (
                    True,
                    8.187,
                    "320632.39",
                    [
                        (Decimal("39163.60000"), Decimal("8.187")),
                        (Decimal("39162.80000"), Decimal("0.768")),
                        (Decimal("39162.40000"), Decimal("1.360"))
                    ],
                    "0",
            ),
        ],
    )
    def test_execute_market_order(
        self,
        bid,
        product_amount,
        expected_total_cost,
        order_book,
        expected_remaining_amount,
    ):
        cost, remaining_amount = execute_market_order(
            product_amount_target=product_amount,
            order_book=order_book,
            bid=bid,
        )
        assert str(cost) == expected_total_cost
        assert str(remaining_amount) == expected_remaining_amount

    @pytest.mark.parametrize(
        [
            "kraken_enabled",
            "kraken_order_book",
            "gemini_order_book",
            "coinbase_order_book",
            "product",
            "expected_bids",
            "expected_offers",
        ],
        [
            (
                True,
                successful_kraken_response(),
                successful_gemini_response(),
                successful_coinbase_response(),
                "BTCUSD",
                6,
                6,
            ),
            (
                False,
                None,
                successful_gemini_response(),
                successful_coinbase_response(),
                "BTCUSD",
                4,
                4,
            ),
        ],
    )
    def test_get_exchange_data(
        self,
        kraken_enabled,
        product,
        kraken_order_book,
        gemini_order_book,
        coinbase_order_book,
        mocker,
        expected_bids,
        expected_offers,
    ):
        mock_kraken_client = mocker.patch(
            "orderbooks.integrations.exchanges.KrakenClient.get_order_book",
            return_value=kraken_order_book,
        )

        mock_gemini_client = mocker.patch(
            "orderbooks.integrations.exchanges.GeminiClient.get_order_book",
            return_value=gemini_order_book,
        )
        mock_coinbase_client = mocker.patch(
            "orderbooks.integrations.exchanges.CoinBaseClient.get_order_book",
            return_value=coinbase_order_book,
        )

        bid_order_book, offer_order_book = get_exchange_data(
            product=product, kraken=kraken_enabled
        )
        mock_coinbase_client.assert_called_with("BTC-USD", params={"level": "3"})
        mock_gemini_client.assert_called_with("BTCUSD")
        if kraken_enabled:
            mock_kraken_client.assert_called_with("XBTUSD")
        else:
            mock_kraken_client.assert_not_called()

        assert len(bid_order_book) == expected_bids
        assert len(offer_order_book) == expected_offers

    def test_transform_exchange_data(self):
        test_data = {
            "bids": [[100, 1, "_"], [99, 2, "_"]],
            "asks": [[101, 3, "_"], [102, 4, "_"]],
        }

        bids, offers = transform_exchange_data(test_data)

        assert bids == [(100, 1), (99, 2)]
        assert offers == [(101, 3), (102,4)]

