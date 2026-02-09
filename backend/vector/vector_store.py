from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

embeddings = OpenAIEmbeddings()

vector_store = FAISS.from_texts(["initial memory"], embeddings)


def add_memory(text: str):
    doc = Document(page_content=text)
    vector_store.add_documents([doc])


def search_memory(query: str):
    return vector_store.similarity_search(query, k=3)
