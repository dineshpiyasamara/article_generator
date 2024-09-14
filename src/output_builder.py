import re

def builder(topic, result):
    # match = re.search(f"{topic}:\n", result)
    # result = result[match.span()[1]:]
    return {
        "article_title": topic,
        "article_content": result
    }