import json

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from config import CHUNK_SIZE, CHUNK_OVERLAP, CHROMA_DB_PATH, OPENAI_API_KEY, OPENAI_BASE_URL, EMBEDDING_MODEL

def load_articles(filepath):
    """Load articles from a JSON file."""
    with open(filepath, "r", encoding="utf-8") as f:
        articles = json.load(f)
    return articles

def chunk_articles(articles):
    """
    For each article, prepend the title to the content, then chunk.
    Store title and url as metadata for each chunk.
    """
    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    docs = []
    for article in articles:
        # Combine title and content for better retrieval
        full_text = f"Title: {article['title']}\n\n{article['content']}"
        chunks = splitter.create_documents([full_text])
        for chunk in chunks:
            # Attach metadata for citation/display
            chunk.metadata = {
                "title": article["title"],
                "url": article["url"],
            }
            docs.append(chunk)
    return docs

def index_documents(docs):
    """
    Embed and index all chunks into Chroma.
    """
    embeddings = OpenAIEmbeddings(
        openai_api_key=OPENAI_API_KEY,
        openai_api_base=OPENAI_BASE_URL,
        model=EMBEDDING_MODEL,
    )
    db = Chroma.from_documents(docs, embedding=embeddings, persist_directory=CHROMA_DB_PATH)
    return db

def ingest_and_index(json_path):
    """
    End-to-end ingestion pipeline: load, chunk, and index articles.
    """
    articles = load_articles(json_path)
    docs = chunk_articles(articles)
    db = index_documents(docs)
    print(f"Ingested {len(docs)} chunks into Chroma DB at {CHROMA_DB_PATH}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python data_ingestion.py <articles.json>")
    else:
        ingest_and_index(sys.argv[1])
