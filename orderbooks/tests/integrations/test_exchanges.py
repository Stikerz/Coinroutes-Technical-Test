from contextlib import nullcontext as does_not_raise
from http import HTTPStatus
from unittest.mock import Mock

import pytest
from requests.exceptions import (ConnectionError, HTTPError, RequestException,
                                 Timeout)

from orderbooks.integrations.exchanges import (CoinBaseClient, GeminiClient,
                                               KrakenClient)
from orderbooks.tests.helpers import (successful_coinbase_response,
                                      successful_gemini_response,
                                      successful_kraken_response)


class TestGeminiClient:
    @pytest.mark.parametrize(
        [
            "response",
            "expected_exception",
            "expected_response",
            "product",
            "status_code",
            "reason",
        ],
        [
            (
                {"json": {}, "status_code": HTTPStatus.BAD_REQUEST},
                pytest.raises(Exception),
                None,
                "HUUIUH",
                HTTPStatus.BAD_REQUEST,
                "bad request",
            ),
            (
                {
                    "json": successful_gemini_response(),
                    "status_code": HTTPStatus.OK,
                },
                does_not_raise(),
                successful_gemini_response(),
                "BTCUSD",
                HTTPStatus.OK,
                "",
            ),
        ],
    )
    def test_get_order_book(
        self,
        response,
        expected_exception,
        expected_response,
        product,
        mocker,
        status_code,
        reason,
    ):
        client = GeminiClient()
        mock = Mock()
        mock.status_code = status_code
        mock.json.return_value = response["json"]
        mock.reason = reason
        mocker.patch(
            "orderbooks.integrations.exchanges.requests.get", return_value=mock
        )
        with expected_exception:
            resp = client.get_order_book(product=product)
            assert resp == expected_response

    @pytest.mark.parametrize(
        [
            "exception",
            "expected_exception",
            "exception_message",
            "product",
        ],
        [
            (
                Timeout,
                pytest.raises(Exception),
                "Timeout Error: ",
                "HUUIUH",
            ),
            (
                ConnectionError,
                pytest.raises(Exception),
                "Connection Error: ",
                "HUUIUH",
            ),
            (
                HTTPError,
                pytest.raises(Exception),
                "Http Error: ",
                "HUUIUH",
            ),
            (
                RequestException,
                pytest.raises(Exception),
                "Error: ",
                "HUUIUH",
            ),
        ],
    )
    def test_request_exceptions(
        self, exception, expected_exception, exception_message, product, mocker
    ):
        client = GeminiClient()
        mocker.patch(
            "orderbooks.integrations.exchanges.requests.get", side_effect=exception
        )
        with expected_exception as err:
            client.get_order_book(product=product)

        assert err.value.args[0] == exception_message


class TestCoinBaseClient:
    @pytest.mark.parametrize(
        [
            "response",
            "expected_exception",
            "expected_response",
            "product",
            "status_code",
            "reason",
        ],
        [
            (
                {"json": {}, "status_code": HTTPStatus.BAD_REQUEST},
                pytest.raises(Exception),
                None,
                "HUUIUH",
                HTTPStatus.BAD_REQUEST,
                "bad request",
            ),
            (
                {
                    "json": successful_coinbase_response(),
                    "status_code": HTTPStatus.OK,
                },
                does_not_raise(),
                successful_coinbase_response(),
                "BTC-USD",
                HTTPStatus.OK,
                "",
            ),
        ],
    )
    def test_get_order_book(
        self,
        response,
        expected_exception,
        expected_response,
        product,
        mocker,
        status_code,
        reason,
    ):
        client = CoinBaseClient()
        mock = Mock()
        mock.status_code = status_code
        mock.json.return_value = response["json"]
        mocker.patch(
            "orderbooks.integrations.exchanges.requests.get", return_value=mock
        )
        with expected_exception:
            resp = client.get_order_book(product=product)
            assert resp == expected_response

    @pytest.mark.parametrize(
        [
            "exception",
            "expected_exception",
            "exception_message",
            "product",
        ],
        [
            (
                Timeout,
                pytest.raises(Exception),
                "Timeout Error: ",
                "HUUIUH",
            ),
            (
                ConnectionError,
                pytest.raises(Exception),
                "Connection Error: ",
                "HUUIUH",
            ),
            (
                HTTPError,
                pytest.raises(Exception),
                "Http Error: ",
                "HUUIUH",
            ),
            (
                RequestException,
                pytest.raises(Exception),
                "Error: ",
                "HUUIUH",
            ),
        ],
    )
    def test_request_exceptions(
        self, exception, expected_exception, exception_message, product, mocker
    ):
        client = CoinBaseClient()
        mocker.patch(
            "orderbooks.integrations.exchanges.requests.get", side_effect=exception
        )
        with expected_exception as err:
            client.get_order_book(product=product)

        assert err.value.args[0] == exception_message


class TestKrakenClient:
    @pytest.mark.parametrize(
        [
            "response",
            "expected_exception",
            "expected_response",
            "product",
            "status_code",
            "reason",
        ],
        [
            (
                {"json": {}, "status_code": HTTPStatus.BAD_REQUEST},
                pytest.raises(Exception),
                None,
                "HUUIUH",
                HTTPStatus.BAD_REQUEST,
                "bad request",
            ),
            (
                {
                    "json": successful_kraken_response(),
                    "status_code": HTTPStatus.OK,
                },
                does_not_raise(),
                successful_kraken_response(),
                "XBTUSD",
                HTTPStatus.OK,
                "",
            ),
        ],
    )
    def test_get_order_book(
        self,
        response,
        expected_exception,
        expected_response,
        product,
        mocker,
        status_code,
        reason,
    ):
        client = KrakenClient()
        mock = Mock()
        mock.status_code = status_code
        mock.json.return_value = response["json"]
        mocker.patch(
            "orderbooks.integrations.exchanges.requests.get", return_value=mock
        )
        with expected_exception:
            resp = client.get_order_book(product=product)
            assert resp == expected_response

    @pytest.mark.parametrize(
        [
            "exception",
            "expected_exception",
            "exception_message",
            "product",
        ],
        [
            (
                Timeout,
                pytest.raises(Exception),
                "Timeout Error: ",
                "HUUIUH",
            ),
            (
                ConnectionError,
                pytest.raises(Exception),
                "Connection Error: ",
                "HUUIUH",
            ),
            (
                HTTPError,
                pytest.raises(Exception),
                "Http Error: ",
                "HUUIUH",
            ),
            (
                RequestException,
                pytest.raises(Exception),
                "Error: ",
                "HUUIUH",
            ),
        ],
    )
    def test_request_exceptions(
        self, exception, expected_exception, exception_message, product, mocker
    ):
        client = KrakenClient()
        mocker.patch(
            "orderbooks.integrations.exchanges.requests.get", side_effect=exception
        )
        with expected_exception as err:
            client.get_order_book(product=product)

        assert err.value.args[0] == exception_message
