import os
from chatbot.actions import wikipedia, calculate, plot, action_re

# API Configuration
api_config = {
    "openai_api_key": os.environ.get("OPENAI_API_KEY", "your-default-api-key"),
}

# Model Configuration
model_config = {
    "default_model": "gpt-4o-mini",
    "temperature": 0.7,
    "max_tokens": 150,
}

# Other Parameters
other_params = {
    "max_turns": 5,
    "retry_attempts": 3,
}

known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "plot": plot,
}


system_prompt = """
You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

calculate:
e.g. calculate: 4 * 7 / 3
Runs a calculation and returns the number - uses Python so be sure to use floating point syntax if necessary

wikipedia:
e.g. wikipedia: Django
Returns a summary from searching Wikipedia

search_internet:
e.g. search_internet: Quantum Gravity Theories
Searches the internet for the given query, ranks the results, and provides a summary with citations.

plot:
e.g. plot: [(1, 2), (2, 4), (3, 6)]
Generates a plot from the given data points and returns the plot as a base64 encoded image.

Always look things up on Wikipedia if you have the opportunity to do so.

Example session:

Question: What is the capital of France?
Thought: I should look up France on Wikipedia.
Action: wikipedia: France
PAUSE

You will be called again with this:

Observation: France is a country. The capital is Paris.

You then output:

Answer: The capital of France is Paris.
"""
