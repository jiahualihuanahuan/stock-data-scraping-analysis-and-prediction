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

# a list of security
etf_list = pd.read_csv("https://raw.githubusercontent.com/jiahualihuanahuan/stock-data-scraping-analysis-and-prediction/main/CADETF.csv", encoding='latin-1')
for symbol in etf_list.Symbol:
    try:
        data = yf.download(f"{symbol}", period="max", interval="1d", progress=False)
        # Add ta features filling NaN values
        data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
        if data.Adj_Close[-1] < min(data.Low)*1.05:
            print(f"{symbol} is within 5% low of the year")
        else:
            print(f"{symbol} is not within 5% low of the year")

    except:
        print(f"{symbol} error, not screened")
