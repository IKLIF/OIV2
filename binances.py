import requests

def binance_get_symbols():
    try:
        url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
        response = requests.get(url, timeout=30)
        data_many_f = response.json()

        data = []

        for coin in data_many_f:
            symbol = coin['symbol']
            if symbol[-1] == 'T':
                data.append({'symbol':coin['symbol'], 'priceChangePercent':coin['priceChangePercent']})

        return data
    except:
        pass

def binance_get_open_interest_5m(symbol):
    try:
        base_url = "https://fapi.binance.com"
        endpoint = "/futures/data/openInterestHist"
        params = {
            "symbol": symbol,
            "period": "5m",  # Интервал времени (5 минут, 1 час, 1 день и т. д.)
            "limit": 4  # Количество записей
        }

        response = requests.get(base_url + endpoint, params=params, timeout=30)
        data = response.json()
        return data
    except:
        pass

def binance_get_open_interest_15m(symbol):
    try:
        base_url = "https://fapi.binance.com"
        endpoint = "/futures/data/openInterestHist"
        params = {
            "symbol": symbol,
            "period": "15m",  # Интервал времени (5 минут, 1 час, 1 день и т. д.)
            "limit": 500  # Количество записей
        }

        response = requests.get(base_url + endpoint, params=params, timeout=30)
        data = response.json()
        return data
    except:
        pass

def binance_get_klines(symbol):
    try:
        url = f'https://fapi.binance.com/fapi/v1/klines'
        params = {
            'symbol': symbol,
            'interval': '15m',  # Интервал - 1 час
            'limit': 500,  # 24 часа
        }

        response = requests.get(url, params=params, timeout=30).json()
        return response
    except:
        pass



def volue(symbol):
    try:
        url = f'https://fapi.binance.com/fapi/v1/klines'
        params = {
                'symbol': symbol,
                'interval': '5m',  # Интервал - 1 час
                'limit': 24,  # 24 часа
                }

        response = requests.get(url, params=params, timeout=30)
        data_back = response.json()

        url = f'https://fapi.binance.com/fapi/v1/klines'
        params = {
                'symbol': symbol,
                'interval': '5m',  # Интервал - 1 час
                'limit': 12,  # 24 часа
                }

        response = requests.get(url, params=params, timeout=30)
        data_now = response.json()

        data_back = [data_back[i][5] for i in range(0,12)]

        #for i in data_back:
         #   i[0] = pd.to_datetime(i[0], unit='ms')
          #  print(f'timestamp: {i[0]}, open: {i[1]}, high: {i[2]}, low: {i[3]}, close: {i[4]}, volume: {i[5]}, close_time: {i[6]}, quote_asset_volume:{i[7]}, trades: {i[8]}, taker_buy_base: {i[9]}, taker_buy_quote: {i[10]}')

        all = 0
        for i in data_back:
            all += float(i)

        all /= 12


        data_now = [i[5] for i in data_now]
        all_now = 0
        for i in data_now:
            all_now += float(i)

        all_sr = all_now/12

        #z = (x / y - 1) * 100
        pr_all = (all_sr-all)/all_sr * 100#(data_vol_now - data_back_vol_sr)/data_vol_now * 100
        pr_all = round(pr_all, 3)
        return f'📌Volume: 👉 {pr_all}%'

    except Exception as e:
        pass
        #print('\nОшибка:\n', traceback.format_exc())

def binance_get_trades(symbol):
    try:
        url = f'https://api.binance.com/api/v3/klines'
        params = {
            'symbol': symbol,
            'interval': '5m',  # Интервал - 1 час
            'limit': 96,  # 24 часа
        }

        response = requests.get(url, params=params, timeout=30)
        data_back = response.json()

        x = 0
        for i in data_back:
            x += i[8]


        return x

    except Exception as e:
        pass
        #print('\nОшибка:\n', traceback.format_exc())






