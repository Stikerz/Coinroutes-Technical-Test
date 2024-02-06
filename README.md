# Coinroutes Technical Test (Backend) & Live Coding Interview - Order Book Price Checker

The **CoinRoutes Order Book Price Checker** is a command-line program that fetches order books from CoinBase Pro, Gemini, and Kraken (optional) exchanges. It then prints out the prices to buy and sell a specified quantity of a product.

This is for the backend role at coinroutes. Note this also includes an extension of the assignment related to the follow up live coding interview

## Table of Contents


- [Assignment](#assignment)
- [Installation](#installation)
- [Usage](#usage)
- [Command-Line Options](#command-line-options)
- [Testing](#testing)
- [Project Structure](#project-structure)
- [Third-party Integrations](#third-party-integrations)



## Assignment

# Coinroutes Order book aggregator in Python

Before beginning, read about how an order book works [here](https://falconair.github.io/2015/01/05/financial-exchange.html) (you can ignore the Scala bits).

Since they use slightly non-standard terminology, here are some definitions of terms this description uses:

- **Bids**: the line of buyers as referenced in the article.
  - Array of records. Each record contains Quantity and price. Sorted by highest price first.
- **Offers**: The line of sellers as referenced in the article.
  - Array of records. Each record contains Quantity and price. Sorted by lowest price first.
- **Order Book**: This is an object that contains the bids and offers data arrays.

**Expected output:**

Write a Python program that runs from the terminal, that fetches the order books from CoinBase Pro and Gemini exchanges and prints out the price to buy 10 bitcoin and the price to sell 10 bitcoin.

In the context of the article above, we want to “take” liquidity which means picking people out of their place in line: bids side if selling or the offers side if buying.

**Bonus:** add console log parameters to adjust the quantity and add the Kraken exchange.

## Resources:

The exchanges all have JSON REST APIs for fetching order books.

1. **CoinBase Pro**:
   - Docs: [Coinbase Pro Docs](https://docs.pro.coinbase.com/#get-product-order-book)
   - Endpoint for BTC-USD: [Coinbase Pro Endpoint](https://docs.cloud.coinbase.com/exchange/docs/websocket-channels#level2-channel)

2. **Gemini Exchange**:
   - Docs: [Gemini Exchange Docs](https://docs.gemini.com/rest-api/#current-order-book)
   - Endpoint for BTC-USD: [Gemini Endpoint](https://api.gemini.com/v1/book/BTCUSD)

3. **Kraken Exchange** (Bonus):
   - Docs: [Kraken Exchange Docs](https://www.kraken.com/en-us/features/api#get-order-book)
   - Endpoint for BTC-USD: [Kraken Endpoint](https://api.kraken.com/0/public/Depth?pair=XBTUSD)

Fetch the order books using `requests` (or preferred library). [Requests Documentation](https://requests.readthedocs.io/en/master/)

## Tips:
- You will want to normalize the order books into a common format. You can use standard Python Lists for the bids and offers arrays and Python dictionaries for the price level objects within each bid/offer list.
- You may want to merge the 2-3 order books from each exchange into a single data structure in order to generate the output.
- Order books can be merged across exchanges as long as the resulting merged bids and asks data structures are sorted correctly
- Bids are typically sorted highest first IE the highest price a seller can sell at, and offers lowest
first IE the lowest price a buyer can buy at.

## Coinroute Livecoding extenstion:
- Related to a limit order book , Given the code you wrote, extend the application to track the quantity of product amount purchased from each exchange and record the last purchase price from each exchange & store it in a datastructure.

e.g
```python

# {'Exchange name': [product_amount], [last_price_bought_at_exchange]}
# {'KRAKEN': [Decimal('12.368'), Decimal('42549.20000')], 'GEMINI': [Decimal('0.47058617'), Decimal('42550.5')], 'COINBASE': [Decimal('3.16141383'), Decimal('42549.63')]}


```


## Installation

This project makes use of [Poetry](https://python-poetry.org/).
We recommend using [pyenv](https://github.com/pyenv/pyenv) for managing multiple python versions.

```shell
pyenv install 3.12
pyenv local 3.12 # Activated python 3.12 for this project
poetry env use python3.12 # Or /full/path/to/python if you have to
poetry shell # Enable your virtual environment
poetry install # Install dependencies
```

## Usage

Run the program using the following command:

```bash
 python -m  orderbooks.main --add-kraken-exchange --quantity 10 --product BTCUSD
```

## Command-Line Options

- `--add-kraken-exchange`: Include this flag to fetch order books from the Kraken Exchange as well.
- `--quantity`: The amount of the product for which to get the buy and sell prices (default is 10).
- `--product`: The product that you want to buy/sell on the stock exchanges (default is "BTCUSD").


## Testing

Testing is facilitated via pytest and can simply be run as follows:

```shell
pytest
# or
pytest path/to/your/test.py

```
## Project Structure

Here is the project structure. 

```
├── README.md
├── orderbooks
│   ├── __init__.py
│   ├── integrations
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   └── exchanges.py
│   ├── main.py
│   ├── tests
│   │   ├── __init__.py
│   │   ├── helpers.py
│   │   ├── integrations
│   │   │   ├── __init__.py
│   │   │   └── test_exchanges.py
│   │   ├── test_main.py
│   │   └── test_utils.py
│   └── utils.py
└── pyproject.toml

```

Here is a brief description of the purpose of each file and directory in the project structure:

### `README.md`

Project documentation.

### `orderbooks/`

Contains your project's Python modules and packages.

- **`__init__.py`**: Initialization file for the module.
- **`integrations`**: Module folder containing the third party integration functionality.
- **`main.py`**: Main module file containing the core functionality.
- **`tests`**: Module folder containing the project test cases.
- **`utils.py`**: Module file containing general utility functions used in the application.

### `orderbooks/integrations/`

Holds projects third party integrations

- **`__init__.py`**: Initialization file for the integrations.
- **`constants.py`**: Module file used to store constant values, variables, or configurations
- **`exchanges.py`**: Module file containing the third party integration functionality.

### `orderbooks/tests/`

Holds project test cases.

- **`__init__.py`**: Initialization file for the tests.
- **`helpers.py`**: Helpers for test cases.
- **`test_main.py`**: Test cases for the `main.py` module.
- **`test_utils.py`**: Test cases for the `utils.py` module.
- **`integrations/test_exchanges.py`**: Test cases for the `exchanges.py` module.


### `pyproject.toml`

Configures project dependencies and settings (for Poetry).


## Third-party integrations

The project integrates with the following exchanges for fetching order books.

1. **CoinBase Pro:**
   - Docs: [CoinBase Pro API Documentation](https://docs.cloud.coinbase.com/exchange/reference)
   - Endpoint for BTC-USD: [CoinBase Pro BTC-USD Order Book](https://api.exchange.coinbase.com/products/BTC-USD/book?level=3)

2. **Gemini Exchange:**
   - Docs: [Gemini Exchange API Documentation](https://docs.gemini.com/rest-api/#current-order-book)
   - Endpoint for BTC-USD: [Gemini BTC-USD Order Book](https://api.gemini.com/v1/book/BTCUSD)

3. **Kraken Exchange:**
   - Docs: [Kraken Exchange API Documentation](https://docs.kraken.com/rest/)
   - Endpoint for BTC-USD: [Kraken BTC-USD Order Book](https://api.kraken.com/0/public/Depth?pair=XBTUSD)



## TODO 

Fix tests after making changes to the orderbook datastructure for the live coding extension changes made.