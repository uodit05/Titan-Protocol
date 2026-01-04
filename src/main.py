import argparse
import sys
import os

# Add project root to sys.path to allow running as script
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
    import concurrent.futures
    
    tribunal = Tribunal()
    verdicts = []
    
    print(f"Starting Tribunal for {len(passed_tickers)} tickers in parallel...")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_ticker = {executor.submit(tribunal.run, ticker): ticker for ticker in passed_tickers}
        for future in concurrent.futures.as_completed(future_to_ticker):
            ticker = future_to_ticker[future]
            try:
                verdict = future.result()
                verdicts.append(verdict)
            except Exception as exc:
                print(f'{ticker} generated an exception: {exc}')

    # 4. Construction
    from src.stages.construction import CIO
    cio = CIO()
    cio.generate_report(verdicts)

if __name__ == "__main__":
    main()
