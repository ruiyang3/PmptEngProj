from tqdm import tqdm
from policy_rag_utils.DocProcessing import policy_tokenize, token_to_text
from policy_rag_utils.PromptModel import prompt_model

import json, chromadb

# chunk the tokens of policy text into equally-long chunks
def chunk_text(text, chunk_size=2048, overlap=1024):
    tokens = policy_tokenize(text)
    chunks = []
    start_index = 0
    while start_index < len(tokens):
        end_index = start_index + chunk_size
        if end_index > len(tokens):
            end_index = len(tokens)
        # decode the tokens back to text
        chunk = token_to_text(tokens[start_index:end_index])
        chunks.append(chunk)
        start_index += chunk_size - overlap
    print(f"The number of chucks:{len(chunks)}")
    return chunks

def generate_vectorize_prompt(chuck):
    prompt_instructions = "You are a helpful assistant to generate questions. Please generate 3 questions based on the given context. The questions can be based on the information in the context and the overall understanding of the context. Your response should be in a list of JSON format questions. The format is AS FOLLOWS. Your response should ONLY contains the generated questions in the given format."
    format = "[{\"question\":\"your generated question 1 here\"}, {\"question\":\"your generated question 2 here\"},...,{\"question\":\"your generated question n here\"}]"
    prompt = f"<Instructions>: {prompt_instructions}\n<Context>: {chuck}\n<Format>: {format}"
    return prompt

def generate_questions(chucks):
    chucks_dictionary = dict()
    question_list = []
    index = 0
    for chuck in tqdm(chucks, total=len(chucks), desc="Generating questions"):
        # generate an index for the chuck
        chucks_dictionary[index] = chuck
        prompt = generate_vectorize_prompt(chuck)
        regenerate = True
        questions = []
        chucks_json = []
        while regenerate:
            try:
                # get the model's answer
                answer = prompt_model(prompt)
                # resolve the answer using JSON
                data = json.loads(answer)
                for question in data:
                    questions.append({'question': question['question'], 'index': index})
                regenerate = False
            except Exception as e:
                # error in resolving model's answer
                # delay after **delay** seconds to ask model again
                regenerate = True
                questions = []
        question_list.extend(questions)
        index += 1
    print(f"generated {len(question_list)} questions for the chucks.")
    # keep the questionList and the chucks in Json format
    with open('policy_rag_assets/questionList.json', 'w+', encoding='utf-8') as f:
        json.dump(question_list, f, ensure_ascii=False, indent=4)
    with open('policy_rag_assets/chucks.json', 'w+', encoding='utf-8') as f:
        json.dump(chucks_dictionary, f, ensure_ascii=False, indent=4)

def vectorize_questions(question_list):
    chromadb.api.client.SharedSystemClient.clear_system_cache()
    chroma_client = chromadb.PersistentClient(path="policy_rag_assets/chroma_db")
    collection = chroma_client.get_or_create_collection(name="qa_index")

    # add questions in DB
    main_index = 0
    for question_index in tqdm(question_list, total=len(question_list), desc="Generating Vector Database"):
        collection.add(
            ids=[str(main_index)],
            documents=[question_index['question']],  # the generated questions
            metadatas=[{"index": question_index['index']}]  # index to the chucks
        )
        main_index += 1
    return collection