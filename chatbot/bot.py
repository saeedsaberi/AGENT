import re, openai
from .config import api_config, model_config

openai.api_key = api_config['openai_api_key']


class ChatBot:
    def __init__(self, system="", model=model_config['default_model']):
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
        print(self.model,self.messages)
        completion = openai.chat.completions.create(
            model= self.model, 
            messages=self.messages
        )
        return completion.choices[0].message.content
