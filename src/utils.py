import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from src.product import ProductList
import logging
from typing import Union
import openai

logging.basicConfig()
logger = logging.getLogger("utils")
logging.getLogger().setLevel(logging.INFO)


def extract_products(
    text: str, prompt: str, model: str, client: openai.Client
) -> Union[ProductList, None]:
    messages: list[dict[str, str]] = []
    base_prompt = {"role": "system", "content": prompt}
    text_prompt = {"role": "user", "content": f"[TEXT START]\n{text}\n[TEXT END]"}
    messages.extend([base_prompt, text_prompt])
    try:
        response = client.beta.chat.completions.parse(
            model=model,
            response_format=ProductList,
            messages=messages,
            temperature=1.18,
            max_tokens=250,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        for choice in range(len(response.choices)):
            logger.info(f"Choice number {choice}\n")
            for p in response.choices[choice].message.parsed.products:
                print(p)
                print()
        return response.choices
    except openai.NotFoundErr as err:
        logger.error(f"Could not return response. Error: {err}")
        return None


def scrape_internal_urls(url) -> list[str]:
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Failed to fetch URL: {url}")
        return []

    # Create a BeautifulSoup object
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract all anchor tags
    anchor_tags = soup.find_all("a", href=True)

    # Get base URL for relative links
    base_url = urlparse(url).scheme + "://" + urlparse(url).netloc

    internal_urls = set()

    # Extract internal URLs
    for tag in anchor_tags:
        href = tag["href"]
        if href.startswith("/") or href.startswith(base_url):
            internal_urls.add(urljoin(base_url, href))

    return list(internal_urls)


def scrape_text_from_url(url: str) -> Union[str, None]:
    try:
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch URL: {url}")
            return None

        soup = BeautifulSoup(response.content, "html.parser")
        text = soup.get_text()

        return text.strip().replace("  ", "")

    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None
