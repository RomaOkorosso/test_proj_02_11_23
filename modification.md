Чтобы программа могла обрабатывать не только пару XRP/USDT,
но и другие пары, можно добавить возможность ввода пары
пользователем.
Для этого можно использовать командную строку или ввод данных через UI.

Также, можно хранить список всех поддерживаемых пар в
конфиг файле или в БД, и позволять пользователю
выбрать интересующую его пару из списка.

Для обработки ввода пользователя можно использовать:

1. В коде можно использовать цикл,
   чтобы обрабатывать все пары по очереди.
   В этом цикле можно вызывать функцию получения
   цены для каждой пары, и сравнивать текущую цену с
   максимальной ценой для этой пары.

2. Вы можете использовать asyncio в Python, чтобы организовать асинхронную обработку нескольких пар.

   Основные шаги будут следующие:
    1. Определите функцию, которая будет запрашивать цену для одной пары.
    2. Определите функцию, которая будет вызывать функцию из п.1 для каждой пары и возвращать ответы в виде генератора.
    3. Используйте `asyncio.gather()` для сбора ответов из всех вызовов функции из п.2.
    4. Внутри `asyncio.gather()` определите колбек, который будет вызываться, когда все ответы будут получены, и
       обработайте эти ответы.

Примерно так:

```python

import asyncio
import aiohttp

async def fetch_price(session, symbol):
    async with session.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}") as resp:
        if resp.status != 200:
            return None
        price_data = await resp.json()
        return float(price_data["price"])

async def monitor_price(symbol, threshold):
    async with aiohttp.ClientSession() as session:
        while True:
            price = await fetch_price(session, symbol)
            if price is None:
                print(f"Failed to fetch price for {symbol}")
            elif price < threshold:
                print(f"{symbol} is now below {threshold} ({price})")
            await asyncio.sleep(1)

async def main():
    symbols = ["XRPUSDT", "BNBUSDT", "BTCUSDT"]
    tasks = [asyncio.create_task(monitor_price(symbol, threshold=0.9)) for symbol in symbols]
    await asyncio.gather(*tasks)

asyncio.run(main())
```