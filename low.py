# check if a security is within 5% low of the year
# the code can be modified to check a different percentage of a different period (timeframe)

# single security
import yfinance as yf
symbol = "SHOP.TO"
data = yf.download(f"{symbol}", period="1y", interval="1d", progress=False)
data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
if data.Adj_Close[-1] < min(data.Low)*1.05:
    print(f"{symbol} is within 5% low of the year")
else:
    print(f"{symbol} is not within 5% low of the year")

# a list of securities
list_name = "CADETF"
list = pd.read_csv(f"https://raw.githubusercontent.com/jiahualihuanahuan/stock-data-scraping-analysis-and-prediction/main/{list_name}.csv", encoding='latin-1')
# list.columns = ["Symbol"]
for symbol in list.Symbol:
    try:
        data = yf.download(f"{symbol}", period="1y", interval="1d", progress=False)
        # Add ta features filling NaN values
        data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
        if min(data.Low)*1.01 < data.Adj_Close.iloc[-1] < min(data.Low)*1.05:
            print(f"{symbol} is within 5% low of the year")
        elif data.Adj_Close.iloc[-1] < min(data.Low)*1.01:
            print(f"{symbol} is within 1% low of the year")
        else:
            pass
    except:
        pass
