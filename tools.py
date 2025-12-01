"""Tools used by APIAgent.
- GoogleSearchTool: stub that simulates a search result. Replace with ADK search tool for production.
- CSVLoaderTool: loads latest row for a location from CSV.
"""
import csv
from datetime import datetime
from pathlib import Path

class GoogleSearchTool:
    def __init__(self):
        self.name = "google_search"

    def run(self, query: str):
        # Stubbed response. In production, replace with ADK Search tool or official API.
        snippet = f"AQI {query.split()[0]}: 128 (Unhealthy for sensitive groups). PM2.5: 86 µg/m3. Source: example.com"
        return {
            "query": query,
            "timestamp": datetime.utcnow().isoformat(),
            "result_snippet": snippet,
            "raw_html": "<html>...</html>"
        }

class CSVLoaderTool:
    def __init__(self, csv_path):
        self.csv_path = Path(csv_path)

    def run(self, location: str):
        if not self.csv_path.exists():
            return {"error": "sample data missing", "path": str(self.csv_path)}
        latest = None
        with open(self.csv_path, 'r') as f:
            reader = list(csv.DictReader(f))
            for row in reader:
                if row.get('location','').lower() == location.lower():
                    latest = row
        if latest:
            return latest
        return {"error": "no data for location"}
