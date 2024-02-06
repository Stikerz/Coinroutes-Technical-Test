def successful_kraken_response():
    return {
        "error": [],
        "result": {
            "XXBTZUSD": {
                "asks": [
                    ["39163.70000", "1.539", 1706044374],
                    ["39166.60000", "0.020", 1706044372],
                ],
                "bids": [
                    ["39163.60000", "8.187", 1706044373],
                    ["39162.80000", "0.768", 1706044375],
                ],
            }
        },
    }


def successful_gemini_response():
    return {
        "bids": [
            {"price": "39150.97", "amount": "0.03319", "timestamp": "1706044291"},
            {"price": "39150.36", "amount": "0.2987", "timestamp": "1706044291"},
        ],
        "asks": [
            {"price": "39155.01", "amount": "0.1162", "timestamp": "1706044291"},
            {"price": "39155.02", "amount": "0.03319", "timestamp": "1706044291"},
        ],
    }


def successful_coinbase_response():
    return {
        "bids": [
            ["40071.98", "0.18687374", "2c8d3a8a-41f6-47a8-83e6-2d021cd64513"],
            ["40071.97", "0.2", "99ab5cdf-24b1-4747-84d5-ccb524ce4fe7"],
        ],
        "asks": [
            ["40072.71", "0.07707", "a057d2dd-8b5c-4327-8501-4ad25b2d805a"],
            ["40075.55", "0.0019513", "20ae18ec-e7d6-47c3-a404-d5470b028867"],
        ],
        "sequence": 72012524197,
        "auction_mode": False,
        "auction": None,
        "time": "2024-01-24T15:47:18.850950Z",
    }
