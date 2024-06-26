import yfinance as yf
import ta
from ta.utils import dropna
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
import pandas as pd
import sys

etf_name = sys.argv[1]
threshold = sys.argv[2]

# multiple symbols' RSI
# etf_list = [""]
etf_list = pd.read_csv(f"https://raw.githubusercontent.com/jiahualihuanahuan/stock-data-scraping-analysis-and-prediction/main/{etf_name}.csv") # , encoding='latin-1' 
RSI = []

for symbol in etf_list.Symbol: # ["Symbol"]
    indicator = "RSI"
    print(symbol)
    try:
        data = yf.download(f"{symbol}", period="max", interval="1d", progress=False)
        # Add ta features filling NaN values
        data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
        data[f"{indicator}"] = RSIIndicator(close=data["Adj_Close"]).rsi()
        if data[ f"{indicator}"].iloc[-1] < int(threshold):
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
            plt.savefig(f'{indicator} of {symbol}.png') 
            plt.show()
    except:
        print(f"{symbol} not available")
            

RSI_df = pd.DataFrame(RSI)
RSI_df.columns = ["Symbol","RSI"]
print(RSI_df.sort_values(by="RSI"))
RSI_df.sort_values(by="RSI").to_csv("RSI.csv")
