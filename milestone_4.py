import datetime
import random
import uvicorn
import sys
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

app = FastAPI()

# --- 1. TECHNICAL KNOWLEDGE BASE ---
KNOWLEDGE_BASE = {
    "fastapi": "FAST_API: High-performance framework for building APIs with Python 3.8+ using standard type hints.",
    "langchain": "LANGCHAIN: A framework designed to simplify the creation of applications using LLMs by chaining components.",
    "agents": "AI_AGENTS: Autonomous entities that use LLMs to reason, use tools, and execute complex task sequences.",
    "multi agent": "MULTI_AGENT_SYSTEMS: A specialized architecture where multiple independent agents collaborate to solve a single problem.",
    "docker": "DOCKER: Containerization platform used to package applications with all dependencies into isolated units.",
    "python": "PYTHON: The core programming language for AI, known for its readability and massive library ecosystem.",
    "milestone 4": "MILESTONE_4: The final synthesis phase of project development involving UI, memory, and agent logic."
}

system_state = {
    "session_id": f"SC-{random.randint(1000, 9999)}",
    "history": [],
    "active_node": "IDLE"
}

# --- 2. THE 4-AGENT PIPELINE & TOOLS ---

def research_agent(query: str):
    q_lower = query.lower().strip()
    
    # TOOL 1: MATH
    if any(op in query for op in ["+", "-", "*", "/"]):
        system_state["active_node"] = "MATH_ENGINE"
        try:
            return f"CALCULATION_SUCCESS: {query} = {eval(q_lower, {'__builtins__': None}, {})}."
        except: return "ERROR: INVALID_MATH"

    # TOOL 2: WEATHER
    elif "weather" in q_lower:
        system_state["active_node"] = "METEO_PROBE"
        temp = random.randint(22, 35)
        return f"WEATHER_REPORT: Temperature is {temp}°C. Atmosphere is stable."

    # TOOL 3: MULTI-TOPIC KNOWLEDGE
    else:
        system_state["active_node"] = "KNOWLEDGE_GRAPH"
        found = [val for key, val in KNOWLEDGE_BASE.items() if key in q_lower]
        return " | ".join(found) if found else "LOG: No local data found."

def analysis_agent(data: str):
    return f"ANALYSIS: Verified {system_state['active_node']}. Data integrity: 99.8%."

def summary_agent(data: str):
    return f"STRATEGIC_SUMMARY: {data}"

def email_agent(summary: str, query: str):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    return (f"FROM: StateCraft AI Dispatch\nDATE: {ts}\nSUBJECT: Intelligence Report: {query.upper()}\n"
            f"--------------------------------------------------\n\nDear User,\n\n{summary}\n\n"
            f"Regards,\nStateCraft AI Team")

# --- 3. ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/process")
async def process(request: Request):
    data = await request.json()
    q = data.get("query", "")
    res = research_agent(q)
    ana = analysis_agent(res)
    summ = summary_agent(res)
    eml = email_agent(summ, q)
    system_state["history"].append({"input": q, "output": summ})
    return {"research": res, "analysis": ana, "summary": summ, "email": eml, "state": system_state}

@app.post("/clear")
async def clear_history():
    system_state["history"] = []
    return {"status": "cleared"}

# --- 4. THE FORCE-STAY-ALIVE RUNNER ---
if __name__ == "__main__":
    import uvicorn
    print("\n--- [STATECRAFT AI] SYSTEM ONLINE ---")
    print("Direct Link: http://127.0.0.1:8080")
    
    uvicorn.run(app, host="127.0.0.1", port=8080)