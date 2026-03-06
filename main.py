from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_community.llms.fake import FakeListLLM

# --- STEP 1: THE MEGA SCRIPT DATABASE ---
# Each key represents a "Domain". The lists contains the Thought and the Final Answer.
script_database = {
    "math": [
        "Thought: The user has a calculation request. I will use the Calculator tool.\nAction: Calculator\nAction Input: 50 * 2",
        "Final Answer: 50 multiplied by 2 is 100."
    ],
    "weather": [
        "Thought: Checking the atmospheric data for the requested location.\nAction: WeatherTool\nAction Input: Kozhikode",
        "Final Answer: It is currently 31°C with 65% humidity in Kozhikode. Expect clear skies!"
    ],
    "code": [
        "Thought: I need to provide a clean Python example for the user.\nAction: CodingAssistant\nAction Input: Python Hello World",
        "Final Answer: To get started, use: print('Hello, Python World!'). It's the standard first step."
    ],
    "research": [
        "Thought: Accessing the knowledge base for 2026 AI trends.\nAction: KnowledgeBase\nAction Input: AI Agents 2026",
        "Final Answer: In 2026, the focus has shifted from simple chatbots to 'Agentic Workflows'—AI that can plan and execute multi-step tasks."
    ],
    "translate": [
        "Thought: The user wants a translation. I will use the Translator tool.\nAction: Translator\nAction Input: How are you?",
        "Final Answer: The Malayalam translation is: സുഖമാണോ? (Sukhamano?)"
    ],
    "travel": [
        "Thought: Looking up local tourism data for planning.\nAction: TravelPlanner\nAction Input: Munnar Trip",
        "Final Answer: For a 2-day Munnar trip: Visit Eravikulam National Park on Day 1 and the Tea Museum on Day 2!"
    ],
    "motivation": [
        "Thought: The user needs a boost. I will check the KnowledgeBase for inspiration.\nAction: KnowledgeBase\nAction Input: Motivation",
        "Final Answer: 'The only way to do great work is to love what you do.' - Steve Jobs. Keep going!"
    ],
    "default": [
        "Thought: I am not specifically programmed for this query yet.\nFinal Answer: I am a specialized Assistant. Try asking about Math, Weather, Coding, Research, Travel, or Translation!"
    ]
}

# --- STEP 2:THE TOOLS (6 Distinct Capabilities) ---
tools = [
    Tool(name="Calculator", func=lambda x: str(eval(x)), description="Solves math."),
    Tool(name="KnowledgeBase", func=lambda x: "Data Found", description="General info."),
    Tool(name="WeatherTool", func=lambda x: "Clear Skies", description="Weather info."),
    Tool(name="CodingAssistant", func=lambda x: "Code Ready", description="Writes code."),
    Tool(name="Translator", func=lambda x: "Translated", description="Languages."),
    Tool(name="TravelPlanner", func=lambda x: "Itinerary Set", description="Travel help.")
]

# --- STEP 3: THE PROMPT TEMPLATE ---
template = """Answer the following questions as best you can. You have access to:
{tools}

Use the following format:
Question: {input}
Thought: [Your Reasoning]
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat)
Thought: I now know the final answer
Final Answer: the final answer

Begin!
Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

# --- STEP 4: INTERFACE & LOGIC ---
if __name__ == "__main__":
    print("\n" + "="*55)
    print("      MILESTONE 1: ADVANCED MULTI-DOMAIN AGENT")
    print("="*55)
    print("TOPICS: Math | Weather | Code | Research | Travel | Malayalam")
    
    while True:
        user_query = input("\nYou: ").lower()
        if user_query in ["exit", "quit", "bye"]:
            print("Shutting down agent. Goodbye!")
            break

        # SMART ROUTING: Select script based on keyword detection
        if any(word in user_query for word in ["math", "calculate", "50", "plus"]):
            selected_script = script_database["math"]
        elif "weather" in user_query:
            selected_script = script_database["weather"]
        elif any(word in user_query for word in ["code", "python", "script"]):
            selected_script = script_database["code"]
        elif any(word in user_query for word in ["research", "trend", "future"]):
            selected_script = script_database["research"]
        elif any(word in user_query for word in ["translate", "malayalam", "language"]):
            selected_script = script_database["translate"]
        elif any(word in user_query for word in ["travel", "trip", "munnar", "vacation"]):
            selected_script = script_database["travel"]
        elif any(word in user_query for word in ["motivation", "quote", "inspire"]):
            selected_script = script_database["motivation"]
        else:
            selected_script = script_database["default"]

        # Initialize LLM with the specific script
        llm = FakeListLLM(responses=selected_script)
        
        # Build Agent
        agent = create_react_agent(llm, tools, prompt)
        executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
        
        # Run Execution
        print("\n--- AGENT PROCESSING ---")
        executor.invoke({"input": user_query})