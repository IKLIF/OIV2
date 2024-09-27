import requests
from pybit.unified_trading import HTTP

def bybit_get_symbols():
    try:
        session = HTTP(
            testnet=False,
            api_key="9kBNn0gpUuXK6s80l4",
            api_secret="mZ3SJCj9FOuBQnVNnad3xqtrZZ0tp7aOm7qN",
            recv_window=60000
        )

        # spot
        # linear

        tickers_spot = session.get_tickers(category="linear")
        data_tickers = tickers_spot['result']['list']

        data_tickers = [{'symbol':i['symbol'], 'priceChangePercent':round(float(i['price24hPcnt'])*100,3)} for i in data_tickers if i['symbol'][-1] == 'T']
        return data_tickers
                #data.append({'symbol':coin['symbol'], 'priceChangePercent':coin['priceChangePercent']})

        #return data
    except:
        pass


def bybit_get_open_interest_5m(symbol):
    session = HTTP(
        testnet=False,
        api_key="9kBNn0gpUuXK6s80l4",
        api_secret="mZ3SJCj9FOuBQnVNnad3xqtrZZ0tp7aOm7qN",
        recv_window=60000
    )

    result = session.get_open_interest(symbol=symbol, category='linear', intervalTime='5min', limit=4)
    data_interes = result['result']['list']
    data_interes.reverse()

    data = data_interes#[i for i in data_interes]

    return data

def bybit_get_open_interest_15m(symbol):
    session = HTTP(
        testnet=False,
        api_key="9kBNn0gpUuXK6s80l4",
        api_secret="mZ3SJCj9FOuBQnVNnad3xqtrZZ0tp7aOm7qN",
        recv_window=60000
    )

    result = session.get_open_interest(symbol=symbol, category='linear', intervalTime='15min', limit=500)
    data_interes = result['result']['list']
    data_interes.reverse()
    data = [{'openInterest': data_interes[0]['openInterest']} for i in range(0,300)]

    for i in data_interes:
        data.append({'openInterest': i['openInterest']})

    return data

def bybit_get_klines(symbol):
    try:
        times = '15'

        url = "https://api.bybit.com/v5/market/kline"

        # Параметры запроса
        params = {
            "symbol": symbol,  # Пара торгов
            "interval": times,  # Интервал свечей (1 минута)
            "limit": 500  # Количество свечей
        }

        # Выполнение запроса
        response = requests.get(url, params=params).json()

        response = response['result']['list']

        response.reverse()

        return response
    except:
        pass



#print(bybit_get_symbols())

#print(bybit_get_open_interest_5m('LTCUSDT'))

#print(len(bybit_get_open_interest_15m('LTCUSDT')))
#print(bybit_get_open_interest_15m('LTCUSDT'))

#print(bybit_get_trades('LTCUSDT'))

