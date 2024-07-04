import pandas as pd
import yfinance as yf
from tqdm import tqdm
import sys
import matplotlib.pyplot as plt

"""
to run this script:
python pasma.py QQQ 20 1y 1d
"""

index_name = sys.argv[1]
sma_period = int(sys.argv[2])
period = sys.argv[3]
interval = sys.argv[4]

# index_list = pd.read_csv(f"https://raw.githubusercontent.com/jiahualihuanahuan/stock-data-scraping-analysis-and-prediction/main/{index_name}.csv")
index_list = pd.read_csv(f"https://raw.githubusercontent.com/jiahualihuanahuan/stock-data-scraping-analysis-and-prediction/main/{index_name}.csv")
def get_stock_data(stock_symbol, period, interval):
    """
    function to get stock historical data using yfinance library
    """
    stock_data = yf.download(stock_symbol, period=period, interval=interval, progress = False)
    stock_data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
    return stock_data


def above_or_below(stock_symbol, sma, period, interval):
    """
    function to check if close price is above a certain period SMA
    """
    stock_data = get_stock_data(stock_symbol, period=period, interval=interval)
    stock_data['SMA'] = (stock_data['Adj_Close'].rolling(sma).mean() <= stock_data['Adj_Close'])
    return stock_data['SMA']

def percentage_above_SMA(stock_list, sma, period, interval):
    """
    function to calculate the percentage of the stocks that above certain period SMA
    
    """
    mb = []
    pas = pd.DataFrame
    for i in tqdm(range(len(stock_list))):
        mb.append(above_or_below(stock_list[i], sma=sma, period=period, interval=interval))
        pas = pd.DataFrame(mb).transpose().sum(axis=1)
    return (pas/len(stock_list))*100

# Percentage of stocks above 50 SMA (one of the Market Breadth indicator)

pasma = percentage_above_SMA(index_list.Symbol, sma=sma_period, period=period, interval=interval)
print(f"current Market Breadth: there are {pasma.iloc[-1]}% stocks in {index_name} is above {sma_period} day Simple Moving Average")

fig, ax1 = plt.subplots(figsize=(16,6))

# Plotting the first set of data on the first y-axis
ax1.plot(pasma, 'g-', label=f"Percentage of stocks above {sma_period} SMA")
ax1.set_xlabel("Date")
ax1.set_ylabel(f"Percentage of stocks above {sma_period} SMA")
ax1.tick_params(axis='y', labelcolor='g')
ax1.axhline(y=85, color="r", linewidth = 3)
ax1.axhline(y=80, color="r")
ax1.axhline(y=15, color="g", linewidth = 3)
ax1.axhline(y=20, color="g")

# Creating a second y-axis
ax2 = ax1.twinx()
ax2.plot(get_stock_data(f"{index_name}", period=period, interval=interval)["Adj_Close"], 'b-', label=f'{index_name}')
ax2.set_ylabel(f'{index_name}', color='b')
ax2.tick_params(axis='y', labelcolor='b')

# Adding a legend (handles the legend from both axes)
fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
# title
plt.title(f"{index_name} Percentage of stocks above {sma_period} SMA")
plt.savefig(f'{index_name} Percentage of stocks above {sma_period} SMA.png') 
plt.show()
