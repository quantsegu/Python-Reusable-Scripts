import eikon as ek  # the Eikon Python wrapper package
import numpy as np  # NumPy
import pandas as pd  # pandas
import configparser as cp
import warnings
import sys
warnings.filterwarnings("ignore")
df = pd.read_csv(r'C:\Users\segul\OneDrive\Documents\ReutersTickers.csv', header=None)
ek.set_app_id('a17f5ab013e449cc86857ecbfe62f4c96577df86')
tickers = list(df[0])
# text = ''
data, error = ek.get_data(tickers,'TR.CDSPrimaryCDSRic')
data.dropna(inplace=True)
data = data[data['Primary CDS RIC']!='']
data.to_csv(r'C:\Users\segul\OneDrive\Documents\ReutersTickersData.csv')
cdsIdList = [str(cdsId)  for cdsId in data.ix[:,1].values]
print('================')
result, err = ek.get_data(cdsIdList, ['PRIMACT_1'])
print('#2')
result.to_csv(r'C:\Users\segul\OneDrive\Documents\ReutersTickersOutput2.csv')
dfFinal = pd.merge(data, result, left_on='Primary CDS RIC', right_on='Instrument', how='left')
dfFinal.to_csv(r'C:\Users\segul\OneDrive\Documents\ReutersTickersFinal.csv')
print('#3')