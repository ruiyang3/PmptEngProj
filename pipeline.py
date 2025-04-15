from sub_task_formulator import SubTaskFormulatorAgent
from sql_rag_api import SQLAgent
from policy_rag_api import policy_rag_init
from policy_rag_api import get_answer as policy_rag_answer

class PipelineRAG:
    def __init__(self):
        self.sub_task_formulator = SubTaskFormulatorAgent()
        self.sql_agent = SQLAgent(db_path="./sql_rag_assets/hrms.db", schema_path="./sql_rag_assets/schema.sql")
        self.polict_agent = None
        self.compiler_agent = None
        
        # Policy Agent
        # self.policy_chucks, self.questions_db = policy_rag_init()        

    def run(self, query):
        subtasks = self.sub_task_formulator.generate_sub_tasks(query)
        
        subtasks_w_answers = []
        subtasks_output = "" 
        for idx, sub_task in enumerate(subtasks["sub-tasks"]):
            subtasks_output += f"Sub-task {idx+1} :: {sub_task['module']} :: {sub_task['question']}\n"
            if sub_task['module'] == 'Policy RAG':
                question = sub_task['question']
                # answer = policy_rag_answer(question, self.questions_db, self.policy_chucks)
                sub_task['answer'] = answer
            elif sub_task['module'] == 'Database RAG':
                question = sub_task['question']
                sql_query, answer = self.sql_agent.get_answer(question)
                sub_task['answer'] = str(sql_query) + " ---- " + str(answer)
            
            subtasks_w_answers.append(sub_task)
                
        # compiled_output = self.compiler_agent.compile(query, answer)        
        
        return subtasks_output, subtasks_w_answers