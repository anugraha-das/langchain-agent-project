from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI()

# -----------------------------
# Structured Memory
# -----------------------------
memory = {
    "research": [],
    "analysis": [],
    "summary": []
}

def is_duplicate(text, category):
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

                if not is_duplicate(v, "research"):
                    memory["research"].append(v)

            output += section + "\n"

    if not output:
        return "Information not found."

    return output.strip()

#---ANALYSIS AGENT----

def analysis_agent(research):

    if "not found" in research.lower():
        return research

    sections = research.split("\n\n")  # split concepts
    final_analysis = ""

    for sec in sections:
        if not sec.strip():
            continue

        lines = sec.split("\n")
        title = lines[0]   # LANGCHAIN:

        final_analysis += title + "\nAnalysis:\n"

        for l in lines[1:]:
            if "•" in l:
                text = l.replace("• ", "")
                final_analysis += f"- This explains that {text.lower()}.\n"

                if text not in memory["analysis"]:
                    memory["analysis"].append(text)

        final_analysis += "\n"

    return final_analysis.strip()

#----SUMMARIZER AGENT---

def summary_agent(analysis):

    if "not found" in analysis.lower():
        return analysis

    sections = analysis.split("\n\n")
    final_summary = ""

    for sec in sections:
        if not sec.strip():
            continue

        lines = sec.split("\n")
        title = lines[0]   # LANGCHAIN:

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

    analysis_sections = analysis.split("\n\n")
    summary_sections = summary.split("\n\n")

    email_body = "Subject: AI Concept Summary\n\nDear User,\n\n"

    for a_sec, s_sec in zip(analysis_sections, summary_sections):

        if not a_sec.strip() or not s_sec.strip():
            continue

        # Get title (LANGCHAIN, etc.)
        title = a_sec.split("\n")[0]

        email_body += f"{title}\n"

        # Add Analysis
        for line in a_sec.split("\n")[1:]:
            email_body += line + "\n"

        # Add Summary
        for line in s_sec.split("\n")[1:]:
            email_body += line + "\n"

        email_body += "\n"

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
        return JSONResponse({
            "research": "Empty input",
            "analysis": "",
            "summary": "",
            "email": "",
            "memory": memory
        })

    research = research_agent(query)
    analysis = analysis_agent(research)
    summary = summary_agent(analysis)
    email = email_agent(analysis, summary)

    return JSONResponse({
        "research": research,
        "analysis": analysis,
        "summary": summary,
        "email": email,
        "memory": memory
    })