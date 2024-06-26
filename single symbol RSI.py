import yfinance as yf
import ta
from ta.utils import dropna
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
import pandas as pd


# single symbol RSI
RSI = []
indicator = "RSI"
symbol = "HUG.TO"
data = yf.download(f"{symbol}", period="max", interval="1d", progress=False)
# Add ta features filling NaN values
data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
data[f"{indicator}"] = RSIIndicator(close=data["Adj_Close"]).rsi()
RSI.append([f"{symbol}",f"{data[f"{indicator}"].iloc[-1]}"])

fig, ax1 = plt.subplots(figsize=(10, 5), dpi=120) 
ax1.set_xlabel('Date') 
ax1.set_ylabel(f'{symbol}', color = 'blue') 
ax1.plot(data["Adj_Close"].iloc[-200:], color = 'blue', label=f'{symbol}') 
ax1.tick_params(axis ='y', labelcolor = 'blue') 
  
# Adding Twin Axes

ax2 = ax1.twinx() 
  
ax2.set_ylabel(f'{indicator}', color = 'black') 
ax2.plot(data[f'{indicator}'].iloc[-200:], color = 'black', label=f'{indicator}') 
ax2.tick_params(axis ='y', labelcolor = 'black') 
ax2.axhline(y=70, color = 'green')
ax2.axhline(y=30, color = 'red')
 
# Show plot
plt.title(f"{indicator} of {symbol}")
plt.show()
plt.savefig(f'{indicator} of {symbol}.png') 
