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
	
	=========
	ARGUMENTS:
	=========
	ticker: str, ticker for whichever token you want to pull, assuming it's listed on Kraken
	interval: int, defaulted for daily prices (1440 / 60) = 24 hours

	=======
	RETURNS
	=======
	Pandas data frame for ticker passed into function.

	======
	RAISES
	======
	ValueError if ticker or interval are invalid values
	ImportError if libraries not installed or imported

	'''
	ticker_str = '_'+str(ticker.upper())

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


if __name__ == "__main__": 
	main()
