import eikon as ek  # the Eikon Python wrapper package
import numpy as np  # NumPy
import pandas as pd  # pandas
import configparser as cp
import warnings
import sys
warnings.filterwarnings("ignore")

ek.set_app_id('a17f5ab013e449cc86857ecbfe62f4c96577df86')
df = pd.read_csv(r'C:\Users\segul\OneDrive\Documents\CDSNLTickers.csv', header=None)
tickers = list(df[0])
d = []
dates = ['2020-03-02', '2020-03-16', '2020-04-10']
for x in dates:
    data,error = ek.get_data(tickers,
                   ['TR.PARMIDSPREAD'],
                   {'SDate': x, 'EDate': x, 'DateType': 'AD', 'CURN': 'EUR'})
    data.dropna(inplace=True)
    data['Date'] = x
    d.append(data)
FinalData = pd.concat(d)
FinalData.to_csv(r'C:\Users\segul\OneDrive\Documents\CDSNLTickersResult.csv')
# print(tickers)
print('#1')
