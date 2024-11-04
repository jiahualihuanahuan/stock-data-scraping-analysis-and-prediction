import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
import sys
from datetime import date
import os
"""
relationship
python ratio.py DX=F TLT
python ratio.py XLV SPY
python ratio.py XDIV.TO SPY
python ratio.py JEPI.TO JEPI
python ratio.py JEPQ.TO JEPQ

related tickers
python ratio.py LPAY.TO TLT
python ratio.py HPYT.TO TLT
python ratio.py HBND.TO TLT

python ratio.py QQC.TO QQQ

python ratio.py TSLA.NE TSLA
python ratio.py YTSL.NE TSLA

python ratio.py AMZN.NE AMZN
python ratio.py YAMZ.NE AMZN

python ratio.py YGOG.NE GOOG
python ratio.py GOOG.NE GOOG

python ratio.py NVDA.NE NVDA 
python ratio.py YNVD.NE NVDA 
python ratio.py NVDH.TO NVDA
python ratio.py NVHE.TO NVDA

python ratio.py MA.NE MA 
python ratio.py DIS.NE DIS

python ratio.py MSFT.NE MSFT
python ratio.py MSFY.NE MSFT

python ratio.py MCDS.NE MCD 
python ratio.py AMD.NE AMD 
 

python ratio.py INTC.NE INTC 
python ratio.py SMCI.NE SMCI 

python ratio.py XOM.NE XOM
python ratio.py DEER.NE DE
python ratio.py VISA.NE V
python ratio.py UBER.NE UBER
python ratio.py DIS.NE DIS
python ratio.py SBUX.NE SBUX
python ratio.py JNJ.NE JNJ
python ratio.py MCDS.NE MCD
python ratio.py RTX.NE RTX
python ratio.py YAMZ.NE AMZN
python ratio.py MSFT.NE MSFT
python ratio.py MSFY.NE MSFT

python ratio.py RTX.NE RTX
python ratio.py AMZN.NE AMZN
python ratio.py YAMZ.NE AMZN

python ratio.py JNJ.NE JNJ


python ratio.py XTLH.TO TLT

python ratio.py ZDJ.TO DIA

python ratio.py CHPS.TO SMH

python ratio.py XQQ.TO QQQ

python ratio.py EQL.TO RSP

python ratio.py ZSP.TO SPY

python ratio.py BTCY.TO BTC-USD 
python ratio.py BTC-USD BTC-CAD 
python ratio.py ETHY.TO ETH-USD 

"""

etf1 = sys.argv[1]
etf2 = sys.argv[2]

indicator = "ratio"
today = date.today()
if not os.path.exists(f'./{today}/{indicator}'):
   os.makedirs(f'./{today}/{indicator}')

etf1_data = yf.download(f"{etf1}", period="5d", interval="1m", progress = False)
etf1_data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]

etf2_data = yf.download(f"{etf2}", period="5d", interval="1m", progress = False)
etf2_data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]


# startdate = "2024-07-23"
# enddate = "2024-07-25"
# etf1_data = yf.download(f"{etf1}", start=startdate, end=enddate, interval="1m", progress = False)
# etf1_data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]

# etf2_data = yf.download(f"{etf2}", start=startdate, end=enddate, interval="1m", progress = False)
# etf2_data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]

Combined_data = [etf1_data.Adj_Close, etf2_data.Adj_Close]
Combined_data = pd.DataFrame(Combined_data).transpose().dropna()
Combined_data.columns = [f"{etf1}", f"{etf2}"]
# print(Combined_data.describe())

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
# plt.show()
plt.savefig(f'./{today}/{indicator}/{etf1} and {etf2} over time.png') 
plt.close()

import matplotlib.pyplot as plt
plt.plot(Combined_data[f"{etf1}"],Combined_data[f"{etf2}"], '.')
plt.title(f"{etf1} vs. {etf2}")
# plt.show()
plt.savefig(f'./{today}/{indicator}/{etf1} vs. {etf2}.png') 
plt.close()

X = Combined_data[f"{etf1}"].to_numpy().reshape(-1, 1)
y = Combined_data[f"{etf2}"].to_numpy().reshape(-1, 1)

reg = LinearRegression().fit(X, y)

print(f"R-squared: {reg.score(X, y)}")

print(f"Linear Regression Slope/Coefficient: {reg.coef_}")

print(f"Linear Regression Intercept: {reg.intercept_}")

