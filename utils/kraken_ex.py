'''
Uses Kraken Python API to pull crypto data.

'''
import datetime
import numpy as np
import krakenex
from pykrakenapi import KrakenAPI

api = krakenex.API()
k = KrakenAPI(api)

def pull_data(ticker, interval = 1440):
	'''
	Pulls data for different cryptos from Kraken API.
	Interval is on per minute basis, but function defaults to daily prices
	'''
	ticker_str = '_'+str(ticker)

	ticker, last = k.get_ohlc_data(str(ticker)+'USD', interval)

	ticker['log_high'] = np.log(ticker['high'])
	ticker['log_low'] = np.log(ticker['low'])
	ticker['log_vwap'] = np.log(ticker['vwap'])

	col_names = ['time']

	for i in ticker.columns:
		if i != 'time':
			col_names.append(i+ticker_str)

	ticker.columns = col_names

	now = datetime.datetime.now()

	print(f"Pulled {ticker_str} at {now}")

	return ticker

def merge_data(dfs):
	'''
	Merge dataframes on the time column to have all cryptos in one dataframe
	dfs should be passed as a list of dataframes.
	'''
	df_merged = reduce(lambda left, right: pd.merge(left,right,
		on = ['time'],
		how = 'outer'),
	dfs)

	df_merged.index = dfs[0].index
	df_merged = df_merged.drop(columns = ['time'])

	return df_merged


if __name__ == "__main__": main()
