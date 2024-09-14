from langchain.embeddings import HuggingFaceEmbeddings
from langchain_openai import OpenAIEmbeddings

def huggingface_embedding():
    embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
    )
    return embedding_model

def openai_embedding():
    embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-small"
    )
    return embedding_model