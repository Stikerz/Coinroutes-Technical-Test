from decimal import Decimal

import pytest
from click.testing import CliRunner

from orderbooks.main import get_prices


class TestMain:
    @pytest.mark.parametrize(
        [
            "buy_and_sell_price",
            "add_kraken_exchange",
            "quantity",
            "product",
            "expected_buy_output",
            "expected_sell_output",
        ],
        [
            (
                (200, 0, 210, 0),
                ["--add-kraken-exchange"],
                "10.0",
                "BTCUSD",
                "Buy price for {} {} is",
                "Sell price for {} {} is",
            ),
            (
                (300.0, Decimal(5.0), 310.0, Decimal(3.0)),
                ["--add-kraken-exchange"],
                "100.0",
                "BTCUSD",
                "Buy order of {} {} partially filled",
                "Sell order of {} {} partially filled",
            ),
            (
                (300.0, Decimal(5.0), 310.0, 0),
                [],
                "100.0",
                "BTCUSD",
                "Buy order of {} {} partially filled",
                "Sell price for {} {} is",
            ),
            (
                (300.0, 0, 310.0, Decimal(3.0)),
                [],
                "100.0",
                "BTCUSD",
                "Buy price for {} {} is",
                "Sell order of {} {} partially filled",
            ),
        ],
    )
    def test_get_prices_buy_sell(
        self,
        mocker,
        buy_and_sell_price,
        add_kraken_exchange,
        quantity,
        product,
        expected_buy_output,
        expected_sell_output,
    ):
        runner = CliRunner()

        mock_get_prices = mocker.patch(
            "orderbooks.main.get_buy_and_sell_price", return_value=buy_and_sell_price
        )

        result = runner.invoke(
            get_prices,
            ["--quantity", quantity, "--product", product] + add_kraken_exchange,
        )

        assert expected_buy_output.format(quantity, product) in result.output
        assert expected_sell_output.format(quantity, product) in result.output
        mock_get_prices.assert_called_with(
            quantity=float(quantity),
            product=product,
            kraken_exchange=bool(add_kraken_exchange),
        )

    def test_get_prices_unsupported_product(self, mocker):
        runner = CliRunner()
        mock_get_prices = mocker.patch("orderbooks.main.get_buy_and_sell_price")

        result = runner.invoke(
            get_prices,
            ["--quantity", "10", "--product", "XYZ", "--add-kraken-exchange"],
        )
        assert "Unsupported product XYZ submitted" in result.output
        mock_get_prices.assert_not_called()
