import uvicorn
from fastapi import FastAPI
import asyncio

from core.utils.fetch_data import (
    fetch_binance_data,
    fetch_kraken_data,
    price_data
)

# Initialize the FastAPI app
app = FastAPI()


@app.on_event("startup")
async def startup_event() -> None:
    """
    Function that runs on application startup.
    Creates asynchronous tasks to fetch data from Binance and Kraken.
    """
    # Get the current event loop
    loop = asyncio.get_event_loop()
    # Start the task to fetch data from Binance
    loop.create_task(fetch_binance_data())
    # Start the task to fetch data from Kraken
    loop.create_task(fetch_kraken_data())


@app.get("/prices")
async def get_prices(
        pair: str = None,
        exchange: str = None
) -> dict:
    """
    API endpoint to retrieve prices.
    Filters: pair (pair) and exchange (exchange) — both can be null.
    """
    result = {}
    # List of supported exchanges
    exchanges = ['BINANCE', 'KRAKEN']
    # If the exchange filter is specified
    if exchange:
        # Check if the exchange is supported
        if exchange.upper() in exchanges:
            # Set the filter to the specified exchange
            exchanges = [exchange.upper()]
        else:
            # Return error if exchange is unsupported
            return {'error': 'Invalid value for the exchange field.'}
    # Iterate over the selected exchanges
    for exch in exchanges:
        # If the pair filter is specified
        if pair:
            pair = pair.upper()
            # Check if the pair is available on the exchange
            if pair in price_data[exch]:
                # Retrieve buy and sell prices
                buy, sell = price_data[exch][pair]
                # Calculate and store the average price
                result[exch] = {pair: (buy + sell) / 2}
        # If the pair is not specified, return all available pairs
        else:
            result[exch] = {}
            # Iterate over all pairs on the exchange
            for p, (buy, sell) in price_data[exch].items():
                # Calculate and store the average price for each pair
                result[exch][p] = (buy + sell) / 2
    return result


# Start the Uvicorn server to run the FastAPI app
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
