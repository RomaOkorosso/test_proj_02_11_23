import time
import ccxt

# class object Binance
exchange = ccxt.binance()

# identification of XRP/USDT pair
symbol = "XRP/USDT"

# max price from current price
max_price = 0

while True:
    # get current XRP/USDT price
    ticker = exchange.fetch_ticker(symbol)
    current_price = ticker["last"]

    # if current price is higher than max price from last hour - update max price
    if current_price > max_price:
        max_price = current_price

    # if price downed by 1% from max price - send notification
    if current_price < max_price * 0.99:
        print("Price fell by 1% from the maximum price!")

    # wait 1 second
    time.sleep(1)
