# which stock just moved above it 20 sma line

list = pd.read_csv("https://raw.githubusercontent.com/jiahualihuanahuan/stock-data-scraping-analysis-and-prediction/main/CDR.csv", encoding='latin-1')
for symbol in list.Symbol:
    data = yf.download(f"{symbol}", period="max", interval="1d", progress=False)
    data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]
    # data_ta = add_all_ta_features(data, open="Open", high="High", low="Low", close="Adj_Close", volume="Volume", fillna=True)
    data["20SMA"] = data.Adj_Close.rolling(window=20).mean()
    
    if data["20SMA"].iloc[-2] > data.Adj_Close.iloc[-2] and data["20SMA"].iloc[-1] < data.Adj_Close.iloc[-1]:
    
        figure(figsize=(18, 6), dpi=120)
        plt.plot(data["Adj_Close"].iloc[-250:], color = 'blue')
        plt.plot(data["20SMA"].iloc[-250:], color = 'red')
        # plt.plot(data["Low"], color = 'green')
        plt.title(f'{symbol}')
        plt.show()
    else:
        pass
