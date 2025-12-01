# APIAgent — Air Pollution Insight Agent (Agents for Good)

**Project**: APIAgent — Air Pollution Insight Agent  
**Track**: Agents for Good — Kaggle/Google Agents Intensive Capstone  
**Author**: Dharshaa

## Overview
APIAgent is a multi-agent system that fetches air quality data (live Google Search if available, otherwise a local CSV fallback), analyzes short-term trends and anomalies, and provides clear, personalized health and activity recommendations.

## Repository structure
```
.
├── apia_agent.py          # Main agent runtime script
├── tools.py              # Tool wrappers (Search stub / CSV loader)
└── utils.py              # Utility functions
└── sample_data.csv       # Fallback sample dataset
├── requirements.txt
├── LICENSE
└── README.md
```

## How to run (local)
1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate    # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```
2. Run the agent (uses Google Search stub by default; falls back to CSV):
   ```bash
   python apia_agent.py
   ```

## Notes
- The Google Search tool is implemented as a stub for portability. Replace the stub with the ADK Search tool or integrate official APIs when deploying.
- Do NOT commit API keys. Use environment variables or secret managers for deployment.

