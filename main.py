from chatbot.bot import ChatBot
from chatbot.config import other_params, system_prompt
from chatbot.actions import known_actions, action_re


class UnknownActionError(Exception):
    """Exception raised when the bot encounters an unknown action."""
    def __init__(self, action, action_input):
        self.action = action
        self.action_input = action_input
        self.message = f"Unknown action: {action} with input: {action_input}"
        super().__init__(self.message)


def query(question, max_turns=other_params.max_turns):
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
                raise UnknownActionError(action, action_input)
            elif action=='search_internet':
                observation = known_actions[action](question, action_input)
            else:                  
                observation = known_actions[action](action_input)

            next_prompt = f"""{action} performed, resulting in Observation: {observation}, 
                                next_prompt: {next_prompt}\n"""
 
        else:
            print(result)
            print()
            # print(next_prompt)

            return result
if __name__ == "__main__":
    query("what are the most important quantum gravity theories, rank them and explain why and explain their approach, plotschematics images to explain better")
