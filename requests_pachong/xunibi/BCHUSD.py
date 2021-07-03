import requests
import pandas as pd
import matplotlib
import mplfinance as mpf
from matplotlib import pyplot as plt
import matplotlib.dates
import numpy as np

# BITCOKE网址 www.bitcoke.pro,注意.com域名遭到污染，如果某些页面无法访问需要改成.pro.
from matplotlib.pyplot import setp

class BitcokeRest:

    def __init__(self):
        self.base = 'http://api.bitcoke.pro/'

    # bitcoke交易所数据获取rest api
    def bitcoke_k(self, start=1624440940582, symbol='XBTCUSD', period='4H'):
        url = 'api/kLine/byTime'
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36'}
        print('K line period list: 1M, 3M, 5M, 10M, 15M, 30M, 1H, 2H, 4H, 6H, 8H, 12H, D, W, MTH')
        payload = {
            'from': start,
            'step': 500,
            'symbol': symbol,
            'type': period
        }
        data = requests.get(self.base + url, params=payload, headers=header).json()
        df = pd.DataFrame(data['result'])
        return df

def KLinePlot(Data):
    # 删除 不需要的数据，保留 Date, Open, High, Low, Close, Volume
    df = Data.drop(labels=['source', 'symbol', 'keyTime', 'turnover'], axis=1)

    # 对数据关键词改名，必须为Date, Open, High, Low, Close, Volume
    df.rename(
        columns={'timeStamp': 'Date', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'},
        inplace=True)

    # 原数据是按时间倒叙的 倒转数据
    df = df[::-1]
    # print(df)
    # print(df.columns)
    # 把 Date 列数据设置成索引
    df.set_index(["Date"], inplace=True)

    # 把 Date 数据转换成 datetime 格式
    df.index = pd.to_datetime(df.index)

    # 这里可以自定义样式
    # mc = mpf.make_marketcolors(
    #     up="red",  # 上涨K线的颜色
    #     down="green",  # 下跌K线的颜色
    #     # edge="black",  # 蜡烛图箱体的颜色
    #     # wick="red"  # 蜡烛图影线的颜色
    # )
    # # 改变样式style
    # style = mpf.make_mpf_style(marketcolors=mc)
    mpf.plot(
        data=df,
        type="candle",
        title="Candlestick for XBTCUSD",
        ylabel="price($)",
        style='binance',
        volume=True,
        ylabel_lower="volume(shares)",
        figratio = (2, 1),
        mav = (7, 25, 99),   #平均线
        datetime_format = '%Y-%m-%d %H:%M'
    )


if __name__ == '__main__':
    print('start')
    a = BitcokeRest()
    data_BTC = a.bitcoke_k(start=1624440940582, symbol='XBTCUSD')
    data_BCH = a.bitcoke_k(start=1624441489097, symbol='XBCHUSD')
    # res.to_csv('data_BTCUSD.csv', mode='a', header=False)
###Index(['source', 'symbol', 'open', 'close', 'high', 'low', 'keyTime','timeStamp', 'volume', 'turnover']

    KLinePlot(data_BTC)
    KLinePlot(data_BCH)
    # 基本 获取近3个月XBTCUSD的柱状图数据，并进行图像化，要求价格数据和交易量数据进行图像分离。
    # 进阶 获取近3个月XBCHUSD的柱状图数据，与XBTCUSD数据进行对比，并形成分析报告（想到什么、看到什么、分析出什么都能写）
    # 基本 将代码提交至你本人的Gitee.com代码库，并设为公开以供查阅。


