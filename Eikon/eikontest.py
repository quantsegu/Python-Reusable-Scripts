import eikon as ek  # the Eikon Python wrapper package
import numpy as np  # NumPy
import pandas as pd  # pandas
import warnings
import sys
import json
import os

with open(os.path.dirname(os.path.realpath(__file__)) + '\\config.json', 'r') as f:
    config = json.load(f)

# Get information from the Configuration file
Tickers = config['TickersFile']
ReutersKey = config['ReutersKey']
FieldsToFetch = config['FieldsToFetch']
Options = config["FetchOptions"]

options = ""

for attribute, value  in Options.items():
    options = options + '\'' + attribute + '\':\'' + value + '\','

warnings.filterwarnings("ignore")

df = pd.read_csv(Tickers, header=None)
ek.set_app_key(ReutersKey)

tickers = list(df[0])
data, error = ek.get_data(tickers,FieldsToFetch,options[:-1])
data.to_csv(str(Tickers).replace('.csv', '.result'))