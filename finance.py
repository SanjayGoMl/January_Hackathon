import yfinance as yf

# Fetch AMZN stock data
amzn = yf.Ticker("AMZN")
data = amzn.history(period="5y") 
monthly_data = data['Close'].resample('M').last()
print(monthly_data)
