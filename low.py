# check if a security is within 5% low of the year
# the code can be modified to check a different percentage of a different period (timeframe)

"""
python low.py FAVS 1y
python low.py FAV 1y

python low.py CADEQTY 1y
python low.py USDEQTY 1y
python low.py CDR 1y
python low.py XIU.TO 1y
python low.py SPY 1y
python low.py PURPOSE 1y
python low.py HAMILTON 1y
python low.py GLOBALX 1y

python low.py BROMPTON 1y
python low.py EVOLVE 1y
python low.py HARVEST 1y
python low.py INVESCO 1y
python low.py MIDDLEFIELD 1y



"""
import sys
import pandas as pd
from datetime import date
import yfinance as yf
import os

etf_name = sys.argv[1]
period = sys.argv[2]

indicator = "low"

# single security
# symbol = "SHOP.TO"
# data = yf.download(f"{symbol}", period="1y", interval="1d", progress=False)
# data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
# if data.Adj_Close[-1] < min(data.Low)*1.05:
#     print(f"{symbol} is within 5% low of the year")
# else:
#     print(f"{symbol} is not within 5% low of the year")

# a list of securities
# list_name = "CADETF"
list_ = pd.read_csv(f"https://raw.githubusercontent.com/jiahualihuanahuan/stock-data-scraping-analysis-and-prediction/main/{etf_name}.csv", encoding='latin-1')
# list_.columns = ["Symbol"]
low = []
for symbol in list_.Symbol:
    try:
        data = yf.download(f"{symbol}", period=period, interval="1d", progress=False)
        # Add ta features filling NaN values
        data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
        low.append([f"{symbol}",min(data.Low),data.Adj_Close.iloc[-1],(data.Adj_Close.iloc[-1]-min(data.Low))*100/(data.Adj_Close.iloc[-1])])
        if min(data.Low)*1.05 < data.Adj_Close.iloc[-1] < min(data.Low)*1.1:
            print(f"{symbol} is within 10% low of the year")
        elif min(data.Low)*1.01 < data.Adj_Close.iloc[-1] < min(data.Low)*1.05:
            print(f"{symbol} is within 5% low of the year")
        elif data.Adj_Close.iloc[-1] < min(data.Low)*1.01:
            print(f"{symbol} is within 1% low of the year")
        else:
            pass
    except:
        pass

low_df = pd.DataFrame(low)
low_df.columns = ["Symbol","Minimum_Price","Current_Price","Percentage_Low"]
print(low_df.sort_values(by="Percentage_Low"))

today = date.today()
if not os.path.exists(f'./{today}/{indicator}'):
   os.makedirs(f'./{today}/{indicator}')
low_df.sort_values(by="Percentage_Low").to_csv(f"./{today}/{indicator}/{etf_name}.csv")
