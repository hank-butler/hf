'''
=================
Kraken Util Class
=================

Practicing OOP by making kraken_ex.py file into a class for
more pythonic implementation and to practice for algo trading
job interviews.

'''

class Kraken:
    def __init__(self):
        import datetime
        import numpy as np
        import krakenex
        from pykrakenapi import KrakenAPI
        self.api = krakenex.API()
        self.k = KrakenAPI(self.api)

    def pull_data(self, ticker, interval = 1440):
        '''
        Pulls data for different cryptos from KrakenAPI.
        Interval is on per minute basis, function defaults to daily
        (1440 / 60) = 24

        '''
        ticker_str = '_'+str(ticker)

        ticker, last = self.k.get_ohlc_data(str(ticker)+'USD', interval)

        ticker['log_high'] = np.log(ticker['high'])
        ticker['log_low'] = np.log(ticker['low'])
        ticker['log_vwap'] = np.log(ticker['vwap'])

        col_names = ['time']

        for i in ticker.columns:
            if i != 'time':
                col_names.append(i+ticker_str)

        ticker.columns = col_names

        print(f'Pulled {ticker_str} at {datetime.datetime.now()}')

        return ticker
