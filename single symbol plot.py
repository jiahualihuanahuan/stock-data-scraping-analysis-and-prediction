import plotly.graph_objects as go
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import pandas as pd
from datetime import datetime
import yfinance as yf
symbol = "URA"
df = yf.download(f"{symbol}", period="1d", interval="1m", progress=False)
df.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]


figure(figsize=(18, 6), dpi=120)
plt.plot(df["Adj_Close"], color = 'red')
print(f"Current Price of {symbol} is ${df.Adj_Close.iloc[-1]}")
print(f"Lowest Price of {symbol} is ${min(df.Adj_Close)}")
