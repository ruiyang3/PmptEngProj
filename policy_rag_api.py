"""
This is the API for the policy RAG.
It provides all the apis for initialize the policy RAG and get answer of the policy RAG.
"""
import json
import os

import chromadb

from policy_rag_utils.ChuckVectorize import chunk_text, generate_questions, vectorize_questions
from policy_rag_utils.DocProcessing import policy_processing
from policy_rag_utils.PromptModel import prompt_model
from policy_rag_utils.RetrivePolicy import get_most_relevant_context, rag_prompt_generation


# initialize the policy RAG.
def policy_rag_init():
    # check if the chucks.json and questionList.json are in assets
    try:
        with open('policy_rag_assets/chucks.json', 'r', encoding='utf-8') as f:
            policy_chucks = json.load(f)
        with open('policy_rag_assets/questionList.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)
    except FileNotFoundError:
        # generate the policy chucks and questions
        # extract the text from the PDF file
        print("Can find the chucks file or the questions file. Re-generate from policy.")
        policy_text = policy_processing("policy_rag_assets/policy")
        chucks = []
        for policy in policy_text:
            curr_policy_chucks = chunk_text(policy['text'])
            chucks.extend(curr_policy_chucks)
        generate_questions(chucks)
        with open('policy_rag_assets/chucks.json', 'r', encoding='utf-8') as f:
            policy_chucks = json.load(f)
        with open('policy_rag_assets/questionList.json', 'r', encoding='utf-8') as f:
            questions = json.load(f)

    # check if the questions have vectorized and put into chromadb
    chromadb.api.client.SharedSystemClient.clear_system_cache()
    chroma_client = chromadb.PersistentClient(path="policy_rag_assets/chroma_db")
    try:
        questions_db = chroma_client.get_collection(name="qa_index")
    except Exception as e:
        print(e)
        print("Error while getting collection. re-vectorize the questions")
        questions_db = vectorize_questions(questions)

    # policy_chucks is the dict of the chucked and indexed text chucks
    # questions_db is the vectorized questions
    return policy_chucks, questions_db

def get_answer(question, db_collection, chucks_dict):
    relevant_context = get_most_relevant_context(db_collection, question, chucks_dict)
    prompt = rag_prompt_generation(relevant_context, question)
    answer = prompt_model(prompt)
    return answer










