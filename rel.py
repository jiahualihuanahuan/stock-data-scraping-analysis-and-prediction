import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
import sys
from datetime import date
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot
"""
relationship
python rel.py EMAX.TO ENCC.TO
python rel.py EMAX.TO CL=F
python rel.py XLE CL=F
python rel.py XLE CL=F

"""

etf1 = sys.argv[1]
etf2 = sys.argv[2]

# list_ = pd.read_csv(f"https://raw.githubusercontent.com/jiahualihuanahuan/stock-data-scraping-analysis-and-prediction/main/{etf_name}.csv", encoding='latin-1')
# list_.columns = ["Symbol"]

indicator = "relationship"
today = date.today()
if not os.path.exists(f'./{today}/{indicator}'):
   os.makedirs(f'./{today}/{indicator}')

relationship = []

try:
   print(f"calculating relationship between {etf1} and {etf2}...")
   etf1_data = yf.download(f"{etf1}", period="max", interval="1d", progress = False)
   etf1_data.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]

   etf2_data = yf.download(f"{etf2}", period="max", interval="1d", progress = False)
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

   # relationship.append([f"{etf1}", f"{etf2}", f"{reg.score(X, y)}", f"{reg.coef_}", f"{reg.intercept_}"])
except:
   pass

# relationship_df = pd.DataFrame(relationship)
# relationship_df.columns = ["Symbol_1","Symbol_2","R-squared","Linear Regression Slope","Linear Regression Intercept"]
# print(relationship_df.sort_values(by="R-squared"))

# today = date.today()
# if not os.path.exists(f'./{today}/{indicator}'):
#    os.makedirs(f'./{today}/{indicator}')
# relationship_df.sort_values(by="R-squared").to_csv(f"./{today}/{indicator}/relationship of {etf_name}.csv")