from openai import OpenAI
import json
import numpy as np
import copy

import sqlite3

class SQLAgent:
    def __init__(self, db_path, schema_path):
        self.db_path = db_path
        
        self.schema = open(schema_path, 'r').read()
        
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

    def execute_query(self, query):
        conn = sqlite3.connect(self.db_path)

        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        
        description = [d[0] for d in cursor.description]
        
        ans = []
        ans.append(description)
        for row in result:
            ans.append(list(row))
                
        cursor.close()
        conn.close()
        return ans

    def get_answer(self, question):
        instruction = f"""
        You are a SQL expert. You have to write SQL queries to extract information from the HRMS database.

        Respond only a JSON object containing:
        "sql": the SQL query you would use to extract the information, NA if you don't know
        """
        
        prompt = f"""{instruction}

        The schema of the HRMS database is as follows:
        {self.schema}

        Help me get information to answer the question:
        {question}
        """
        
        response = self.prompt_model("gpt-4o-mini", prompt)
        
        if response['sql'] == "NA":
            return response['sql']
        
        query = response['sql']
        
        try:
            result = self.execute_query(query)
        except Exception as e:
            print(f"Error executing query: {e}")
            return "NA"

        return result        
    
    
    
if __name__ == "__main__":
    db_path = "./sql_rag_assets/hrms.db"
    schema_path = "./sql_rag_assets/schema.sql"
    
    sql_agent = SQLAgent(db_path, schema_path)
    
    question = "What is the name of the employee with ID 1?"
    result = sql_agent.get_answer(question)
    
    print(result)