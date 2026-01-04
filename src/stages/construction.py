from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

class CIO:
    def __init__(self):
        self.console = Console()

    def generate_report(self, verdicts: list[dict]):
        """
        Aggregates verdicts and prints a beautiful report.
        """
        # Sort by score descending
        sorted_verdicts = sorted(verdicts, key=lambda x: x.get('score', 0), reverse=True)
        
        self.console.print("\n[bold gold1]THE TITAN PROTOCOL - FINAL REPORT[/bold gold1]", justify="center")
        self.console.print("="*60, justify="center")
        
        table = Table(title="Investment Candidates")
        table.add_column("Ticker", style="cyan", no_wrap=True)
        table.add_column("Verdict", style="magenta")
        table.add_column("Score", justify="right", style="green")
        table.add_column("Reasoning", style="white")
        
        for v in sorted_verdicts:
            ticker = v['ticker']
            verdict = v.get('verdict', 'N/A')
            score = str(v.get('score', 0))
            # Extract a brief reason from the history or verdict
            # For now, just taking the verdict text itself as it usually contains the reason
            reason = verdict 
            
            table.add_row(ticker, verdict, score, reason)
            
        self.console.print(table)
        
        # Detailed Drill-down
        for v in sorted_verdicts:
            if v.get('score', 0) > 80:
                self.console.print(f"\n[bold cyan]Detailed Analysis: {v['ticker']}[/bold cyan]")
                self.console.print("-" * 40)
                # Print the last few turns of the debate
                history = v.get('history', [])
                for h in history[-3:]:
                    self.console.print(h)
