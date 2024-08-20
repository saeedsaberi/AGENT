# main.py

from chatbot.bot import ChatBot
from chatbot.config import other_params, system_prompt
from chatbot.actions import known_actions, action_re

def query(question, max_turns=5):
    """
    Executes a chatbot query to answer a given question.
    
    Args:
        question (str): The question to be answered.
        max_turns (int, optional): The maximum number of turns allowed for the query. Defaults to 5.
    
    Returns:
        str: The answer to the question.
    
    Raises:
        Exception: If the bot encounters an unknown action.
    
    """
    bot = ChatBot(system=system_prompt)
    next_prompt = question
    i = 0
    while i < other_params['max_turns']:
        i += 1
        result = bot(next_prompt)
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception(f"Unknown action: {action}: {action_input}")
            else:
                print('aha',actions)
                print()
                print()


            observation = known_actions[action](action_input)
            print(observation)
            print()
            print()
            next_prompt = f"Observation: {observation}"
        else:
            return result

if __name__ == "__main__":
    query("what are the most important quantum gravity theories, rank them and explain why and explain their approach")
