"""
MIT License
Copyright (c) 2025 Vidzai Digital
Full license text available in the LICENSE file.
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
import uvicorn

app = FastAPI()

# -----------------------------
# Structured Memory (Cumulative)
# -----------------------------
memory = {
    "research": [],
    "analysis": [],
    "summary": [],
    "sent_emails": [] 
}

def is_duplicate(text, category):
    """Checks if the fact already exists in the shared memory."""
    return text.lower().strip() in [x.lower().strip() for x in memory[category]]

# -----------------------------
# Research Agent
# -----------------------------
def research_agent(query):
    knowledge = {
        "langchain": [
            "LangChain is a framework for building LLM applications",
            "Supports chains, agents, and memory"
        ],
        "shared memory": [
            "Shared memory allows reuse of information",
            "Accessible by all agents"
        ],
        "multi agent": [
            "Multiple agents work together",
            "Each has a specific role"
        ]
    }
    output = ""
    for key, val in knowledge.items():
        if key in query.lower():
            section = key.upper() + ":\n"
            for v in val:
                section += "• " + v + "\n"
                # Add to memory if not already there
                if not is_duplicate(v, "research"):
                    memory["research"].append(v)
            output += section + "\n"
    
    return output.strip() if output else "Information not found."

# -----------------------------
# Analysis Agent
# -----------------------------
def analysis_agent(research):
    if "not found" in research.lower():
        return research
    
    sections = research.split("\n\n")
    final_analysis = ""
    for sec in sections:
        if not sec.strip(): continue
        lines = sec.split("\n")
        title = lines[0]
        final_analysis += title + "\nAnalysis:\n"
        for l in lines[1:]:
            if "•" in l:
                text = l.replace("• ", "")
                final_analysis += f"- This explains that {text.lower()}.\n"
                if text not in memory["analysis"]:
                    memory["analysis"].append(text)
        final_analysis += "\n"
    return final_analysis.strip()

# -----------------------------
# Summarizer Agent
# -----------------------------
def summary_agent(analysis):
    if "not found" in analysis.lower():
        return analysis
    
    sections = analysis.split("\n\n")
    final_summary = ""
    for sec in sections:
        if not sec.strip(): continue
        lines = sec.split("\n")
        title = lines[0]
        final_summary += title + "\nSummary:\n"
        for l in lines:
            if l.startswith("-"):
                clean = l.replace("- This explains that ", "")
                final_summary += f"- {clean}\n"
                if clean not in memory["summary"]:
                    memory["summary"].append(clean)
        final_summary += "\n"
    return final_summary.strip()

# -----------------------------
# Email Agent
# -----------------------------
def email_agent(analysis, summary):
    if "not found" in analysis.lower():
        return "Information not found."
    
    email_body = "Subject: AI Concept Summary\n\nDear User,\n\n"
    email_body += f"Technical Analysis:\n{analysis}\n\n"
    email_body += f"Final Summary:\n{summary}\n\n"
    email_body += "Regards,\nAI Assistant"
    return email_body

# -----------------------------
# Routes
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

@app.post("/process")
async def process(request: Request):
    data = await request.json()
    query = data.get("query", "")
    
    if not query.strip():
        return JSONResponse({"research": "Empty input", "analysis": "", "summary": "", "email": "", "memory": memory})
    
    # Run Agents sequentially
    research = research_agent(query)
    analysis = analysis_agent(research)
    summary = summary_agent(analysis)
    email = email_agent(analysis, summary)

    return JSONResponse({
        "research": research,
        "analysis": analysis,
        "summary": summary,
        "email": email,
        "memory": memory # Memory grows over time (Cumulative)
    })

@app.post("/send-mock")
async def send_mock(request: Request):
    """Mock tool to simulate sending the email after user confirmation."""
    data = await request.json()
    email_content = data.get("email", "")
    memory["sent_emails"].append(email_content)
    return JSONResponse({"status": "Success", "message": "Email sent successfully (Mock Mode)!"})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

 # Final Version: Multi-Agent System with Shared Memory
