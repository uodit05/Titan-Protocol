import yfinance as yf
from src.config import config
import requests

class FinanceTool:
    def __init__(self):
        self.fmp_key = config.FMP_API_KEY

    def get_metrics(self, ticker: str) -> dict:
        """
        Fetches basic metrics: P/E, Debt/Equity, FCF.
        Uses yfinance as primary, could fallback to FMP.
        """
        # Append .NS for Indian stocks if not present (heuristic)
        # In a real app, we'd handle exchanges more robustly.
        if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
             # Simple heuristic: try .NS first for Indian context
             ticker_ns = f"{ticker}.NS"
        else:
            ticker_ns = ticker

        try:
            stock = yf.Ticker(ticker_ns)
            info = stock.info
            
            # Safe extraction
            pe = info.get('trailingPE', 0)
            debt_to_equity = info.get('debtToEquity', 0)
            
            # FCF approximation (Operating Cash Flow - CapEx)
            # yfinance often has this in 'freeCashflow'
            fcf = info.get('freeCashflow', 0)
            
            return {
                "ticker": ticker,
                "pe": pe,
                "debt_to_equity": debt_to_equity,
                "fcf": fcf,
                "market_cap": info.get('marketCap', 0)
            }
        except Exception as e:
            print(f"Error fetching metrics for {ticker}: {e}")
            return {}

    def get_news(self, ticker: str) -> list[str]:
        """
        Fetches recent news for narrative analysis.
        """
        if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
             ticker_ns = f"{ticker}.NS"
        else:
            ticker_ns = ticker
            
        try:
            stock = yf.Ticker(ticker_ns)
            news = stock.news
            return [n['title'] for n in news]
        except Exception as e:
            print(f"Error fetching news for {ticker}: {e}")
            return []

finance_tool = FinanceTool()
