# APIAgent — Air Pollution Insight Agent (Agents for Good)

**Project**: Air Pollution Insight Agent (APIAgent)  
**Track**: Agents for Good — Kaggle/Google Agents Intensive Capstone  
**Author**: Dharshaa

## Overview
APIAgent is a multi-agent system that fetches air quality data, analyzes trends and anomalies, and provides plain-language health & activity recommendations. It uses a hybrid data strategy: try Google Search at runtime, fall back to a sample CSV dataset.

## Features
- Multi-agent orchestration (Planner, Data, Analysis, Explanation, Advisory)
- Tool usage: Google Search (runtime) and local CSV fallback
- Session & Long-term memory support
- Observability: structured logs and metrics
- Simple anomaly detection & trend analysis
- Personalization using user preferences

## How to run (local)
1. Clone repository
2. Create a virtual env:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
