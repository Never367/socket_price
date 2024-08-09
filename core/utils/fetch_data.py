from decimal import Decimal, getcontext

import websockets
import json

# Set the precision for Decimal operations to 8 significant digits
getcontext().prec = 8

# Dictionary to store price data for Binance and Kraken exchanges
price_data = {
    'BINANCE': {},
    'KRAKEN': {}
}


async def fetch_binance_data() -> None:
    """
    Establishes a WebSocket connection to Binance and continuously
    retrieves real-time ticker data for all trading pairs.
    """
    # Binance WebSocket URI for all tickers
    uri = "wss://stream.binance.com:9443/ws/!ticker@arr"
    # Establish the connection
    async with websockets.connect(uri) as websocket:
        while True:
            # Receive data from Binance
            data = await websocket.recv()
            # Parse the JSON data
            tickers = json.loads(data)
            for ticker in tickers:
                # Extract the trading pair symbol
                pair = ticker['s']
                # Store the bid and ask prices in the price_data
                price_data['BINANCE'][pair] = (
                    Decimal(ticker['b']),
                    Decimal(ticker['a'])
                )


async def fetch_kraken_data() -> None:
    """
    Establishes a WebSocket connection to Kraken and continuously
    retrieve real-time ticker data for all trading pairs.
    """
    # Kraken WebSocket URI
    uri = "wss://ws.kraken.com/v2"
    # Establish the connection
    async with websockets.connect(uri) as websocket:
        await websocket.send(
            json.dumps({
                "method": "subscribe",
                'params': {
                    # Subscribe to the ticker channel
                    "channel": "ticker",
                    # Request data for all trading pairs
                    "symbol": ['*']
                }
            }))
        while True:
            # Receive data from Kraken
            data = await websocket.recv()
            # Parse the JSON data
            message = json.loads(data)
            # Check if the message is from the ticker channel
            if "channel" in message and message['channel'] == 'ticker':
                for ticker in message['data']:
                    # Normalize the pair symbol
                    pair = ticker['symbol'].replace("/", '')
                    # Store the bid and ask prices in the price_data
                    price_data['KRAKEN'][pair] = (
                        Decimal(ticker['bid']),
                        Decimal(ticker['ask'])
                    )
