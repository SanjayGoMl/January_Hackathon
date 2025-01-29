import os
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

# Load environment variables
load_dotenv()

# Set API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class StockAnalyzer:
    def __init__(self):
        self.role = "Stock Analyst"

    def fetch_stock_data(self, stock_symbol, period="1mo"):
        """Fetch historical stock data from YFinance."""
        stock = yf.Ticker(stock_symbol)
        return stock.history(period=period)

    def get_stock_metrics(self, stock_symbol):
        """Get stock valuation metrics like P/E and P/B ratio."""
        stock = yf.Ticker(stock_symbol)
        info = stock.info
        return {
            "P/E Ratio": info.get("trailingPE", "N/A"),
            "P/B Ratio": info.get("priceToBook", "N/A"),
            "Market Cap": info.get("marketCap", "N/A"),
        }

class StockComparison:
    def display_comparison(self, stock1, stock2, stock1_data, stock2_data):
        """Display stock prices in tabular format."""
        data = {
            "Stock": [stock1, stock2],
            "Latest Price": [
                stock1_data["Close"].iloc[-1] if not stock1_data.empty else "N/A",
                stock2_data["Close"].iloc[-1] if not stock2_data.empty else "N/A",
            ],
        }
        df = pd.DataFrame(data)
        print("\nStock Comparison Table")
        print(df.to_string(index=False))

class RiskAnalysis:
    def display_risk_analysis(self, stock1, stock2, stock1_data, stock2_data):
        """Visualize stock risks using bar charts."""
        volatilities = [
            stock1_data["Close"].pct_change().std() if not stock1_data.empty else 0,
            stock2_data["Close"].pct_change().std() if not stock2_data.empty else 0,
        ]
        fig, ax = plt.subplots()
        ax.bar([stock1, stock2], volatilities, color=['blue', 'orange'])
        ax.set_title('Stock Volatility Analysis')
        ax.set_ylabel('Volatility (Standard Deviation)')
        return fig

class DisplayRecommendation:
    def display_recommendation_charts(self, stock1, stock2, stock1_data, stock2_data):
        """Display stock data as charts."""
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.plot(stock1_data.index, stock1_data['Close'], label=stock1, color='blue')
        ax.plot(stock2_data.index, stock2_data['Close'], label=stock2, color='orange')
        ax.set_title('Stock Price Comparison')
        ax.set_xlabel('Date')
        ax.set_ylabel('Closing Price')
        ax.legend()
        return fig


class InvestmentAdvisor:
    def __init__(self):
        self.llm = ChatOpenAI(model_name="gpt-4", openai_api_key=OPENAI_API_KEY)

    def generate_investment_advice(self, stock1, stock2, stock1_data, stock2_data, stock1_metrics, stock2_metrics):
        stock1_price = stock1_data["Close"].iloc[-1] if not stock1_data.empty else "N/A"
        stock2_price = stock2_data["Close"].iloc[-1] if not stock2_data.empty else "N/A"

        messages = [
            SystemMessage(content="You are a financial analyst providing investment advice."),
            HumanMessage(content=f"""
                Compare the two stocks {stock1} and {stock2} based on:
                - {stock1} Current Price: ${stock1_price}
                - {stock2} Current Price: ${stock2_price}
                - {stock1} P/E Ratio: {stock1_metrics['P/E Ratio']}
                - {stock2} P/E Ratio: {stock2_metrics['P/E Ratio']}
                - {stock1} P/B Ratio: {stock1_metrics['P/B Ratio']}
                - {stock2} P/B Ratio: {stock2_metrics['P/B Ratio']}
                Provide a detailed investment recommendation.
            """),
        ]

        response = self.llm(messages)
        print("\nInvestment Advice:\n")
        return response.content


# Main Execution
if __name__ == "__main__":
    stock1 = "AAPL"
    stock2 = "MSFT"
    period = "1mo"

    analyzer = StockAnalyzer()
    comparison_agent = StockComparison()
    risk_agent = RiskAnalysis()
    advisor_agent = InvestmentAdvisor()
    display_agent = DisplayRecommendation()

    # Fetch stock data
    stock1_data = analyzer.fetch_stock_data(stock1, period)
    stock2_data = analyzer.fetch_stock_data(stock2, period)

    # Fetch stock valuation metrics
    stock1_metrics = analyzer.get_stock_metrics(stock1)
    stock2_metrics = analyzer.get_stock_metrics(stock2)

    # Display comparison table
    comparison_agent.display_comparison(stock1, stock2, stock1_data, stock2_data)
    risk_agent.display_risk_analysis(stock1, stock2, stock1_data, stock2_data)
    advisor_agent.generate_investment_advice(stock1, stock2, stock1_data, stock2_data, stock1_metrics, stock2_metrics)
    display_agent.display_recommendation_charts(stock1, stock2, stock1_data, stock2_data)
