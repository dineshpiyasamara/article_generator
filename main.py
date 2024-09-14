from flask import Flask, jsonify, request
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from src.llm import openai_llm
from src.embedding import openai_embedding
from src.parser import output_parser
from src.template import prompt_template
from src.data_loader import pdf_loader
from src.output_builder import builder
from src.logger import logging
from params import *

app = Flask(__name__)

llm = openai_llm()
embedding_model = openai_embedding()
parser = output_parser()
prompt = prompt_template()


def generator(inputs):
    retriever_output = {
        'context': inputs["retriever"].invoke(inputs['topic']),
        'topic': inputs['topic'],
        'language': inputs['language']
    }
    llm_input = prompt.invoke(retriever_output)
    llm_output = llm.invoke(llm_input)
    parsed_output = parser.invoke(llm_output)
    return parsed_output


@app.route("/api/test", methods=['GET'])
def test_api():
    return "Working..."


@app.route("/api/generate_article", methods=['POST'])
def article_generator():
    try:
        data = request.get_json()

        topic = data["topic"]
        language = data["language"]
        data_path = data["data_path"]

        logging.info(f"Requested topic: {topic}")
        logging.info(f"Requested language: {language}")
        logging.info(f"Requested data path: {data_path}")

        docs = pdf_loader(data_path)

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_SIZE)

        splits = text_splitter.split_documents(docs)
        logging.info(f"Number of chunks: {len(splits)}")

        vectorstore = FAISS.from_documents(
            documents=splits, embedding=embedding_model)
        logging.info(f"Build vector store")

        retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

        result = generator(
            {"topic": topic, "language": language, "retriever": retriever})

        final_result = builder(topic=topic, result=result)
        logging.info(f"Final Response: {final_result}")

        final_result["status"] = "success"

        return final_result
    except Exception as e:
        print(e)
        return {
            "status": "failed"
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
