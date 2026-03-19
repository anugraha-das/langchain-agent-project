from langchain.memory import ConversationBufferMemory

# -----------------------------
# Shared Memory
# -----------------------------
shared_memory = []

# -----------------------------
# Helper function to remove duplicates
# -----------------------------
def is_duplicate(text):
    clean_text = text.strip().lower().rstrip(".")
    for item in shared_memory:
        if clean_text == item.strip().lower().rstrip("."):
            return True
    return False


# -----------------------------
# Research Agent
# -----------------------------
class ResearchAgent:

    def __init__(self):
        self.memory = ConversationBufferMemory()

    def run(self, question):
        print("\n==============================")
        print("\n[Agent-1 | Research Module] Activated...")

        keywords = [
            "langchain",
            "multi agent",
            "shared memory",
            "individual memory",
            "vector store"
        ]

        # Check shared memory
        for kw in keywords:
            if kw in question.lower():
                for item in shared_memory:
                    if kw in item.lower():
                        print("[Agent-1] Retrieved from memory.")
                        return item

        # Research logic
        if "langchain" in question.lower():
            result = "LangChain is a framework used to build applications powered by language models with components like chains, agents, and memory."

        elif "multi agent" in question.lower():
            result = "A multi-agent system consists of multiple AI agents that collaborate to solve tasks by sharing responsibilities and communicating with each other."

        elif "shared memory" in question.lower():
            result = "Shared memory is a common storage accessible by all agents, allowing them to share and reuse information across tasks."

        elif "individual memory" in question.lower():
            result = "Individual memory is private to each agent and stores its own interaction history for context-aware processing."

        elif "vector store" in question.lower():
            result = "A vector store is used to store embeddings of data and enables efficient similarity search for retrieving relevant information."

        else:
            result = "Information not found. Please ask about LangChain or multi-agent concepts."

        self.memory.save_context({"input": question}, {"output": result})

        if not is_duplicate(result):
            shared_memory.append(result)

        return result


# -----------------------------
# Analysis Agent
# -----------------------------
class AnalysisAgent:

    def __init__(self):
        self.memory = ConversationBufferMemory()

    def run(self, research_result):

        print("\n[Agent-2 | Analysis Module] Activated...")

        analysis = research_result

        self.memory.save_context({"input": research_result}, {"output": analysis})

        if not is_duplicate(analysis):
            shared_memory.append(analysis)

        return analysis


# -----------------------------
# Summarizer Agent
# -----------------------------
class SummarizerAgent:

    def __init__(self):
        self.memory = ConversationBufferMemory()

    def run(self, analysis_result):

        print("\n[Agent-3 | Summary Module] Activated...")

        summary = analysis_result.split(".")[0]

        self.memory.save_context({"input": analysis_result}, {"output": summary})

        if not is_duplicate(summary):
            shared_memory.append(summary)

        return summary


# -----------------------------
# Create Agents
# -----------------------------
research_agent = ResearchAgent()
analysis_agent = AnalysisAgent()
summarizer_agent = SummarizerAgent()


# -----------------------------
# Orchestration Loop
# -----------------------------
while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("\nSystem shutting down...")
        break

    research_output = research_agent.run(question)
    analysis_output = analysis_agent.run(research_output)
    final_output = summarizer_agent.run(analysis_output)

    # -----------------------------
    # AI TABLE OUTPUT
    # -----------------------------
    print("\n--------------Agent Output--------------")
    print("-----------------|-----------------------------------------------")
    print(f"Research Agent   | {research_output}")
    print(f"Analysis Agent   | {analysis_output}")
    print(f"Summarizer Agent | {final_output}")

    print("\nFinal Answer:", final_output)

    print("\nShared Memory:", shared_memory)