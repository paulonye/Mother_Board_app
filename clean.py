import pandas as pd
import datetime as dt


WTI = pd.read_csv('Wti.csv')
WTI  = WTI.dropna()
BRENT = pd.read_csv('Brent.csv')
BRENT = BRENT.dropna()



WTI['Date'] = pd.to_datetime(WTI['Date'])
BRENT['Date'] = pd.to_datetime(BRENT['Date'])

WTI = WTI.sort_values(by = 'Date', ascending=True)
BRENT = BRENT.sort_values(by = 'Date', ascending = True)
WTI['Month'] = WTI['Date'].dt.month_name()
WTI['Day'] = WTI['Date'].dt.day
WTI['Year'] = WTI['Date'].dt.year.astype('str')
WTI['Month-Day'] = WTI['Month'].str[0:3]+'-'+WTI['Day'].astype('str')

BRENT['Month'] = BRENT['Date'].dt.month_name()
BRENT['Day'] = BRENT['Date'].dt.day
BRENT['Year'] = BRENT['Date'].dt.year.astype('str')
BRENT['Month-Day'] = BRENT['Month'].str[0:3]+'-'+BRENT['Day'].astype('str')
#print(WTI['Year'])
#print(WTI['Month-Day'])


