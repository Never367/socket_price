# Mini-app for test task

To start a project, you must execute commands in the project root: `docker build -t socket_price_app .` and `docker run -p 8000:8000 socket_price_app`.  
There is no .env file in the project because there is no sensitive information here.

### Project description
The app connects to cryptocurrency exchanges Binance and Kraken via sockets and receives real-time price data for all currency pairs. When you query, you get the latest data received from the exchanges.

### List of endpoints
1. http://localhost:8000/prices — obtaining data on currency exchanges.  
Accepts 2 query params: pair and exchange. These parameters filter the data output. If only exchange is specified, the result will be output only for this exchange. If only pair is specified, the result for this pair will be output for both exchanges. If both pair and exchange are specified, the result for both pair and exchange will be output. If nothing is specified, all received data on exchanges will be displayed.

Thank you for the test assignment.