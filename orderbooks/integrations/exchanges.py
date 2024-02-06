from http import HTTPStatus
from typing import Dict
from urllib.parse import urljoin

import requests
from requests.models import Response as RequestResponse


def validate_response(
    response: RequestResponse, expected_status: int, method_name: str, class_name: str
):
    if response.status_code == expected_status:
        return

    raise Exception(
        f"{class_name} {method_name} error, error code: {response.status_code} error message: {response.reason}",
        response.status_code,
    )


class CoinBaseClient:
    """
    Client to make requests to CoinBase Pro API.
    see : https://docs.cloud.coinbase.com/exchange/reference
    """

    COINBASE_BASE_URL = "https://api.exchange.coinbase.com"
    ENDPOINT_GET_ORDER_BOOK = "products/{}/book"

    def get_order_book(self, product: str, params: Dict[str, str] = None):
        """Get order book via Coinbase exchange API which
        provides a list of open orders for a product."""
        if params is None:
            params = dict()

        try:
            response = requests.get(
                urljoin(
                    self.COINBASE_BASE_URL, self.ENDPOINT_GET_ORDER_BOOK.format(product)
                ),
                params=params,
            )
        except requests.exceptions.ConnectionError as errc:
            raise Exception(f"Connection Error: {errc}")
        except requests.exceptions.Timeout as errt:
            raise Exception(f"Timeout Error: {errt}")
        except requests.exceptions.HTTPError as errh:
            raise Exception(f"Http Error: {errh}")
        except requests.exceptions.RequestException as err:
            raise Exception(f"Error: {err}")

        validate_response(
            response=response,
            expected_status=HTTPStatus.OK,
            method_name=CoinBaseClient.get_order_book.__name__,
            class_name=CoinBaseClient.__name__,
        )
        return response.json()


class GeminiClient:
    """
    Client to make requests to Gemini Exchange API.
    see : https://docs.gemini.com/rest-api/
    """

    GEMINI_BASE_URL = "https://api.gemini.com"
    ENDPOINT_GET_ORDER_BOOK = "v1/book/{}"

    def get_order_book(self, product: str, params: Dict[str, str] = None):
        """Get order book via Gemini exchange API which
        provides a list of the current orders for a product."""
        if params is None:
            params = dict()

        try:
            response = requests.get(
                urljoin(
                    self.GEMINI_BASE_URL, self.ENDPOINT_GET_ORDER_BOOK.format(product)
                ),
                params=params,
            )
        except requests.exceptions.ConnectionError as errc:
            raise Exception(f"Connection Error: {errc}")
        except requests.exceptions.Timeout as errt:
            raise Exception(f"Timeout Error: {errt}")
        except requests.exceptions.HTTPError as errh:
            raise Exception(f"Http Error: {errh}")
        except requests.exceptions.RequestException as err:
            raise Exception(f"Error: {err}")

        validate_response(
            response=response,
            expected_status=HTTPStatus.OK,
            method_name=GeminiClient.get_order_book.__name__,
            class_name=GeminiClient.__name__,
        )
        return response.json()


class KrakenClient:
    """
    Client to make requests to Kraken Exchange API.
    see : https://docs.kraken.com/rest/
    """

    KRAKEN_BASE_URL = "https://api.kraken.com"
    ENDPOINT_GET_ORDER_BOOK = "0/public/Depth"

    def get_order_book(self, product: str, params: Dict[str, str] = None):
        """Get order book via Kraken exchange API which
        provides a list of the current orders for a product."""
        if params is None:
            params = dict()
        params["pair"] = product

        try:
            response = requests.get(
                urljoin(self.KRAKEN_BASE_URL, self.ENDPOINT_GET_ORDER_BOOK),
                params=params,
            )
        except requests.exceptions.ConnectionError as errc:
            raise Exception(f"Connection Error: {errc}")
        except requests.exceptions.Timeout as errt:
            raise Exception(f"Timeout Error: {errt}")
        except requests.exceptions.HTTPError as errh:
            raise Exception(f"Http Error: {errh}")
        except requests.exceptions.RequestException as err:
            raise Exception(f"Error: {err}")

        validate_response(
            response=response,
            expected_status=HTTPStatus.OK,
            method_name=KrakenClient.get_order_book.__name__,
            class_name=KrakenClient.__name__,
        )
        return response.json()
