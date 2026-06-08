import os

from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


def search_web(query: str):

    response = client.search(
        query=query,
        max_results=5
    )

    results_text = ""

    for result in response["results"]:

        results_text += f"""
Title: {result.get('title')}
Content: {result.get('content')}
URL: {result.get('url')}

"""

    return results_text