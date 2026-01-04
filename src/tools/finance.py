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
            news_items = []
            for n in news:
                title = n.get('title')
                if not title and 'content' in n:
                    title = n['content'].get('title')
                if title:
                    news_items.append(title)
            return news_items
        except Exception as e:
            print(f"Error fetching news for {ticker}: {e}")
            return []

    def get_financials(self, ticker: str) -> dict:
        """
        Fetches full historical financial data: Income Stmt, Balance Sheet, Cash Flow.
        Returns a dict of cleaned pandas DataFrames.
        """
        if not ticker.endswith(".NS") and not ticker.endswith(".BO"):
             ticker_ns = f"{ticker}.NS"
        else:
            ticker_ns = ticker
            
        try:
            stock = yf.Ticker(ticker_ns)
            
            # Fetch data
            income_stmt = stock.financials
            balance_sheet = stock.balance_sheet
            cash_flow = stock.cashflow
            
            # Clean data (fill NaNs with 0 for calculation safety)
            # Transpose so that years are rows and metrics are columns (easier for pandas analysis)
            financials = {
                "income_stmt": income_stmt.T.fillna(0) if not income_stmt.empty else None,
                "balance_sheet": balance_sheet.T.fillna(0) if not balance_sheet.empty else None,
                "cash_flow": cash_flow.T.fillna(0) if not cash_flow.empty else None
            }
            return financials
        except Exception as e:
            print(f"Error fetching financials for {ticker}: {e}")
            return {}

finance_tool = FinanceTool()
