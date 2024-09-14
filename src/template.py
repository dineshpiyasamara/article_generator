from langchain.prompts import ChatPromptTemplate

def prompt_template():
    template = """
    Generate an article about '{topic}' in {language} language using the provided context only.
    If context not related to topic return don't know.

    Context:
    {context}

    {topic}:
    """
    prompt=ChatPromptTemplate.from_template(template)
    return prompt