"""APIAgent - Multi-agent skeleton for the Kaggle Agents Intensive capstone.

Usage:
    python agent/apia_agent.py

Notes:
- This script uses a hybrid data strategy: try Google Search (stub) -> fallback to sample CSV.
- Replace SearchTool.run() with ADK search tool in production.
- No API keys are included.
"""
import csv
import json
import time
from datetime import datetime
from pathlib import Path

from tools import GoogleSearchTool, CSVLoaderTool
from utils import simple_logger

# Minimal agent scaffolding for demonstration
class Agent:
    def __init__(self, name, tools=None, memory=None, logger=None):
        self.name = name
        self.tools = tools or {}
        self.memory = memory
        self.logger = logger or (lambda *a, **k: None)

    def call_tool(self, tool_name, *args, **kwargs):
        self.logger(f"[{self.name}] calling tool: {tool_name}")
        tool = self.tools.get(tool_name)
        if not tool:
            raise RuntimeError(f"Tool {tool_name} not found")
        return tool.run(*args, **kwargs)

class PlannerAgent(Agent):
    def handle(self, user_text, user_context):
        self.logger(f"Planner received: {user_text}")
        # Decide the flow based on user intent (very simple)
        return {"action": "fetch_data", "location": user_context.get("location", "Chennai")}

class DataAgent(Agent):
    def fetch(self, location):
        # Try Google Search tool first
        try:
            res = self.call_tool("google_search", f"{location} AQI today")
            parsed = parse_search_snippet(res.get("result_snippet", ""))
            if parsed:
                parsed["source"] = "google_search"
                parsed["timestamp"] = res.get("timestamp") or datetime.utcnow().isoformat()
                return parsed
            else:
                raise ValueError("Parsing failed")
        except Exception as e:
            self.logger("Google Search failed or parsing failed:", e)
            csv_res = self.call_tool("csv_loader", location)
            if isinstance(csv_res, dict) and csv_res.get("error"):
                return {"error": "no data available"}
            return {
                "pm25": float(csv_res["pm25"]),
                "pm10": float(csv_res["pm10"]),
                "aqi": int(csv_res.get("aqi", -1)),
                "timestamp": csv_res.get("date"),
                "source": "sample_csv"
            }

class AnalysisAgent(Agent):
    def analyze(self, datapoint, recent_series=None):
        result = {"trend": "stable", "anomaly": False, "confidence": 0.8}
        try:
            today_pm = float(datapoint.get("pm25", 0))
            if recent_series:
                past_vals = [float(x.get("pm25", 0)) for x in recent_series if x.get("pm25")!='']
                if len(past_vals):
                    past_avg = sum(past_vals)/len(past_vals)
                    if past_avg>0:
                        if today_pm > past_avg * 1.3:
                            result.update({"trend":"rising","anomaly":True})
                        elif today_pm < past_avg * 0.8:
                            result.update({"trend":"falling"})
                        else:
                            result.update({"trend":"stable"})
                        result["confidence"] = 0.9
            return result
        except Exception as e:
            self.logger("Analysis failed", e)
            return {"error":"analysis_error"}

class ExplanationAgent(Agent):
    def explain(self, datapoint, analysis, user_prefs=None):
        pm25 = datapoint.get("pm25")
        trend = analysis.get("trend")
        text = f"Current PM2.5 is {pm25} µg/m3. Trend: {trend}. "
        try:
            if pm25 and float(pm25) > 100:
                text += "Air quality is poor — avoid strenuous outdoor activity. If you have respiratory issues, use a mask."
            else:
                text += "Air quality is moderate; normal activities are OK."
        except Exception:
            text += "Unable to fully assess air quality."
        return {"summary": text, "confidence": analysis.get("confidence", 0.7)}

class AdvisoryAgent(Agent):
    def advise(self, explanation, user_prefs=None):
        advice = []
        s = explanation.get("summary","")

        if any(w in s.lower() for w in ["poor","avoid"]):
            advice.append("Avoid outdoor exercise today.")
            advice.append("Use N95 mask if you must go out.")
        else:
            advice.append("Good day for outdoor activities.")

        if user_prefs and user_prefs.get("asthma"):
            advice.append("Carry inhaler and avoid crowded roads.")

        return {"advice": advice}

# Utils
def parse_search_snippet(snippet:str):
    # Rudimentary parsing for demo; replace with robust regex/HTML parsing
    out = {}
    try:
        lowered = snippet.lower()
        if "pm2.5" in lowered or "pm2.5" in snippet or "pm2.5" in snippet.lower() or "pm2.5" in snippet:
            # fake parse values for skeleton; production code should parse numbers
            if "86" in snippet:
                out["pm25"] = 86.0
                out["pm10"] = 150.0
                out["aqi"] = 128
            else:
                # fallback synthetic
                out["pm25"] = 55.0
                out["pm10"] = 90.0
                out["aqi"] = 80
        return out
    except Exception:
        return {}

# Simple in-memory memory
class MemoryBank:
    def __init__(self):
        self.storage = {"queries":[], "preferences":{}}
    def save_query(self, q):
        self.storage["queries"].append(q)
    def set_pref(self, k, v):
        self.storage["preferences"][k] = v
    def get_pref(self, k, default=None):
        return self.storage["preferences"].get(k, default)

def main():
    # setup
    base = Path(__file__).resolve().parents[1]
    sample_csv = base / "data" / "sample_data.csv"

    mem = MemoryBank()
    tools = {
        "google_search": GoogleSearchTool(),
        "csv_loader": CSVLoaderTool(str(sample_csv))
    }

    planner = Agent("planner", tools=tools, memory=mem, logger=simple_logger)
    data_agent = Agent("data_agent", tools=tools, memory=mem, logger=simple_logger)
    analysis_agent = Agent("analysis_agent", tools=tools, memory=mem, logger=simple_logger)
    explain_agent = Agent("explain_agent", tools=tools, memory=mem, logger=simple_logger)
    adv_agent = Agent("advisory_agent", tools=tools, memory=mem, logger=simple_logger)

    # For clarity use dedicated classes for behaviors
    planner = PlannerAgent("planner", tools=tools, memory=mem, logger=simple_logger)
    data_agent = DataAgent("data_agent", tools=tools, memory=mem, logger=simple_logger)
    analysis_agent = AnalysisAgent("analysis_agent", tools=tools, memory=mem, logger=simple_logger)
    explain_agent = ExplanationAgent("explain_agent", tools=tools, memory=mem, logger=simple_logger)
    adv_agent = AdvisoryAgent("advisory_agent", tools=tools, memory=mem, logger=simple_logger)

    # User input simulation
    user_text = "What's Chennai AQI right now and can I run at 6am?"
    user_context = {"location":"Chennai","user_id":"dharshaa","preferences":{"asthma":False}}

    plan = planner.handle(user_text, user_context)
    mem.save_query({"user_text": user_text, "time": time.time(), "location": user_context["location"]})

    # Fetch data
    dp = data_agent.fetch(plan["location"])
    if not dp or dp.get("error"):
        simple_logger("Data fetch error:", dp)
        return

    # get recent series for trend detection
    recent_series = []
    try:
        with open(sample_csv, 'r') as f:
            reader = list(csv.DictReader(f))
            recent = [r for r in reader if r.get("location","").lower()==plan["location"].lower()]
            recent_series = recent[-7:]
    except Exception:
        recent_series = None

    analysis = analysis_agent.analyze(dp, recent_series=recent_series)
    explanation = explain_agent.explain(dp, analysis, user_prefs=user_context["preferences"])
    advice = adv_agent.advise(explanation, user_prefs=user_context["preferences"])

    mem.save_query({"location": plan["location"], "data": dp, "analysis":analysis, "time": time.time()})

    response = {
        "location": plan["location"],
        "data": dp,
        "analysis": analysis,
        "explanation": explanation,
        "advice": advice
    }

    print(json.dumps(response, indent=2, default=str))

if __name__ == '__main__':
    main()
