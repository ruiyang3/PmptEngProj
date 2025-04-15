import json
from openai import OpenAI

class SubTaskFormulatorAgent:
    def __init__(self):
        self.policy_rag_name = "Policy RAG"
        self.database_rag_name = "Database RAG"

    def prompt_model(self, prompt):
        client = OpenAI(
            organization='org-miLxPVrUMo3EKEXwFxGkDoiS',
            project='proj_oS3d7Rnjgr141tDhCN7hZohr',
        )
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            store=True,
            messages=[
                {"role": "user", 'content': prompt}
            ]
        )
        return completion.choices[0].message.content
    
    def task_formulator_prompt_generation(self, user_question):
        system_prompt = """
        You are a sub-task planning agent. You have access to two modules: a policy RAG module and a database RAG module.

        Your job is to take a complex user question, think of the policies and data required need to answer this complex question and generate questions that the two to fetch that data.
        
        Here's a brief overview of the two modules:
        - Policy RAG: This module retrieves relevant company policies and guidelines from the CMU Employee Handbook.
        - Database RAG: This module retrieves relevant data from the HRMS database. Please ask only simple questions that can be answered by the database.
        
        The schema of the HRMS database is as follows:
        CREATE TABLE tb1 (
            one TEXT,
            two INTEGER
        );
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT
        );
        CREATE TABLE designations (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            title TEXT,
            descriptions TEXT
        );
        CREATE TABLE schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            title TEXT,
            time_in TEXT,
            time_out TEXT
        );
        CREATE TABLE leaves (
            id INTEGER PRIMARY KEY NOT NULL UNIQUE,
            employee_id INTEGER REFERENCES employees(id) NOT DEFERRABLE,
            start_date TEXT,
            end_date TEXT,
            type TEXT,
            reason TEXT
        );
        CREATE TABLE attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            employee_id INTEGER REFERENCES employees(id) NOT DEFERRABLE,
            title TEXT,
            time TEXT,
            date TEXT
        );
        CREATE TABLE overtime (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            employee_id INTEGER REFERENCES employees(id),
            duration INTEGER,
            date TEXT
        );
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            department_id INTEGER REFERENCES departments(id),
            designation_id INTEGER REFERENCES designations(id),
            schedule_id INTEGER REFERENCES schedules(id),
            first_name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT,
            gender TEXT
        );


        Guidelines:
        - DO NOT explain anything.
        - DO NOT provide a paragraph or answer.
        - DO NOT say "It depends" or give advice.
        - DO NOT include bullet points or context.
        - JUST OUTPUT clear questions that can be answered by the modules.
        - output your answer in JSON format.

        Output format:
        {
            "sub-tasks" : [
            {"module" : "Policy RAG", "question": "[your question here]"},
            {"module" : "Database RAG", "question": "[your question here]"}
            {"module" : "Policy RAG", "question": "[your question here]"},
            {"module" : "Database RAG", "question": "[your question here]"}
            ]
        }

        Example:
        User Question:
        "Is a manager allowed to revoke access to the finance dashboard without prior notice?"

        Output:
        {
            "sub-tasks" : [
            {"module": "Policy RAG", "question": "[your question here]"},
            {"module": "Database RAG", "question": "[your question here]"},
            ]
        }
            
        The given question: \n
        """
        
        system_prompt += user_question
        return system_prompt

    def generate_sub_tasks(self, user_question):
        sub_task_formulator_prompt = self.task_formulator_prompt_generation(user_question)
        model_output = self.prompt_model(sub_task_formulator_prompt)
        print("[SubTask] Model Output: ", model_output)
        
        model_output_dict = json.loads(model_output)
        return model_output_dict


