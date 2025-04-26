from googlesearch import search
from src.utils import scrape_text_from_url, extract_products
import openai
from dotenv import load_dotenv
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m",
    "--model",
    dest="model",
    help="OpenAI model",
    type=str,
    default="gpt-4.1",
    required=False,
)
parser.add_argument(
    "-p",
    "--prompt",
    dest="prompt",
    help="Prompt to the system.",
    type=str,
    required=False,
    default="Extract information as is in verbatim on each CBD gummy product you can find in this text from a website. Capture the name of the `brand`, the name of the `product`, a url to the lab report if it's available, and whether or not it's a product page. Include the URL of the product if available."
)
parser.add_argument(
    "-o",
    "--output_dir",
    dest="output_dir",
    help="Output directory",
    type=str,
    required=True,
)

parser.add_argument(
    "-s",
    "--search",
    dest="search",
    help="Search query for Google.",
    type=str,
    required=False,
    default="CBD gummies for sleep"
)

load_dotenv()

args = parser.parse_args()
client = openai.OpenAI(api_key=os.environ["OPENAI_API_KEY"])

urls = search(
    args.search, num_results=10, unique=True, lang="en", region="us"
)

for u in urls:
    text = scrape_text_from_url(u)
    if text:
        print("------------")
        print("URL:", u)
        products = extract_products(text, args.prompt, args.model, client)
        print("------------")
        print()