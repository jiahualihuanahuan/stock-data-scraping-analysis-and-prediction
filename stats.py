import yfinance as yf
import ta
from ta.utils import dropna
import matplotlib.pyplot as plt
from ta.momentum import WilliamsRIndicator
import pandas as pd
from ta import add_all_ta_features
import numpy as np

symbol = 'QQQ'

data = yf.download(f"{symbol}", period="max", interval="1d", progress=False)

data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
data_ta = add_all_ta_features(data, open="Open", high="High", low="Low", close="Adj_Close", volume="Volume", fillna=True)
data_ta.others_dr

np.mean(data_ta.others_dr[-20:])
np.std(data_ta.others_dr[-20:])
