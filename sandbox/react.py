# This code is Apache 2 licensed:
# https://www.apache.org/licenses/LICENSE-2.0
import openai
from openai import OpenAI
import re, os
import httpx


openai.api_key = os.environ["OPENAI_API_KEY"]
messages = [{"role": "system", "content": "You are an intelligent assistant."}]
   

client = OpenAI(api_key=openai.api_key)
# MODEL="gpt-4o-mini" # "gpt-3.5-turbo",  # or "gpt-4" if you want to use that model

class ChatBot:
    def __init__(self, system="", model="gpt-4o-mini"):
        self.system = system
        self.model = model
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})
    
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self):
        print(self.model,type(self.messages))
        completion = openai.chat.completions.create(
            model= "gpt-4o-mini", 
            messages=self.messages
        )
        # Uncomment this to print out token usage each time, e.g.
        # {"completion_tokens": 86, "prompt_tokens": 26, "total_tokens": 112}
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

prompt = """
        You run in a loop of Thought, Action, PAUSE, Observation.
        At the end of the loop you output an Answer
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

        You then output:

        Answer: The capital of France is Paris
""".strip()


action_re = re.compile('^Action: (\w+): (.*)$')

def query(question, max_turns=5):
    i = 0
    bot = ChatBot(prompt)
    next_prompt = question
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        print(result)
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}: {}".format(action, action_input))
            print(" -- running {} {}".format(action, action_input))
            observation = known_actions[action](action_input)
            print("Observation:", observation)
            next_prompt = "Observation: {}".format(observation)
        else:
            return


def wikipedia(q):
    return httpx.get("https://en.wikipedia.org/w/api.php", params={
        "action": "query",
        "list": "search",
        "srsearch": q,
        "format": "json"
    }).json()["query"]["search"][0]["snippet"]


def simon_blog_search(q):
    results = httpx.get("https://datasette.simonwillison.net/simonwillisonblog.json", params={
        "sql": """
        select
          blog_entry.title || ': ' || substr(html_strip_tags(blog_entry.body), 0, 1000) as text,
          blog_entry.created
        from
          blog_entry join blog_entry_fts on blog_entry.rowid = blog_entry_fts.rowid
        where
          blog_entry_fts match escape_fts(:q)
        order by
          blog_entry_fts.rank
        limit
          1""".strip(),
        "_shape": "array",
        "q": q,
    }).json()
    return results[0]["text"]

def calculate(what):
    return eval(what)

known_actions = {
    "wikipedia": wikipedia,
    "calculate": calculate,
    "search_internet": search_internet
}
query("what are the most important quantum gravity theories, rank them and explain why and explain their approach")