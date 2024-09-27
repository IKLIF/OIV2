from mplchart.chart import Chart
from mplchart.primitives import Candlesticks, Volume, OHLC
from mplchart.indicators import SMA, RSI, MACD
import matplotlib.pyplot as plt
import requests
from datetime import datetime
import pandas as pd

from dataclasses import dataclass

from mplchart.library import get_series, calc_ema

@dataclass
class Open_Interest:
    """ Double Exponential Moving Average """
    period: int = 1

    same_scale = False
    # same_scale is an optional class attribute that indicates
    # the indicator should be plot on the same axes by default

    def __call__(self, prices):
        series = prices['oi']
        OI = calc_ema(series, self.period)
        return OI

def get_chart(symbol, datas, date):

    interval = '15m'

    df = pd.DataFrame(datas, index=date)
    df.index = df.index.rename('Date')

    ticker = f'{symbol}->{interval}'
    prices = df

    max_bars = 288

    indicators = [
        Candlesticks(colorup='#1B4B5A', colordn='#F55449'), Volume(), SMA(100), SMA(200), Open_Interest()  # RSI(), MACD(),#, SMA(50), SMA(200)
    ]

    ##00FF00
    chart = Chart(title=ticker, max_bars=max_bars)  # , bgcolor='#c7c7c7')
    chart.plot(prices, indicators)

    # Save the chart as an image
    plt.savefig(f'img/{symbol}.png')
    plt.close()