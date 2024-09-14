from langchain_community.document_loaders import PyPDFLoader

def pdf_loader(path):
    loader = PyPDFLoader(path)
    docs = loader.load()
    return docs