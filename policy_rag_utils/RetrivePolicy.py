
def rag_prompt_generation(context_list, question):
    prompt_instructions = "You are a helpful assistant to generate answers. Please generate answer to the question based on the given context. Please generate your answer in a sentence based on 3 paragraph of contexts. If you can't find the answer to the question in the given context, answer \"IDK\"."
    prompt = f"<Instructions>: {prompt_instructions}\n<Context1>: {context_list[0]}\n<Context2>: {context_list[1]}\n<Context3>: {context_list[2]}\nquestion: {question}"
    return prompt

def get_most_relevant_context(db_collection, question, chucks_dict):
    most_relevant_questions= db_collection.query(
        query_texts=[question],
        n_results=3  # Return the top 3 most relevant questions
    )
    most_relevant_indexes = [item["index"] for item in most_relevant_questions["metadatas"][0]]
    most_relevant_context = [chucks_dict[str(index)]for index in most_relevant_indexes]
    return most_relevant_context




