from openai import OpenAI
import json
import numpy as np
import copy
import pprint

import sqlite3

class CompilerAgent:
    def __init__(self):
        self.client = OpenAI(organization = 'org-miLxPVrUMo3EKEXwFxGkDoiS',
                            project = 'proj_oS3d7Rnjgr141tDhCN7hZohr')

    def prompt_model(self, model, prompt):
        completion = self.client.chat.completions.create(
            model=model,
            store=True,
            messages=[
                {"role": "user", 'content': prompt}
            ],
            response_format= {"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)

    def get_answer(self, question, sub_tasks):
        instruction = f"""
        You are an HR Agent. You have access to RAG Agents which provide you with information that helps you answer questions.
        Given the information provided by these RAG agents, you need to compile the information and provide a final answer to the user.
        
        Respond only a JSON object containing:
        "answer": the final answer you would provide to the user, NA if you don't know

        """
        
        prompt = f"""{instruction}

        Here is the data fetched from the RAG agents:
        {pprint.pformat(sub_tasks)}

        Question : 
        {question}
        """
        
        print("Prompt to Compiler Agent: ", prompt)
        
        response = self.prompt_model("gpt-4o-mini", prompt)
        
        result = response['answer']
        return result  