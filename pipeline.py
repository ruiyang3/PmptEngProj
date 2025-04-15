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

    def run(self, query):
        print("Query : ", query)
        answer = self.sub_task_formulator.generate_sub_tasks(query)
        
        print("Sub Tasks Generated:")
        i = 0
        for sub_task in answer["sub-tasks"]:
            if sub_task['module'] == 'Policy RAG':
                pass                
            elif sub_task['module'] == 'Database RAG':
                question = sub_task['question']
                sql_answer = self.sql_agent.get_answer(question)
                sub_task['answer'] = sql_answer
                print(f"Sub Task {i} : {question} => {sql_answer}")
            i += 1
        # answer = self.compiler_agent.compile(query, answer)
        
        return "Hello World"