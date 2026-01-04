import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import pandas as pd

# Mock external dependencies
sys.modules['google'] = MagicMock()
sys.modules['google.generativeai'] = MagicMock()
sys.modules['yfinance'] = MagicMock()
sys.modules['exa_py'] = MagicMock()
sys.modules['chromadb'] = MagicMock()
sys.modules['rich'] = MagicMock()
sys.modules['rich.console'] = MagicMock()
sys.modules['rich.table'] = MagicMock()
sys.modules['rich.markdown'] = MagicMock()
sys.modules['dotenv'] = MagicMock()

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.agents.librarian import Librarian
from src.tools.finance import FinanceTool

class TestDeepResearch(unittest.TestCase):
    
    @patch('src.core.llm.llm_client.generate')
    def test_librarian_pandas_analysis(self, mock_llm):
        print("\n--- Testing Librarian Pandas Analysis ---")
        
        # 1. Setup Mock DataFrames
        data = {'Revenue': [100, 110, 121]}
        income_stmt = pd.DataFrame(data, index=[2020, 2021, 2022])
        
        dfs = {
            "income_stmt": income_stmt,
            "balance_sheet": None,
            "cash_flow": None
        }
        
        # 2. Mock LLM to return valid pandas code
        # The prompt asks for code to answer the directive.
        # Let's say directive is "Calculate average revenue"
        mock_llm.return_value = "income_stmt['Revenue'].mean()"
        
        # 3. Test Librarian
        lib = Librarian()
        result = lib.analyze_data("Calculate average revenue", dfs)
        
        print(f"Librarian Result: {result}")
        self.assertEqual(float(result), 110.33333333333333)
        print("Pandas Analysis: Passed")

    @patch('src.tools.finance.yf.Ticker')
    def test_finance_tool_full_financials(self, mock_ticker):
        print("\n--- Testing Finance Tool Full Financials ---")
        
        # Mock yfinance ticker object
        mock_stock = MagicMock()
        mock_stock.financials = pd.DataFrame({'2022': [100]}, index=['Revenue'])
        mock_stock.balance_sheet = pd.DataFrame({'2022': [50]}, index=['Assets'])
        mock_stock.cashflow = pd.DataFrame({'2022': [10]}, index=['Operating Cash Flow'])
        
        mock_ticker.return_value = mock_stock
        
        ft = FinanceTool()
        financials = ft.get_financials("TEST")
        
        self.assertIsNotNone(financials['income_stmt'])
        self.assertIsNotNone(financials['balance_sheet'])
        self.assertIsNotNone(financials['cash_flow'])
        print("Finance Tool Fetch: Passed")

if __name__ == '__main__':
    unittest.main()
