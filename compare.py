# this code compares two stocks or etfs their prices and calculate the linear regression coefficient, intercept and slope


import pandas as pd
import yfinance as yf


# if you don't have a particular timeframe you want to check
etf1 = "BTC-USD"
etf2 = "BTCY.TO"
etf1_data = yf.download(f"{etf1}", period="1w", interval="1h", progress = False)
etf1_data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]

etf2_data = yf.download(f"{etf2}", period="1w", interval="1h", progress = False)
etf2_data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]


# if you have a particular timeframe you want to check
etf1 = "BTC-USD"
etf2 = "BTCY.TO"
startdate = "2024-06-24"
enddate = "2024-06-25"
etf1_data = yf.download(f"{etf1}", start=startdate, end=enddate, interval="1m", progress = False)
etf1_data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]

etf2_data = yf.download(f"{etf2}", start=startdate, end=enddate, interval="1m", progress = False)
etf2_data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]

# combine data

Combined_data = [etf1_data.Adj_Close, etf2_data.Adj_Close]
Combined_data = pd.DataFrame(Combined_data).transpose()
Combined_data.columns = [f"{etf1}", f"{etf2}"]
Combined_data.describe()

# plot the data: two etfs in the same graph
import matplotlib.pyplot as plt
fig, ax1 = plt.subplots(figsize=(16,6))

# Plotting the first set of data on the first y-axis
ax1.plot(etf1_data.Adj_Close, 'g-', label=f"{etf1}")
ax1.set_xlabel("Date")
ax1.set_ylabel(f"{etf1}")
ax1.tick_params(axis='y', labelcolor='g')


# Creating a second y-axis
ax2 = ax1.twinx()
ax2.plot(etf2_data.Adj_Close, 'b-', label=f"{etf2}")
ax2.set_ylabel(f'{etf2}', color='b')
ax2.tick_params(axis='y', labelcolor='b')
# ax2.axhline(y=6.04)
# Adding a legend (handles the legend from both axes)
fig.tight_layout()
fig.legend(loc='upper left', bbox_to_anchor=(0.1,0.9))
# title
plt.title(f"{etf1} vs. {etf2}")
plt.savefig(f'{etf1} vs. {etf2}.png') 

# linear regression
from sklearn.linear_model import LinearRegression

X, y = Combined_data.dropna()[f"{etf2}"].array.reshape(-1, 1), Combined_data.dropna()[f"{etf1}"].array.reshape(-1, 1)
reg = LinearRegression().fit(X, y)
reg.score(X, y)

# get slope
reg.coef_

# get intercept
reg.intercept_
