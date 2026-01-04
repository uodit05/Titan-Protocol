import argparse
from src.config import config

def main():
    parser = argparse.ArgumentParser(description="Titan Protocol: Automated Fundamental Analysis")
    parser.add_argument("query", type=str, help="Investment theme or query")
    args = parser.parse_args()
    
    print(f"Titan Protocol Initialized.")
    print(f"Processing Query: {args.query}")
    
    # Pipeline Implementation
    
    # 1. Discovery
    from src.stages.discovery import ThemeHunter
    hunter = ThemeHunter()
    tickers = hunter.run(args.query)
    
    if not tickers:
        print("No tickers found. Exiting.")
        return

    # 2. Triage
    from src.stages.triage import Prism
    prism = Prism()
    passed_tickers = prism.run(tickers)
    
    if not passed_tickers:
        print("No tickers passed triage. Exiting.")
        return

    # 3. Judgment
    from src.stages.judgment import Tribunal
    tribunal = Tribunal()
    verdicts = []
    
    for ticker in passed_tickers:
        verdict = tribunal.run(ticker)
        verdicts.append(verdict)

    # 4. Construction
    from src.stages.construction import CIO
    cio = CIO()
    cio.generate_report(verdicts)
