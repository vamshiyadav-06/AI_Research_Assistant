import requests

from bs4 import BeautifulSoup


def read_website(url: str):

    response = requests.get(
        url,
        timeout=10
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    text = soup.get_text(
        separator=" ",
        strip=True
    )

    return text[:12000]