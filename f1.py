from clean import WTI, BRENT
import pandas as pandas




for x in WTI['Year'].unique():
	for y in WTI['Month'].unique():
		print('Date:', len(WTI[WTI['Year'] == x][WTI['Month']==y]['Date']), x, y)
		print('Price:', len(WTI[WTI['Year'] == x][WTI['Month'] == y]['Price']), x, y)

#if rop[rop['Month'] == yaxis_column]['Price'].iloc[0] > rop[rop['Month'] == yaxis_column]['Price'].iloc[-1] else 'green'
#print(WTI['Month'].unique())
