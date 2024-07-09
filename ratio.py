import yfinance as yf
from ta import add_all_ta_features
import pandas as pd
import statsmodels.api as sm
for i in range (len(list)):
    stock, cdr = list.iloc[i].tolist()
    cdr_data = yf.download(f"{cdr}", period="5d", interval="1m", progress=False)
    stock_data = yf.download(f"{stock}", period="5d", interval="1m", progress=False)
    combined_data = pd.concat([stock_data.High, cdr_data.High], axis=1).dropna()
    combined_data.columns = ['stock_high','cdr_high']
    # Add a constant to the independent variable to include the intercept in the model
    X = sm.add_constant(combined_data['cdr_high'])
    
    # Fit the model
    model = sm.OLS(combined_data['stock_high'], X).fit()
    
    # Get the coefficients
    intercept, slope = model.params
    print(f"ratio of {stock} is {slope}")
