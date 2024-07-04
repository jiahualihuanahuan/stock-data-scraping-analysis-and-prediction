import yfinance as yf
import ta
from ta.utils import dropna
import matplotlib.pyplot as plt
from ta.momentum import RSIIndicator
import pandas as pd
import sys
from tqdm import tqdm
from ta import add_all_ta_features
from datetime import date
import os

"""
python rsi.py SPY 40
two arguments: index/etf/list name and RSI threshold
"""

etf_name = sys.argv[1]
threshold = int(sys.argv[2])
indicator = "RSI"
# multiple symbols' RSI
# etf_list = [""]
etf_list = pd.read_csv(f"https://raw.githubusercontent.com/jiahualihuanahuan/stock-data-scraping-analysis-and-prediction/main/{etf_name}.csv") # , encoding='latin-1' 

RSI = []
today = date.today()
if not os.path.exists(f'./{today}/{indicator}'):
   os.makedirs(f'./{today}/{indicator}')

for symbol in etf_list.Symbol.to_list():
    try:
        stock_data = yf.download(f"{symbol}", period="max", interval="1d", progress = False)
        stock_data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
        data_ta = add_all_ta_features(stock_data, open="Open", high="High", low="Low", close="Adj_Close", volume="Volume")
        RSI.append([f"{symbol}",data_ta.momentum_rsi.iloc[-1]])
        print(f"{indicator} of {symbol} is {data_ta.momentum_rsi.iloc[-1]}")
        if data_ta.momentum_rsi.iloc[-1] < threshold:
            # plot RSI over time
            fig, ax1 = plt.subplots(figsize=(16,6))

            # Plotting the first set of data on the first y-axis
            color = 'tab:red'
            ax1.set_xlabel("Date")
            ax1.set_ylabel(f"RSI", color=color)
            ax1.plot(data_ta.momentum_rsi.iloc[-200:], color=color, label=f"RSI of {symbol}")
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.axhline(y=70, color="r", linewidth = 3)
            ax1.axhline(y=65, color="r")
            ax1.axhline(y=30, color="g", linewidth = 3)
            ax1.axhline(y=35, color="g")

            # Creating a second y-axis
            ax2 = ax1.twinx()
            color = 'tab:blue'
            ax2.set_ylabel(f'{symbol}', color=color)
            ax2.plot(stock_data.Adj_Close.iloc[-200:], color=color, label=f'{symbol}')
            ax2.tick_params(axis='y', labelcolor=color)

            # Adding a legend (handles the legend from both axes)
            fig.tight_layout()
            fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
            # title
            plt.title(f"{symbol} RSI")

            plt.savefig(f'./{today}/{indicator}/{symbol}.png') 
            # plt.show()
            # plt.close()

    except:
        print(f"{symbol} not available")
            

RSI_df = pd.DataFrame(RSI)
RSI_df.columns = ["Symbol","RSI"]
print(RSI_df.sort_values(by="RSI"))


RSI_df.sort_values(by="RSI").to_csv(f"./{today}/{indicator}/{etf_name}.csv")
