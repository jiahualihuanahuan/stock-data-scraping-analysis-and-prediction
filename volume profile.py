# download data
import yfinance as yf
# df = yf.download("TSLA", period="7d", interval="1m")
df = yf.download("YTSL.NE", period="7d", interval="1m")
df.columns = ["Open", "High", "Low", "Close", "Adj_Close", "Volume"]

# plot candlestick 
import plotly.graph_objects as go

fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Adj_Close'])])

fig.show()

import plotly.express as px

px.histogram(df, x='Volume', y='Adj_Close', nbins=20, orientation='h').show()
