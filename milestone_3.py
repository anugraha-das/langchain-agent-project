from langchain.memory import ConversationBufferMemory


# Shared Memory

shared_memory = []


# to remove duplicates

def is_duplicate(text):
    clean_text = text.strip().lower().rstrip(".")
    for item in shared_memory:
        if clean_text == item.strip().lower().rstrip("."):
            return True
    return False


# Research Agent

class ResearchAgent:

    def __init__(self):
        self.memory = ConversationBufferMemory()

    def run(self, question):

        print("\nResearch Agent is researching...")

        keywords = ["python", "java", "ai in healthcare"]

        # Checking shared memory
        for kw in keywords:
            if kw in question.lower():
                for item in shared_memory:
                    if kw in item.lower():
                        print("Research Agent retrieved answer from memory.")
                        return item

        # Research topics
        if "python" in question.lower():
            result = "Python is a high-level programming language used for AI, web development and automation."
        elif "java" in question.lower():
            result = "Java is an object-oriented programming language widely used for enterprise applications."
        elif "ai in healthcare" in question.lower():
            result = "AI in healthcare refers to the use of artificial intelligence technologies to improve diagnosis, treatment, patient care, and hospital management."
        else:
            result = "Information not found."

        self.memory.save_context({"input": question}, {"output": result})

        if not is_duplicate(result):
            shared_memory.append(result)

        return result



# Analysis Agent 

class AnalysisAgent:

    def __init__(self):
        self.memory = ConversationBufferMemory()

    def run(self, research_result):

        print("\nAnalysis Agent is analyzing...")

        #  passing data
        analysis = research_result

        self.memory.save_context({"input": research_result}, {"output": analysis})

        if not is_duplicate(analysis):
            shared_memory.append(analysis)

        return analysis



# Summarizer Agent

class SummarizerAgent:

    def __init__(self):
        self.memory = ConversationBufferMemory()

    def run(self, analysis_result):

        print("\nSummarizer Agent is summarizing...")

        summary = analysis_result.split(".")[0]

        self.memory.save_context({"input": analysis_result}, {"output": summary})

        if not is_duplicate(summary):
            shared_memory.append(summary)

        return summary



# Agent creation

research_agent = ResearchAgent()
analysis_agent = AnalysisAgent()
summarizer_agent = SummarizerAgent()



# Orchestration Loop

while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        print("Program ended.")
        break

    research_output = research_agent.run(question)

    analysis_output = analysis_agent.run(research_output)

    final_output = summarizer_agent.run(analysis_output)

    print("\nFinal Answer:", final_output)

    print("\nShared Memory:", shared_memory)