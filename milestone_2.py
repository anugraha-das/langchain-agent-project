from langchain.tools import Tool

# ---------------- Calculator Tool ----------------
def calculator_tool(expression: str):
    try:
        result = eval(expression)
        return str(result)
    except ZeroDivisionError:
        return "Calculator Error: Division by zero."
    except Exception as e:
        return f"Calculator Error: {str(e)}"


# ---------------- Weather Tool ----------------
def weather_tool(city: str):
    try:
        weather_data = {
            "delhi": "30°C, Sunny",
            "mumbai": "28°C, Humid",
            "kochi": "29°C, Rainy"
        }

        city = city.lower()

        if city in weather_data:
            return weather_data[city]
        else:
            return "Weather API Error: City not found."

    except Exception as e:
        return f"Weather API Failure: {str(e)}"


# ---------------- Coding Tool ----------------
def coding_tool(question: str):
    return "Coding Assistant: Python loops repeat code using 'for' or 'while'."


# ---------------- Knowledge Tool ----------------
def knowledge_tool(question: str):

    knowledge = {
        "capital of india": "The capital of India is New Delhi.",
        "president of india": "The President of India is Droupadi Murmu."
    }

    q = question.lower()

    if q in knowledge:
        return knowledge[q]
    else:
        return "Knowledge not found."


# ---------------- LangChain Tools ----------------
tools = [
    Tool(
        name="Calculator",
        func=calculator_tool,
        description="Use this tool for mathematical calculations."
    ),
    Tool(
        name="WeatherAPI",
        func=weather_tool,
        description="Use this tool to get weather of a city."
    ),
    Tool(
        name="CodingAssistant",
        func=coding_tool,
        description="Use this tool for programming questions."
    ),
    Tool(
        name="KnowledgeBase",
        func=knowledge_tool,
        description="Use this tool for general knowledge questions."
    )
]

print("LangChain Tool Agent Ready (type 'exit' to stop)")

# ---------------- Chat Loop ----------------
while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    try:

        # Detect calculator expressions
        if any(op in user_input for op in ["+", "-", "*", "/"]):
            result = calculator_tool(user_input)

        # Weather queries
        elif "weather" in user_input.lower():
            city = user_input.lower().replace("weather", "").strip()
            result = weather_tool(city)

        # Coding questions
        elif "python" in user_input.lower() or "code" in user_input.lower():
            result = coding_tool(user_input)

        # Knowledge questions
        else:
            result = knowledge_tool(user_input)

        print("Agent:", result)

    except Exception as e:
        print("Agent Error:", str(e))