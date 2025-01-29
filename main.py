import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from func import (
    StockAnalyzer,
    StockComparison,
    RiskAnalysis,
    InvestmentAdvisor,
    DisplayRecommendation
)

# ---- Streamlit UI ----
# Custom CSS for Vibrant UI
st.markdown(
    """
    <style>
        body {
            background-color: #0E1117;
            color: white;
        }
        .stTextInput, .stSelectbox, .stButton > button {
            border-radius: 10px;
            font-size: 16px;
        }
        .stButton > button {
            background: linear-gradient(90deg, #1DB954, #1A73E8);
            color: white;
            padding: 10px;
            border: none;
            border-radius: 10px;
            transition: 0.3s ease-in-out;
        }
        .stButton > button:hover {
            transform: scale(1.05);
            background: linear-gradient(90deg, #1A73E8, #1DB954);
        }
        .report-box {
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 15px rgba(0, 255, 255, 0.3);
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🚀 AI-Powered Stock Analysis & Investment Advisor")

st.sidebar.header("🔍 Stock Selection")
stock1 = st.sidebar.text_input("Enter Stock Symbol 1 (e.g., AAPL):", "AAPL").upper()
stock2 = st.sidebar.text_input("Enter Stock Symbol 2 (e.g., MSFT):", "MSFT").upper()
period = st.sidebar.selectbox("Select Historical Data Range:", ["1mo", "3mo", "6mo", "1y", "5y"])

# Run Analysis Button
if st.sidebar.button("📊 Generate Report"):
    # Initialize agents
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

    # ---- Display Stock Comparison ----
    st.subheader("📊 Stock Comparison")
    comparison_df = pd.DataFrame({
        "Stock": [stock1, stock2],
        "Latest Price": [
            stock1_data["Close"].iloc[-1] if not stock1_data.empty else "N/A",
            stock2_data["Close"].iloc[-1] if not stock2_data.empty else "N/A",
        ]
    })
    st.table(comparison_df)

    # ---- Display Risk Analysis ----
    st.subheader("📉 Risk & Volatility Analysis")
    fig_risk = risk_agent.display_risk_analysis(stock1, stock2, stock1_data, stock2_data)
    st.pyplot(fig_risk)

    # ---- Investment Advice ----
    st.subheader("📝 Investment Advice")
    investment_advice = advisor_agent.generate_investment_advice(
        stock1, stock2, stock1_data, stock2_data, stock1_metrics, stock2_metrics
    )
    st.markdown(f"<div class='report-box'>{investment_advice}</div>", unsafe_allow_html=True)


    # ---- Display Recommendation Chart ----
    st.subheader("📈 Stock Price Comparison")
    fig_recommendation = display_agent.display_recommendation_charts(stock1, stock2, stock1_data, stock2_data)
    st.pyplot(fig_recommendation)
# ---- Report Completed Section ----
    st.divider()
    st.markdown(
        """
        <div style='text-align: center; margin-top: 30px;'>
            <h2 style='color: #4CAF50;'>🎉 Report Completed 🎉</h2>
            <p style='font-size: 18px;'>Thank you for using our analysis tool! 📊</p>
        </div>
        """, 
        unsafe_allow_html=True
    )