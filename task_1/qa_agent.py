from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from config import CHROMA_DB_PATH, OPENAI_API_KEY, OPENAI_BASE_URL, GENERATION_MODEL, EMBEDDING_MODEL

def load_vector_db():
    embeddings = OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_BASE_URL,
        model=EMBEDDING_MODEL,
    )
    db = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)
    return db

def build_qa_agent():
    db = load_vector_db()
    retriever = db.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 3,
            "fetch_k": 20
        }
    )
    template = """
                You are a helpful support assistant for Intercom.

                Instructions:
                - Use ONLY the information provided in the "Context" section below to answer the user's question.
                - If the answer is not explicitly found in the context, reply ONLY with: "I don't know based on the provided information."
                - Do NOT make up any information or use any outside knowledge.
                - If steps, bullet points, or a summary are present in the context, include them in your answer.
                - If relevant sources (titles and URLs) are included, you may reference or cite them as part of your answer.
                - Your responses must be clear, concise, and directly answer the user's question.

                Context:
                {context}

                User question: {question}
                """
    prompt = ChatPromptTemplate.from_template(template)
    llm = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_BASE_URL,
        model=GENERATION_MODEL,
        )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type="stuff",
        chain_type_kwargs={"prompt": prompt},
    )
    return qa

def answer_question(question):
    qa = build_qa_agent()
    result = qa.invoke(question)
    answer = result["result"]
    refusal_phrases = [
        "i don't know",
        "the provided context does not contain",
        "no information",
        "not in the context",
        "cannot answer",
        "no relevant information"
    ]
    is_refusal = any(phrase in answer.lower() for phrase in refusal_phrases)
    if is_refusal:
        return answer
    sources_set = set()
    for doc in result["source_documents"]:
        meta = doc.metadata
        sources_set.add(f"{50 * '-'}\nTitle: {meta['title']}]\nLink: {meta['url']}")
    if sources_set:
        answer += "\n\nSources:\n" + "\n".join(sources_set)
    return answer

if __name__ == "__main__":
    question = input("Ask a question: ")
    print(answer_question(question))
