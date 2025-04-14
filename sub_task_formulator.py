from PromptModel import prompt_model
import json


def task_formulator_prompt_generation(user_question):
    system_prompt = f"""
    You are a sub-task planning agent.

    Your job is to take a complex user question and decompose it into two specific sub-questions:
    1. A sub-question for the policy RAG module — this should retrieve or reason over rules, policies, or regulations.
    2. A sub-question for the database RAG module — this should retrieve or query structured factual information from a database (e.g., employee records, system logs, operational data).

    Guidelines:
    - DO NOT explain anything.
    - DO NOT provide a paragraph or answer.
    - DO NOT say "It depends" or give advice.
    - DO NOT include bullet points or context.
    - JUST OUTPUT two clear questions.
    - output your answer in JSON format.

    Output format:
    Policy RAG: [your question here]
    Database RAG: [your question here]

    Example:
    User Question:
    "Is a manager allowed to revoke access to the finance dashboard without prior notice?"

    Output:
    {{
        \"Policy RAG\": \"What do company policies state about managers revoking access to dashboards without prior notice?\",
        \"Database RAG\": \"Has the finance dashboard access for the user been revoked recently, and was any prior notice logged?\"  
    }}
    
    The given question:
    {user_question}
    """
    return system_prompt

def generate_sub_task(user_question):
    sub_task_formulator_prompt = task_formulator_prompt_generation(user_question)
    model_output = prompt_model(sub_task_formulator_prompt)
    successfully_load = False
    model_output_dict = json.loads(model_output)
    policy_rag_task = model_output_dict['Policy RAG']
    database_rag_task = model_output_dict['Database RAG']
    return policy_rag_task, database_rag_task


