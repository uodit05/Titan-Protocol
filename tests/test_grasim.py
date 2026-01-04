import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add src to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.stages.discovery import ThemeHunter
from src.stages.triage import Prism
from src.stages.judgment import Tribunal
from src.stages.construction import CIO

class TestTitanProtocol(unittest.TestCase):
    
    @patch('src.core.llm.llm_client.generate')
    @patch('src.tools.search.search_tool.search')
    @patch('src.tools.finance.finance_tool.get_metrics')
    @patch('src.tools.finance.finance_tool.get_news')
    def test_grasim_scenario(self, mock_news, mock_metrics, mock_search, mock_llm):
        print("\n--- Starting Grasim Scenario Test ---")
        
        # 1. Setup Mocks
        
        # Discovery Mocks
        mock_llm.side_effect = [
            # Theme Hunter: Expand Query
            "['Indian conglomerates entering new business lines']", 
            # Theme Hunter: Extract Tickers
            "['GRASIM', 'RELIANCE']",
            # Prism: Narrative Analysis (Grasim)
            "PASSED",
            # Prism: Narrative Analysis (Reliance)
            "PASSED",
            # Tribunal Loop 1: Bull
            "Bull argument: Paints entry is huge.",
            # Tribunal Loop 1: Bear
            "Bear argument: High P/E.",
            # Tribunal Loop 1: Judge (Conflict)
            '{"score": 40, "directive": "Calculate sum-of-parts"}',
            # Tribunal Loop 2: Bull
            "Bull: Valuation is cheap if you strip out holdings.",
            # Tribunal Loop 2: Bear
            "Bear: Execution risk remains.",
            # Tribunal Loop 2: Judge (Consensus)
            '{"score": 92, "verdict": "Strong Buy. Hidden Asset Play."}'
        ]
        
        mock_search.return_value = [MagicMock(title="Grasim enters paints", url="url")]
        
        mock_metrics.return_value = {
            "ticker": "GRASIM",
            "pe": 85,
            "debt_to_equity": 1.5,
            "fcf": -5000
        }
        
        mock_news.return_value = ["Birla Opus Launch", "Aggressive CAPEX"]

        # 2. Run Pipeline Steps
        
        # Discovery
        hunter = ThemeHunter()
        tickers = hunter.run("Find me an undervalued Indian giant")
        self.assertIn("GRASIM", tickers)
        print("Discovery Stage: Passed")
        
        # Triage
        prism = Prism()
        passed = prism.run(tickers)
        self.assertIn("GRASIM", passed)
        print("Triage Stage: Passed")
        
        # Judgment
        tribunal = Tribunal()
        verdict = tribunal.run("GRASIM")
        self.assertEqual(verdict['score'], 92)
        self.assertIn("Strong Buy", verdict['verdict'])
        print("Judgment Stage: Passed")
        
        # Construction
        cio = CIO()
        cio.generate_report([verdict])
        print("Construction Stage: Passed")

if __name__ == '__main__':
    unittest.main()
